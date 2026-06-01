# -*- coding: utf-8 -*-

'''
A script to estimate ages for FGK stars based on empirical relations between Li abundance, age, [Fe/H], and effective temperature from Rathsam et al. (2026?).
'''

import numpy as np
import pandas as pd

def age_li_st(li):
  '''Calculates the age as a function of 3D NLTE A(Li) for solar twins.
  '''
  age = (li - 2.59) / (-0.256)
  return age

def gompertz(A, x):
  g = A[0] + (A[1] - A[0]) * np.exp(-np.exp(-A[2] * (x - A[3])))
  return g

def linear(A, x):
  f = A[0]*x + A[1]
  return f

def quadratic(A, x):
  f = A[0] * x**2 + A[1] * x + A[2]
  return f

# Gompertz function parameters, per [Fe/H] interval
a25n_g = np.array([8.88489675e-01, 1.53356161e+00, -1.84102789e-01, 5.82486933e+03])  # -0.3 to -0.2 dex
a15n_g = np.array([-7.85562473e-02, 1.05145237e+00, 1.03782054e-02, 5.82638480e+03])  # -0.2 to -0.1 dex
a05n_g = np.array([-1.06750151e-01, 7.84673015e-01, 6.39877062e-02, 5.88667279e+03])  # -0.1 to +0.0 dex
a05p_g = np.array([-4.07334833e-01, 7.21628357e-01, 1.76690304e-02, 5.83639800e+03])  # +0.0 to +0.1 dex 
a15p_g = np.array([-3.36058396e-01, 6.43721859e-01, 2.29380034e-01, 5.90451253e+03])  # +0.1 to +0.2 dex
a25p_g = np.array([-5.18125047e-01, 6.39822797e-01, 4.98455252e-01, 5.87676390e+03])  # +0.2 to +0.3 dex
a35p_g = np.array([7.47638308e-01, -1.49246493e-01, -9.58512140e-02, 5.86513979e+03]) # +0.3 to +0.4 dex

a_g = np.array([a25n_g, a15n_g, a05n_g, a05p_g, a15p_g, a25p_g, a35p_g])

# Gompertz covariance matrices, per [Fe/H] interval
c25n_g = np.array([
   [1.93861444e-04, -3.58544795e-07, -7.35711532e-04, -7.53430824e-03],
   [-3.58544795e-07, 3.60031051e-03, 6.49030206e-04, -3.48522455e-02],
   [-7.35711532e-04, 6.49030206e-04, 1.01333238e-01, -7.39994308e-01],
   [-7.53430824e-03, -3.48522455e-02, -7.39994308e-01, 6.33562290e+01]]) * (70.21701868995953) # -0.3 to -0.2 dex
c15n_g = np.array([
   [2.08419596e-04, -4.21905299e-05, 2.82816121e-06, 3.21895008e-02],
   [-4.21905299e-05, 2.04457481e-04, -5.70577258e-06, 1.86579636e-02],
   [2.82816121e-06, -5.70577258e-06, 2.48734944e-07, -2.16953647e-04],
   [3.21895008e-02, 1.86579636e-02, -2.16953647e-04, 1.17335867e+01]]) * (159.34707213537084) # -0.2 to -0.1 dex
c05n_g = np.array([
   [1.63307322e-05, -2.00032752e-07, 1.43578271e-06, 6.30448246e-04],
   [-2.00032752e-07, 2.60397111e-05, -1.37615398e-05, 4.62324079e-04],
   [1.43578271e-06, -1.37615398e-05, 7.02636956e-05, 2.27091293e-03],
   [6.30448246e-04, 4.62324079e-04, 2.27091293e-03, 2.28545315e+00]]) * (161.4142142386056)  # -0.1 to +0.0 dex
c05p_g = np.array([
   [5.49737510e-05, -3.60256436e-06, 7.70149970e-07, 5.23013206e-03],
   [-3.60256436e-06, 3.15801594e-05, -2.41264616e-06, 7.62855706e-04],
   [7.70149970e-07, -2.41264616e-06, 3.29787561e-07, 1.75076821e-04],
   [5.23013206e-03, 7.62855706e-04, 1.75076821e-04, 1.86131249e+00]]) * (113.40220851254088) # +0.0 to +0.1 dex
c15p_g = np.array([
   [3.22511016e-05, -2.23525403e-08, 2.75250334e-06, 2.90762886e-04],
   [-2.23525403e-08, 2.04527034e-05, -9.70829327e-05, -5.21925813e-04],
   [2.75250334e-06, -9.70829327e-05, 5.89825464e-03, 1.11157818e-01],
   [2.90762886e-04, -5.21925813e-04, 1.11157818e-01, 7.17088844e+00]]) * (232.78089550794257) # +0.1 to +0.2 dex
c25p_g = np.array([
   [2.57331775e-04, -3.31318754e-07, 1.52098953e-04, 1.54339299e-03],
   [-3.31318754e-07, 3.84982213e-05, -3.85339401e-04, -4.75604302e-04],
   [1.52098953e-04, -3.85339401e-04, 1.30699336e-01, 4.13715491e-01],
   [1.54339299e-03, -4.75604302e-04, 4.13715491e-01, 5.02447080e+00]]) * (43.34287573690795) # +0.2 to +0.3 dex
c35p_g = np.array([
   [6.06358576e-05, -6.62279668e-09, 1.02758383e-04, 1.78152302e-02],
   [-6.62279668e-09, 5.34053908e-04, -7.71527174e-05, 1.56936360e-02],
   [ 1.02758383e-04, -7.71527174e-05, 1.48952803e-03, 2.01830711e-01],
   [ 1.78152302e-02, 1.56936360e-02, 2.01830711e-01, 4.25208580e+01]]) * (101.30672320508826) # +0.3 to +0.4 dex

c_g = np.array([c25n_g, c15n_g, c05n_g, c05p_g, c15p_g, c25p_g, c35p_g])

# Linear function parameters, per [Fe/H] interval
a25n_l = np.array([-7.40279038e-04, 5.47517505e+00]) # -0.3 to -0.2 dex
a15n_l = np.array([2.40717213e-03, -1.36967328e+01]) # -0.2 to -0.1 dex
a05n_l = np.array([2.81197416e-03, -1.62685608e+01]) # -0.1 to +0.0 dex
a05p_l = np.array([2.72549144e-03, -1.58213098e+01]) # +0.0 to +0.1 dex
a15p_l = np.array([3.73368993e-03, -2.17833252e+01]) # +0.1 to +0.2 dex
a25p_l = np.array([4.05897189e-03, -2.37434465e+01]) # +0.2 to +0.3 dex
a35p_l = np.array([2.12091257e-03, -1.21643420e+01]) # +0.3 to +0.4 dex

a_l = np.array([a25n_l, a15n_l, a05n_l, a05p_l, a15p_l, a25p_l, a35p_l])

# Linear covariance matrices, per [Fe/H] interval
c25n_l = np.array([
   [3.11798297e-09, -1.88332627e-05],
   [-1.88332627e-05, 1.13889096e-01]]) * (59.14521302740383)  # -0.3 to -0.2 dex
c15n_l = np.array([
   [9.72287831e-10, -5.68499652e-06],
   [-5.68499652e-06, 3.32639113e-02]]) * (156.63996073939896) # -0.2 to -0.1 dex
c05n_l = np.array([
   [7.32040603e-10, -4.28694789e-06],
   [-4.28694789e-06, 2.51182198e-02]]) * (157.64989469049345) # -0.1 to +0.0 dex
c05p_l = np.array([
   [4.15523739e-10, -2.44808185e-06],
   [-2.44808185e-06, 1.44313865e-02]]) * (158.66342465455747) # +0.0 to +0.1 dex
c15p_l = np.array([
   [1.23031419e-09, -7.23202377e-06],
   [-7.23202377e-06, 4.25338038e-02]]) * (301.11389360962323) # +0.1 to +0.2 dex
c25p_l = np.array([
   [5.15412332e-09, -3.05313652e-05],
   [-3.05313652e-05, 1.80908077e-01]]) * (63.24255194168592)  # +0.2 to +0.3 dex
c35p_l = np.array([
   [3.04790456e-09, -1.82679600e-05],
   [-1.82679600e-05, 1.09556388e-01]]) * (182.20482737778119) # +0.3 to +0.4 dex

c_l = np.array([c25n_l, c15n_l, c05n_l, c05p_l, c15p_l, c25p_l, c35p_l])

# Quadratic function parameters, per [Fe/H] interval
a25n_q = np.array([-8.64172332e-06, 1.04129108e-01, -3.12364520e+02]) # -0.3 to -0.2 dex
a15n_q = np.array([-2.71524044e-06, 3.42528817e-02, -1.06976453e+02]) # -0.2 to -0.1 dex 
a05n_q = np.array([1.72892609e-06, -1.74818898e-02, 4.32499197e+01])  # -0.1 to +0.0 dex
a05p_q = np.array([3.79101599e-06, -4.13860732e-02, 1.12408437e+02])  # +0.0 to +0.1 dex
a15p_q = np.array([-7.78237036e-06, 9.53706173e-02, -2.91358546e+02]) # +0.1 to +0.2 dex
a25p_q = np.array([-8.28294847e-06, 1.01554126e-01, -3.10511467e+02]) # +0.2 to +0.3 dex
a35p_q = np.array([-3.36622007e-06, 4.18579428e-02, -1.29319643e+02]) # +0.3 to +0.4 dex

a_q = np.array([a25n_q, a15n_q, a05n_q, a05p_q, a15p_q, a25p_q, a35p_q])

# Quadratic covariance matrices, per [Fe/H] interval

c25n_q = np.array([
   [6.77241450e-13, -8.17727691e-09, 2.46644945e-05],
   [-8.17727691e-09, 9.87449554e-05, -2.97864680e-01],
   [ 2.46644945e-05, -2.97864680e-01, 8.98593624e+02]]) * (55.51118974106998) # -0.3 to -0.2 dex
c15n_q = np.array([
   [5.11387630e-15, -6.10193154e-11, 1.81812891e-07],
   [-6.10193154e-11, 7.28674349e-07, -2.17286429e-03],
   [1.81812891e-07, -2.17286429e-03, 6.48436270e+00]]) * (181.68072116645627) # -0.2 to -0.1 dex
c05n_q = np.array([
   [2.51769149e-14, -2.94714171e-10, 8.62053782e-07],
   [-2.94714171e-10, 3.45066872e-06, -1.00957805e-02],
   [8.62053782e-07, -1.00957805e-02, 2.95446950e+01]]) * (158.5384476068211)  # -0.1 to +0.0 dex
c05p_q = np.array([
   [1.06773441e-14, -1.23801348e-10, 3.58627190e-07],
   [-1.23801348e-10, 1.43601227e-06, -4.16150388e-03],
   [3.58627190e-07, -4.16150388e-03, 1.20648176e+01]]) * (144.14296543583842) # +0.0 to +0.1 dex
c15p_q = np.array([
   [1.81368240e-14, -2.16448027e-10, 6.45377885e-07],
   [-2.16448027e-10, 2.58407067e-06, -7.70764709e-03],
   [6.45377885e-07,-7.70764709e-03, 2.29982690e+01]]) * (290.4548095472675)  # +0.1 to +0.2 dex
c25p_q = np.array([
   [7.62489548e-14, -9.11295240e-10, 2.72168488e-06],
   [-9.11295240e-10, 1.08936544e-05, -3.25418170e-02],
   [2.72168488e-06, -3.25418170e-02, 9.72298852e+01]]) * (59.95233649421226)  # +0.2 to +0.3 dex
c35p_q = np.array([
   [6.58400894e-14, -7.85344755e-10, 2.34021016e-06],
   [-7.85344755e-10, 9.36994394e-06, -2.79280693e-02],
   [2.34021016e-06, -2.79280693e-02, 8.32639865e+01]]) * (190.65169497593132) # +0.3 to +0.4 dex

c_q = np.array([c25n_q, c15n_q, c05n_q, c05p_q, c15p_q, c25p_q, c35p_q])

pars = {
    gompertz: {"beta": a_g, "cov": c_g},
    linear: {"beta": a_l, "cov": c_l},
    quadratic: {"beta": a_q, "cov": c_q}
}

feh_vec = np.array([-0.25, -0.15, -0.05, 0.05, 0.15, 0.25, 0.35])

def interp(x, x0, x1, f, a0, a1, t):
  ''' Interpolation function.
  x = Interpolated value ([Fe/H])
  x0 = initial [Fe/H]
  x1 = final [Fe/H]
  f = interpolated function
  a0 = function parameters for x0
  a1 = function parameters for x1
  t = effective temperature
  '''
  alpha = (x - x0)/(x1 - x0)

  y0 = f(a0, t)
  y1 = f(a1, t)

  fi = ((1 - alpha)*y0) + (alpha*y1)
  return fi

def age_interp(feh, teff, li, f="gompertz", feh_vec=feh_vec, a=None, c=None, err_feh=0.0, err_teff=0.0, err_li=0.0):
  ''' Function that determines stellar ages based on [Fe/H], effective temperature, and
  3D NLTE A(Li). The interp() and age_li_st() functions are also used.
  The residuals function to be interpolated can be chosen among Gompertz function (default, 'gompertz')
  'linear', or 'quadratic'.
  '''

  f_map = {"gompertz": gompertz, "linear": linear, "quadratic": quadratic}

  if not isinstance(f, str):
    raise TypeError("f must be a string: 'linear', 'quadratic' or 'gompertz (default)'")

  f_lower = f.lower()
  if f_lower not in f_map:
      raise ValueError(f"f must be one of {list(f_map.keys())}")

  f = f_map[f_lower]

  p = pars.get(f)
  a = p["beta"]
  c = p["cov"]

  feh = np.atleast_1d(feh)
  teff = np.atleast_1d(teff)
  li = np.atleast_1d(li)
  err_feh = np.atleast_1d(err_feh)
  err_teff = np.atleast_1d(err_teff)
  err_li = np.atleast_1d(err_li)

  results = []

  for feh_i, teff_i, li_i, err_feh_i, err_teff_i, err_li_i in zip(feh, teff, li, err_feh, err_teff, err_li):
      # Checking whether the parameters are within the bounds:
      if feh_i < -0.3 or feh_i > 0.4 or teff_i < 5400 or teff_i > 6500:
          results.append([np.nan, np.nan])

      else:
          n = 500 
          ages = []

          for i in range(n):
             feh_s  = np.random.normal(feh_i, err_feh_i)
             teff_s = np.random.normal(teff_i, err_teff_i)
             li_s   = np.random.normal(li_i, err_li_i)

             idx1 = np.searchsorted(feh_vec, feh_s)
             if idx1 == 0:
                 idx0, idx1 = 0, 1
             elif idx1 == len(feh_vec):
                 idx0, idx1 = len(feh_vec) - 2, len(feh_vec) - 1
             else:
                  idx0, idx1 = idx1 - 1, idx1

             x0, x1 = feh_vec[idx0], feh_vec[idx1]
             a0, a1 = a[idx0], a[idx1]
             c0, c1 = c[idx0], c[idx1]
             a0_s = np.random.multivariate_normal(a0, c0)
             a1_s = np.random.multivariate_normal(a1, c1)

             res = interp(feh_i, x0, x1, f, a0_s, a1_s, teff_s)

             li_input = li_s - res
             age_i = age_li_st(li_input)
             ages.append(age_i)

          results.append([np.mean(ages), np.std(ages)])

  return np.array(results)
