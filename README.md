# MARBL Diagnostic Examples

This repository hosts examples of MARBL related diagnostics

## How do I look at the Diagnostics?
There are two options when it come to viewing diagnostics produced by this repository

1. Take a look at the plots rendered [by the JupyterBook](https://marbl-ecosys.github.io/marbl-bgc-diagnostics/intro.html), which is an HTML rendering of the notebook used to create the various plots. You can scroll though that page to find links to specific variables within the notebooks. There is a caveat to this approach however; you will **only be able to view the top level of variables with various vertical dimensions**. If you are interested in looking at other vertical levels, I would suggest taking a look at method 2 (below).

2. Run these notebooks on Casper/Cheyenne. This option allows you choose different vertical levels for 3 dimensional variables. You will need to follow the steps below:
- Clone this repository
```bash
git clone https://github.com/marbl-ecosys/marbl-bgc-diagnostics.git
```
- Install and activate the conda environment

```bash
conda env create -f envs/environment.yml
conda activate bgc-diagnostics-dev
```
- Run the notebooks
  - Access these notebooks interactively using the [JupyterHub](https://jupyterhub.hpc.ucar.edu/) or by using [Jupyter-Forward](https://github.com/NCAR/jupyter-forward), using the conda environment you created `bgc-diagnostics-dev`
    * It is recommoned that run the following notebooks **first**:
      * `00_Build_Catalog.ipynb`
      * `01_Compute_20yr_mean.ipynb`
      * `intro.ipynb`
  - Once you run those two notebooks, ssh onto Casper/Cheyenne, activate your environment, and run the following from the project root directory
  ```
  python notebooks/generate_plotting_notebooks.py
  ```
  This script will generate plotting notebooks using the `interactive_plot_template.ipynb` notebook with the syntax (`{plot realm (biogeochemistry or physics)}_{variable}.ipynb`)

  Once you run this, you will see all the new notebooks! At this point, you can build the book locally by using 
  
  ```bash
  jupyter-book build notebooks
  ```
  
  Or, feel free to investigate the fields from the [JupyterHub](https://jupyterhub.hpc.ucar.edu/)!


## What if I want to look at more variables?
Within the `notebooks` directory, there is a config file (`analysis_config.yml`) which includes a list of ocean variables to analyze. You can add more variables to this list (subsitute the variable name in `YOUR_NEW_VARIABLE`)

```yaml
variables:
  - TEMP
  - YOUR_NEW_VARIABLE
```

Once you make adjustments to this config file, go ahead and run through the the notebooks!

## What if I want to look at a different case?
In that same `analysis_config.yml` file, you will see the following block:

```yaml
reference_case_name: b1850.f19_g17.validation_mct.004

compare_case_name:
    - b1850.f19_g17.validation_mct.002
    - b1850.f19_g17.validation_nuopc.004

case_data_paths:
     - /glade/scratch/hannay/archive/b1850.f19_g17.validation_mct.004/ocn/hist
     - /glade/scratch/hannay/archive/b1850.f19_g17.validation_mct.002/ocn/hist
     - /glade/scratch/hannay/archive/b1850.f19_g17.validation_nuopc.004_copy2/ocn/hist
```

Where the casenames (`reference_case_name` and `compare_case_name`) are the cases you are looking to compare, and the `case_data_paths` are which directories to use when building the [`intake-esm catalog`](https://intake-esm.readthedocs.io/en/latest/) using [`ecgtools`](https://ecgtools.readthedocs.io/en/latest/)!

## Where is the Catalog Saved to?

The data catalog (generated in the `00_Build_Catalog.ipynb` notebook) is output to the respective csv/json specified in the `analysis_config.yml` file (default is the `/data` directory), as shown below:

```yaml
catalog_csv: ../data/cesm-validation-catalog.csv
    
catalog_json: ../data/cesm-validation-catalog.json
```

