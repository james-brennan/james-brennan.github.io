import datashader as ds
from datashader import transfer_functions as tf 
from datashader import utils
from colorcet import palette


import xarray as xr
da = xr.open_rasterio("LAI.tif")

da = da.compute()



da = da.where(da < 150.)


cmap = palette['kgy']

bg_col = 'black'
ys, xs = int(da.shape[1]*0.02), int(da.shape[2]*0.02)
agg =  ds.Canvas(plot_width=xs, plot_height=ys).raster(da[0], downsample_method='mean')
img = tf.shade(agg, cmap=cmap)
img = tf.set_background(img, bg_col)
utils.export_image(img=img, filename='lai', fmt=".png", background=None)



da = da.where(da < 150.)


agg =  ds.Canvas(plot_width=xs, plot_height=ys).raster(da[0], downsample_method='mean')
img = tf.shade(agg, cmap=cmap)
img = tf.set_background(img, bg_col)
utils.export_image(img=img, filename='lai2', fmt=".png", background=None)



africa = da[0, 10000:30000, 35000:55000]
ys, xs = int(africa.shape[0]*0.05), int(africa.shape[1]*0.05)
agg =  ds.Canvas(plot_width=xs, plot_height=ys).raster(africa, downsample_method='mean')
img = tf.shade(agg, cmap=cmap)
img = tf.set_background(img, bg_col)
utils.export_image(img=img, filename='lai_africa', fmt=".png", background=None)


africa_zm = da[0, 15500:18500, 48000:51000]
ys, xs = int(africa_zm.shape[0]*0.5), int(africa_zm.shape[1]*0.5)
agg =  ds.Canvas(plot_width=xs, plot_height=ys).raster(africa_zm, downsample_method='mean')
img = tf.shade(agg, cmap=cmap)
img = tf.set_background(img, bg_col)
utils.export_image(img=img, filename='lai_africa_zoom', fmt=".png", background=None)





"""
datashader 2nd post
"""
import datashader as ds
import dask.dataframe as dd
import pandas as pd 
from dask import delayed
import rasterio 
from pathlib import Path
import datashader as ds
from datashader import transfer_functions as tf 
from datashader import utils
from colorcet import palette
