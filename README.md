# Overview

This is a work-in-progress project using persistent Laplacians built from cellular sheaves on simplicial complexes to predict protein-ligand binding energy.

# Data pre-processing

## Description of files

It relies on having pdb files with partial charges. These are obtained using chimeraX scripts contained in ```data/v2007/```. The actual data is not committed to git for data licensing and file size reasons.  There should be a long list of folders ```data/v2007/<pdbid>/```.  The scripts need to be modified to reflect your home directories. The batch script ```chimera.sh``` will use slurm to execute ```chimera.py``` which will read in the pdbids and use chimeraX to execute the script ```chimera_pdbid.cxc```. The other scripts in ```data/v2007/.``` are left over from development and can be ignored. The output from each executation of ```chimera_pdbid.cxc``` is a file ```<pdbid>/<pdbid>_charged.mol2``` with partial charges assigned.

In ```src/readin.py``` there is a short function to read in the mol2 file you just created ```mol2_to_pqre```. Also used for the ligand mol2 files already in the dataset. 

## Instructions for pre-processing

1. Copy the PDBbind2007 dataset into the folder ```data/v2007``` so that we have the structure ```sheafbind/data/v2007/<pdbid>/<pdbid>_protein.pdb``` for all of the different pdbids., 
2. Possibly modify ```chimera_script.py``` in the final line so that the line path is correct for chimeraX (it may not be at this location for different development environments): ```/opt/software-current/2023.06/x86_64/generic/software/ChimeraX/1.9-ubuntu22.04-amd64/bin/ChimeraX```
3. Definitely modify ```chimera.sh``` to have the right paths and outputs for your directory structure.
4. Submit ```sbatch chimera.sh``` and wait for it to run.

# Feature generation

Other than the things explicitly explained below, assume everything is from debugging or experimintation or planned setup for the rest of the project.

In a python virtual environment, run ```pip install -r src/requirements.txt``` (or analogous for conda, but conda might have issues with petls - I haven't tested).

Everything else is mainly in ```sheafbind.ipynb```:

The function ```check_mol2_okay``` is for debugging.

The function ```new_xyzq``` gets protein and ligand coordinates and charges, filters to heavy atoms, and then concatenates them 

The function ```get_rough_diameter``` gets a very rough estimate on the maximum distance between points in the protein-ligand point cloud based on just the bounding box. This will be used to threshold filtration values.

The function ```get_alpha_complex``` turns a point cloud into a 2D alpha complex as a ```simplex_tree``` from ```gudhi```.

The function ```get_extra_data``` extracts the coordinates and charge for each point in the point cloud; this will be used for defining the sheaf.

The function ```my_restriction``` is the sheaf restriction function. It should take a simplex, one of its cofaces, and the ```sheaf_simplex_tree``` from ```petls``` as inputs. It will output a single float value which is the restriction map (a linear transformation from R^1 to R^1, so a scalar). It should only be defined for cofaces up one dimension from the simplex. ***Warning:*** the whole pipeline is numerically unstable because we are trying to compute strange eigenvalues (expected nonzero values around 10^-6, but the numerical algorithms calculate a zero algorithms sometimes also around 10^-6; so how can we possibly tell what is zero and nonzero). Part of my attempt to address this was to multiply in factors of Coulumb's constant (reasonable as the sheaf is supposedly to mimic a coulumb force/potential), but this actually makes it more numerically unstable.

The function ```get_laplacian_complex``` turns the combined protein-ligand coordinates and charges into a ```petls``` ```sheaf_simplex_tree``` and ```PersistentSheafLaplacian```.

The function ```get_selected_spectra_requests``` is building a list of triples ```(dim, a, b)``` that decide which persistent laplacians we will compute. This should be changed as we determine which Laplacians are interesting/useful.

The function ```min_nonzero``` is used to summarize eigenvalue sets. Note that it assumes a tolerance that should be played with to determine the right cutoff, which is exactly what the "***Warning***" above is for.


The function ```pipeline``` takes a pdbid and spits out eigenvalues, and some other things. This is the feature extraction. This function (and the functions it calls) should be modified to determine which persistent Laplacians $\Delta_{dim}^{a,b}$ and eigenvalues we compute. 

Below that function is a bunch of experimentation, and ***Warning:*** these may produce errors and fail to run. Mostly it's Checking out specific Laplacians, trying different eigenvalue algorithms, and plotting eigenvalues. It also has a3d visualization of the alpha complex at varying scales. Plotly is hard to get installed with conflicting sub-dependencies between gudhi, scipy, and plotly in some versions. If you get errors, try running ```pip install anywidget plotly ipywidgets nbformat```, possibly multiple times as the right versions get installed.

Again, all of the other Jupyter notebooks besides ```sheafbind.ipynb``` should be safe to ignore largely because they were failed attempts to get partial charges using software other than chimeraX.

## Usage
It is currently using ```pipeline``` with an example pdbid, but providing the full list of pdbids also works.  For each pdbid, computation time will depend mostly on which persistent laplacians are selected in ```get_selected_spectra_requests```. It's probably not advisable to do more than 10 or 20 different persistent Laplacians until we get to the stage of building a full machine learning model. Each PTL+eigenvalue computation could take anywhere from a few milliseconds to several minutes depending on points in the molecules, dimension of the laplacian, filtration values selected, and how many eigenvalues/the eigenvalue algorithm. To quickly try a faster computation, but possibly ignore **all** of the important information, select smaller starting (the a in (dim,a,b)) filtration values, only dimensions 0 or 1, or only a couple of laplacians.    
