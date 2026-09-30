# -*- coding: utf-8 -*-

'''
A script to estimate ages for FGK stars based on empirical relations between Li abundance, age, [Fe/H], and effective temperature from Rathsam et al. (2026?).
'''

import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names") # otherwise error calculation would spam the terminal

# loading the model:
MODEL_PATH = Path(__file__).parent / 'data/angelica_model.joblib'

bundle = joblib.load(MODEL_PATH)

scaler       = bundle["scaler"]
model        = bundle["model"]
feature_cols = bundle["feature_cols"]
target_col   = bundle["target_col"]

BOUNDS = {
    'teff':       (5400.0, 6500.0),
    '[Fe/H]':     (-0.3,    0.4),
    'logg':       (4.0,     4.6),
    'Li_3D_NLTE': (-1.0,     3.5),
    }

def age_predict(
    x_input: pd.DataFrame,
    errors: bool = True,
    feature_cols: list = feature_cols,
    target_col: str = target_col,
    scaler = scaler,
    model = model):

    """
    Predicts the age of stars based on their Teff, logg, [Fe/H], and 3D NLTE Li abundance.

    Parameters:
        x_input (pd.DataFrame): Input DataFrame containing the stellar parameters.
        errors (bool): Whether to include prediction errors in the output.
        feature_cols (list): List of feature column names.
        target_col (str): Name of the target column.
        scaler: Scaler object for feature scaling.
        model: Trained model for prediction.

    Returns a DataFrame with original features and predicted age, with errors (when set to True).
    """

    # Check that the required stellar parameters are present in the DataFrame
    cols_params = ['teff', '[Fe/H]', 'logg', 'Li_3D_NLTE']
    missing_cols_params = [col for col in cols_params if col not in x_input.columns]
    if missing_cols_params:
        raise ValueError(f"Missing required feature columns: {missing_cols_params}")

    # Scale the features, selecting only the required columns
    X_scaled = scaler.transform(x_input[feature_cols])

    # Make predictions
    age_pred = model.predict(X_scaled)

    # Create a new DataFrame with predictions
    result_df = x_input.copy()
    result_df['age'] = age_pred

    # Checking that the parameters are within the bounds of the training data:
    in_bounds = pd.Series(True, index=result_df.index)
    for param, (lo, hi) in BOUNDS.items():
        in_bounds &= (result_df[param] >= lo) & (result_df[param] <= hi)

    result_df.loc[~in_bounds, 'age'] = np.nan # Set age to NaN for out-of-bounds parameters

    if errors:
        model_err = 0.482 # standard deviation of the model residuals

        # Check if all required error columns are present in the DataFrame. If not, set them to 0.0
        error_cols = ['e_teff', 'e_[Fe/H]', 'e_logg', 'e_Li']
        for c in error_cols:
            if c not in result_df.columns:
                result_df[c] = 0.0  # Set missing error columns to 0.0

        errormap = {
            'teff':       ('e_teff',     'err_prop_teff'),
            '[Fe/H]':     ('e_[Fe/H]',   'err_prop_feh'),
            'logg':       ('e_logg',     'err_prop_logg'),
            'Li_3D_NLTE': ('e_Li',       'err_prop_li'),
        }

        # Initialize output columns with 0
        for feat in errormap:
            result_df[errormap[feat][1]] = 0.0

        # Propagating errors from each parameter:
        for i in range(len(result_df)):
            if not in_bounds.iloc[i]:
                continue # skipping stars with parameters out of bounds

            x_row = result_df[feature_cols].iloc[i].values

            for k in range(len(feature_cols)):
                feat = feature_cols[k]
                err_col, out_col = errormap[feat]

                sigma = result_df[err_col].iloc[i]
                if sigma == 0 or not np.isfinite(sigma):
                    continue # skipping stars with errors = 0 or NaNs

                # bump the input up, predict the age
                x_up = x_row.copy()
                x_up[k] = x_up[k] + sigma
                y_up = float(model.predict(scaler.transform(x_up.reshape(1, -1)))[0])

                # bump the input down, predict the age
                x_down = x_row.copy()
                x_down[k] = x_down[k] - sigma
                y_down = float(model.predict(scaler.transform(x_down.reshape(1, -1)))[0])

                # averaging the difference to get the error contribution from this parameter
                result_df.loc[i, out_col] = abs(y_up - y_down) / 2.0

        # Combining errors:
        per_input_cols = ['err_prop_teff', 'err_prop_feh', 'err_prop_logg', 'err_prop_li']
        sigma_squared_inputs = ((result_df['err_prop_teff'] ** 2) + (result_df['err_prop_feh'] ** 2) + (result_df['err_prop_logg'] ** 2) + (result_df['err_prop_li'] ** 2) + (model_err ** 2))
        sigma_inputs = np.sqrt(sigma_squared_inputs)
        result_df['age_err'] = sigma_inputs

        # Setting errors to NaN for out-of-bounds parameters
        out_cols_to_blank = ['err_prop_teff', 'err_prop_feh', 'err_prop_logg', 'err_prop_li', 'age_err']
        result_df.loc[~in_bounds, out_cols_to_blank] = np.nan
        
    return result_df
