*AnGELIca* package
---------------
*AnGELIca* is a tool to estimate ages for FGK stars based on empirical relations between Li abundance, age, [Fe/H], and effective temperature from `Rathsam et al. (202X) <link>`_. Valid for stars with -0.3 dex <= [Fe/H] <= +0.4 dex and 5400 K <= Teff <= 6500 K.


Installation
------------
To install *AnGELIca*, run::

    pip install git+https://github.com/annerathsam/AnGELIca.git


Dependencies
------------
The dependencies of *AnGELIca* are `pandas <https://pandas.pydata.org/>`_ and `NumPy <https://numpy.org/>`_. 
These are installed using pip::

    pip install pandas numpy
  
  
Example usage
-------------

.. code-block:: python

    # Estimating an age for a single star (errors are not required, but are accounted for in the reported uncertainty):
    teff, e_teff = 5977, 10 # in K
    feh, e_feh = 0.00, 0.05 # in dex
    li, e_li = 1.46, 0.05 # 3D NLTE lithium abundance in dex

    result = AnGELIca.age_interp(feh, teff, li, f='gompertz', err_feh=e_feh, err_teff=e_teff, err_li=e_li)

    age = result[0,0]
    std = result[0,1]

    print(f"Estimated age: {age:.3f} +/- {std:.3f} Gyr")

    # Estimating ages from a sample of stars:

    # Assuming an input table "sample.csv" with columns "id" for star identification, 
    # "[Fe/H]" for metallicity (in dex), "teff" for effective temperature (in K), 
    # "Li_3D_NLTE" for the 3D NLTE A(Li) (in dex), and e_X for errors 

    data = pd.read_csv("sample.csv") 

    feh = np.array(data["[Fe/H]"])
    teff = np.array(data["teff"])
    li = np.array(data["Li_3D_NLTE"])

    e_feh = np.array(data["e_[Fe/H]"])
    e_teff = np.array(data["e_teff"])
    e_li = np.array(data["e_Li_3D_NLTE"])

    results = AnGELIca.age_interp(feh, teff, li, err_feh=e_feh, err_teff=e_teff, err_li=e_li)
    calc_ages = results[:,0]
    std_ages = results[:,1]

    # To check the ages:
    
    for star, age, std_age, in zip(data["id"], calc_ages, std_ages):
         print(f"{star}: {age:.3f} +/- {std_age:.3f} Gyr")

    # Saving to a file "output.csv":

    data['Age'] = calc_ages.round(3)
    data['Age_error'] = std_ages.round(3)

    data.to_csv('sample_ages.csv', index=False)

    # 'nan' values appear when the input parameters were out bounds.
  
  
Contact
------------
For questions or suggestions, please contact me at annerathsam@usp.br or by opening an issue on GitHub.


Author
------
- `Anne Rathsam <https://annerathsam.github.io/>`_


Preferred citation
------------------
Please cite `Rathsam et al. (202X, etc) <link>`_ if you use this code in your research. The BibTeX entry for the paper is:

.. code:: bibtex

    @ARTICLE{
    }


License & attribution
---------------------

Copyright 2026, Anne Viegas Rathsam.

The source code is made available under the terms of the MIT license.

If you make use of this code, please cite this package and its dependencies.


Acknowledgements
---------------------
Special thanks to Miguel de Loreto Neto for helping to choose the code name.
