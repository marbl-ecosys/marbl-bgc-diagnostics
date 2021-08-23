import xarray as xr
import holoviews as hv

import holoviews as hv
import geoviews as gv
import datashader
from holoviews.operation.datashader import regrid, shade, datashade, rasterize
import matplotlib.pyplot as plt
import panel as pn

def plot_interactive(ds, variable, cmap='magma'):
    """Plots an interactive plot using holoviews"""
    da = ds[variable]
    da['nlon'] = ds.nlon
    da['nlat'] = ds.nlat
    da = da.drop_vars(['TLAT', 'TLONG', 'ULAT', 'ULONG'])
    
    hvds = hv.Dataset(da, kdims=list(da.dims))
        
    quadmesh = hvds.to(hv.QuadMesh, kdims=["nlon", "nlat"])
    datashade_obj = rasterize(quadmesh, precompute=True, cmap=plt.cm.RdBu_r).opts(colorbar=True, width=600, height=400, cmap=cmap, tools=['hover'])
    return datashade_obj.relabel(f'{ds.title}')

def plot_comparison(ds, case_to_compare, variable, baseline = 'b1850.f19_g17.validation_mct.004'):
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
    difference_plot = plot_interactive(diff, variable, cmap='seismic')
    
    diff_percent = (diff/ds1[[variable]].max()) * 100
    diff_percent.attrs['title'] = f'Percent Difference'
    diff_percent[variable].attrs['units'] = 'Percent'
    difference_plot_percent = plot_interactive(diff_percent, variable, cmap='seismic')
    
    plots = hv.Layout([case_compare_plot + baseline_plot + difference_plot + difference_plot_percent]).cols(2)
    panel = pn.Column(pn.pane.Markdown(f"## {ds1[variable].long_name} {ds1[variable].units}", align="center"), plots)
    return panel