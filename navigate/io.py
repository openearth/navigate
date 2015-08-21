import netCDF4
import numpy as np
import skimage.draw
import shapely.geometry
import geojson

N = 2048


def get_last_depth(filename):
    ds = netCDF4.Dataset(filename)
    # get waterdepth at t end
    depth = ds.variables['waterdepth'][-1]
    xc = ds.variables['FlowElemContour_x'][:]
    yc = ds.variables['FlowElemContour_y'][:]
    ds.close()

    # get the bounding box of all cell contours
    xmin, xmax = xc.ravel().min(), xc.ravel().max()
    ymin, ymax = yc.ravel().min(), yc.ravel().max()
    # create equidistant grid of NxN cells
    x = np.linspace(xmin, xmax, num=N)
    y = np.linspace(ymin, ymax, num=N)
    extent = (xmin, xmax, ymin, ymax)
    # draw all the cells on the rectilinear grid
    img = np.ma.masked_array(np.zeros((N, N)), dtype='float32', mask=True)
    for i, (x_, y_) in enumerate(zip(
        N*(xc - xmin)/(xmax - xmin),
        N*(yc - ymin)/(ymax - ymin)
    )):
        rr, cc = skimage.draw.polygon(y_, x_, shape=(N,N))
        img[rr, cc] = depth[i]
    # dictionary with all arrays
    results = {
        "depth": depth,
        "xc": xc,
        "yc": yc,
        "x": x,
        "y": y,
        "extent": extent,
        "img": img
    }
    return results


def to_geojson(arr):
    """convert array of points to geojson LineString"""
    geom = shapely.geometry.LineString(arr)
    return geojson.dumps(geom)



