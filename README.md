# utility to search CSD based on CCD definition CIF file or MOL/MOL2/SDF file
======

## Contents
--------------------------------------------
```
activate_csd_python_api.sh  # configuration for conda env
data/ # output data folder to be generated upon run
source/  # application code
source/run/searchCsd.py # code for user to run the search 
```

## Installation
--------------------------------------------
```
git clone https://github.com/shaochenghua/py-rcsb-search-csd.git
```
## Run 
```
cd py-rcsb-search-csd
source activate_csd_python_api.sh
cd source/run
python searchCsd.py -h
```

## testing examples and expected output/result
* run test case on GLC ligand, for the default substructure search, using model coordinates
```
python searchCsd.py -i GLC
```
then check data/GLC folder for results in GLC-model-substructure.tsv

* run substructure search using ideal coordinates
```
python searchCsd.py -i GLC -c ideal
```
then check data/GLC folder for results in GLC-ideal-substructure.tsv

* run similarity search
```
python searchCsd.py -i GLC -s similarity
```
then check data/GLC folder for results in GLC-model-similarity.tsv

* run search using existing SDF. Metal ligands may fail the conversion from CIF to MOL/MOL2/SDF, you can use the option -u to use the existing SDF generated for PDB website
```
python searchCsd.py -i SF4 -u
```

* run search on local files of either CIF, or MOL/MOL2/SDF file, assuming you have local file of data/GLC/GLC.cif
```
python searchCsd.py -l ../../data/GLC/GLC.cif
``` 
The filepath can be either relative path like the one above, or absolute path. The results will still be written into the data folder. 