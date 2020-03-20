import datashader as ds
from datashader import transfer_functions as tf 
from datashader import utils
from colorcet import palette
import xarray as xr
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


@delayed
def process_tile(the_file):
    """
    Load FRP data and fire locations from a file
    """
    elems = the_file.name.split(".") 
    tile = elems[2] 
    date = datetime.datetime.strptime(elems[1][1:], "%Y%j")
    year, month = date.year, date.month
    doy = int(date.strftime("%j"))
    # tmplate for accessing the subdataset
    tmpl = f'HDF4_EOS:EOS_GRID:"{the_file}":MODIS_Grid_Daily_Fire:MaxFRP'
    with rasterio.open(tmpl) as src:
        arr = src.read()
        it, iy, ix = np.where(arr>0)
        xgeo, ygeo = rasterio.transform.xy(src.transform, iy,ix ) 
        doys = doy + it
        frp = arr[it, iy, ix]
    # put it into a dask dataframe
    df = pd.DataFrame(data= np.stack([doys, xgeo, ygeo, frp]).T, columns=['doy', 'x', 'y', 'frp'])   
    return df


cd /work/scratch-nompiio/jbrennan01/data/modis/mod14/MOD14A1/2002/


ffiles = Path(".").rglob("*.hdf")
#files_ = list(ffiles)
delayed_dfs = []

# So we've not actually done any file loading or computation yet
for f in ffiles:
    print(f)
    delayed_dfs.append(  process_tile(f)   )

meta = dd.utils.make_meta([('doy', 'f8'), ('x', 'f8'), ('y', 'f8'), ('frp', 'f8')])
dask_dataframe = dd.from_delayed(delayed_dfs, meta=meta)

print(dask_dataframe)


from dask import distributed
import multiprocessing as mp

pd.options.mode.chained_assignment = None

NWORKERS  = 12
cluster = distributed.LocalCluster(n_workers=NWORKERS,threads_per_worker=1, memory_limit=1.5e+10)
dask_client = distributed.Client(cluster)


x = dask_dataframe.compute()


cmap = palette['fire']
bg_col = 'black'
ys, xs = 1800, 3600
cvs =  ds.Canvas(plot_width=xs, plot_height=ys)
points = cvs.points(x, 'x', 'y', ds.mean('frp'))
img = tf.shade(points, cmap=cmap)
img = tf.set_background(img, bg_col)
utils.export_image(img=img, filename='frp', fmt=".png", background=None)


