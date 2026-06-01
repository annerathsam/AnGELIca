from setuptools import setup

setup(name='AnGELIca',
    version='0.1.0',    
    description='Script to estimate ages for FGK stars based on their 3D NLTE lithium abundances, effective temperatures and [Fe/H].',
    url='https://github.com/annerathsam/lithium_chronos',
    author='Anne Rathsam',
    author_email='annerathsam@usp.br',
    license='MIT',
    packages=['lithium_chronos'],
    install_requires=['numpy', 'pandas'])
