# MARBL Diagnostic Examples

This repository hosts examples of MARBL related diagnostics

## How do I look at the Diagnostics?
There are two options when it come to viewing diagnostics produced by this repository

1. Take a look at the plots rendered [by the JupyterBook](https://marbl-ecosys.github.io/marbl-bgc-diagnostics/02_Plot_Output.html), which is an HTML rendering of the notebook used to create the various plots. You can scroll though that page to find links to specific variables within the notebooks. There is a caveat to this approach however; you will **only be able to view the top level of variables with various vertical dimensions**. If you are interested in looking at other vertical levels, I would suggest taking a look at method 2 (below).
* Click on [this link](https://marbl-ecosys.github.io/marbl-bgc-diagnostics/02_Plot_Output.html) to view available diagnostic plots

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

## What if I want to look at more variables?
Within the `notebooks` directory, there is a config file (`analysis_config.yml`) which includes a list of ocean variables to analyze. You can add more variables to this list (subsitute the variable name in `YOUR_NEW_VARIABLE`)

```
variables:
  - TEMP
  - YOUR_NEW_VARIABLE
```

Once you make adjustments to this config file, go ahead and run through the the notebooks, adding additional plots in the last notebook with the following syntax:

```python
plot_comparison(ds, 'case_to_validate', 'YOUR_NEW_VARIABLE')
```
