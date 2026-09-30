*AnGELIca* package
---------------
*AnGELIca* is a tool to estimate ages for FGK stars based on empirical relations between Li abundance, age, [Fe/H], and effective temperature from Rathsam et al. (in prep). Valid for stars in the solar vicinity with -0.3 dex <= [Fe/H] <= +0.4 dex, 4.0 dex <= logg <= 4.6 dex, and 5400 K <= Teff <= 6500 K.


Installation
------------
To install *AnGELIca*, run::

    pip install git+https://github.com/annerathsam/AnGELIca.git


Dependencies
------------
The dependencies of *AnGELIca* are `pandas <https://pandas.pydata.org/>`_, `NumPy <https://numpy.org/>`_, and `joblib <https://pypi.org/project/joblib/>`_. 
These are installed using pip::

    pip install pandas numpy joblib
  
  
Example usage
-------------

.. code-block:: python

    # Estimating ages for a sample of stars:

    # The code expects an input table with columns "[Fe/H]" for metallicity (in dex),
    # "teff" for effective temperature (in K), "logg" for log of the surface gravity (in dex),
    # "Li_3D_NLTE" for the 3D NLTE A(Li) (in dex), and "e_[Fe/H]", "e_teff", "e_logg",
    # and "e_Li" for errors.

    import pandas as pd
    import AnGELIca

    data = pd.read_csv("sample.csv") 

    results = AnGELIca.age_predict(data)

    # age_predict estimates errors by default
    # New columns on the dataset: age, err_prop_teff, err_prop_feh, err_prop_logg, err_prop_li, age_err
    # err_prop_X is the error propagated from each parameter
    # age_err is the error on the age estimate, including every propagated error + intrinsic error from the model
    # (taken as the standard deviation of the residuals of the fit)

    # If you do not want to estimate errors, age_predict also accepts errors=False, and return "age" as the only new column

    # Saving the results:
    results.to_csv('sample_ages.csv', index=False)

    # 'nan' values appear when the input parameters were out bounds.  
  
Contact
------------
For questions or suggestions, please contact me at annerathsam@usp.br or by opening an issue on GitHub.


Author
------
- `Anne Rathsam <https://annerathsam.github.io/>`_


Preferred citation
------------------
A paper describing the fits adopted in the code is currently in preparation. For the time being, if you use this code in your research, please cite our previous works on the dataset. The BibTeX entries for the papers are:

.. code:: bibtex

    @ARTICLE{2019MNRAS.485.4052C,
       author = {{Carlos}, M. and {Mel{\'e}ndez}, J. and {Spina}, L. and {dos Santos}, L.~A. and {Bedell}, M. and {Ramirez}, I. and {Asplund}, M. and {Bean}, J.~L. and {Yong}, D. and {Yana Galarza}, J. and {Alves-Brito}, A.},
       title = "{The Li-age correlation: the Sun is unusually Li deficient for its age}",
       journal = {\mnras},
       keywords = {techniques: spectroscopic, Sun: abundances, stars: abundances, stars: evolution, planetary systems, stars: solar-type, Astrophysics - Solar and Stellar Astrophysics},
       year = 2019,
       month = may,
       volume = {485},
       number = {3},
       pages = {4052-4059},
       doi = {10.1093/mnras/stz681},
       archivePrefix = {arXiv},
       eprint = {1903.02735},
       primaryClass = {astro-ph.SR},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2019MNRAS.485.4052C},
       adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

    @ARTICLE{2023MNRAS.522.3217M,
       author = {{Martos}, Giulia and {Mel{\'e}ndez}, Jorge and {Rathsam}, Anne and {Carvalho Silva}, Gabriela},
       title = "{Metallicity and age effects on lithium depletion in solar analogues}",
       journal = {\mnras},
       keywords = {stars: abundances, stars: evolution, stars: solar-type, techniques: spectroscopic, Astrophysics - Solar and Stellar Astrophysics, Astrophysics - Earth and Planetary Astrophysics},
       year = 2023,
       month = jul,
       volume = {522},
       number = {3},
       pages = {3217-3226},
       doi = {10.1093/mnras/stad1177},
       archivePrefix = {arXiv},
       eprint = {2305.01861},
       primaryClass = {astro-ph.SR},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2023MNRAS.522.3217M},
       adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

    @ARTICLE{2023MNRAS.525.4642R,
       author = {{Rathsam}, Anne and {Mel{\'e}ndez}, Jorge and {Carvalho Silva}, Gabriela},
       title = "{Lithium depletion in solar analogs: age and mass effects}",
       journal = {\mnras},
       keywords = {techniques: spectroscopic, stars: abundances, stars: evolution, stars: low-mass, planetary systems, stars: solar-type, Astrophysics - Solar and Stellar Astrophysics},
       year = 2023,
       month = nov,
       volume = {525},
       number = {3},
       pages = {4642-4656},
       doi = {10.1093/mnras/stad2589},
       archivePrefix = {arXiv},
       eprint = {2309.00471},
       primaryClass = {astro-ph.SR},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2023MNRAS.525.4642R},
       adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }


License & attribution
---------------------

Copyright 2026, Anne Viegas Rathsam.

The source code is made available under the terms of the MIT license.

If you make use of this code, please cite this package and its dependencies.


Acknowledgements
---------------------
Special thanks to Miguel de Loreto Neto for helping to choose the code name.
