import xarray as xr
import holoviews as hv
import matplotlib.colors as colors
import holoviews as hv
import geoviews as gv
import datashader
from holoviews.operation.datashader import regrid, shade, datashade, rasterize
import matplotlib.pyplot as plt
import panel as pn
import numpy as np
from config import analysis_config


def plot_interactive(ds, variable, cmap='magma', vmin=None, vmax=None):
    """Plots an interactive plot using holoviews"""
    da = ds[variable]
    da['nlon'] = ds.nlon
    da['nlat'] = ds.nlat
    da = da.drop_vars(['TLAT', 'TLONG', 'ULAT', 'ULONG'])
    
    hvds = hv.Dataset(da, kdims=list(da.dims))
        
    quadmesh = hvds.to(hv.QuadMesh, kdims=["nlon", "nlat"])
    if vmin:
        levels = list(np.linspace(vmin, vmax, 20))
        cmap = create_cmap(levels)
        datashade_obj = rasterize(quadmesh, precompute=True).opts(colorbar=True, width=600, height=400, cmap=cmap, tools=['hover'], color_levels=levels, bgcolor='lightgray')
    else:
        datashade_obj = rasterize(quadmesh, precompute=True, cmap=plt.cm.RdBu_r).opts(colorbar=True, width=600, height=400, cmap=cmap, tools=['hover'])
    return datashade_obj.relabel(f'{ds.title}')

def plot_comparison(ds, case_to_compare, variable, baseline = analysis_config['reference_case_name'], first_case=False):
    """Plot a comparison between cases"""
    
    ds2 = ds.sel(case=baseline)
    ds2.attrs['title'] = baseline
    baseline_plot = plot_interactive(ds2, variable)
    
    ds1 = ds.sel(case=case_to_compare)
    ds1.attrs['title'] = case_to_compare
    case_compare_plot = plot_interactive(ds1, variable)
    
    diff = ds1[[variable]] - ds2[[variable]]
    diff.attrs['title'] = f'{case_to_compare} - {baseline}'
    diff[variable].attrs['units'] = ds[variable].units
    max_diff = abs(np.nanmax(diff[variable].values))
    min_diff = abs(np.nanmin(diff[variable].values))
    max_diff = np.max(np.array(max_diff, min_diff))
    difference_plot = plot_interactive(diff, variable, cmap='seismic', vmin=-max_diff, vmax=max_diff)
    
    diff_percent = (diff/ds1[[variable]].max()) * 100
    diff_percent.attrs['title'] = f'Percent Difference'
    diff_percent[variable].attrs['units'] = 'Percent'
    max_diff = abs(np.nanmax(diff_percent[variable].values))
    min_diff = abs(np.nanmin(diff_percent[variable].values))
    max_diff = np.max(np.array(max_diff, min_diff))
    difference_plot_percent = plot_interactive(diff_percent, variable, cmap='seismic', vmin=-max_diff, vmax=max_diff)
    
    plots = hv.Layout([case_compare_plot + baseline_plot + difference_plot + difference_plot_percent]).cols(2)
    out_title = f"### {case_to_compare} vs. {baseline} \n **Units: {ds1[variable].units}**"
    if first_case:
        out_title = f'## {ds1[variable].long_name} ({variable}) \n{out_title}'
    panel = pn.Column(pn.pane.Markdown(out_title, align="start"), plots)
    return panel

def create_cmap(levs):
    assert len(levs) % 2 == 0, 'N levels must be even.'
    return colors.LinearSegmentedColormap.from_list(name='red_white_blue', 
                                                     colors =[(0, 0, 1), 
                                                          (1, 1., 1), 
                                                          (1, 0, 0)],
                                                     N=len(levs)-1,
                                                    )

def plot_variable(ds, variable):
    plots = []
    for case in analysis_config['compare_case_name']:
        plots.append(plot_comparison(ds, case, variable))
        
    out = pn.Column()
    for plot in plots:
        out+=plot
    return out
    