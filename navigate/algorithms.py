import numpy as np
import skimage.graph

N = 2048


def navigate(arrays, options):
    """based on a depth image (img), navigate from the top to the bottom, starting and ending in the deepest parts"""
    img = arrays['img']
    x = arrays['x']
    y = arrays['y']
    min_depth = options['min-depth']
    xmin, xmax, ymin, ymax = arrays['extent']


    # find start end end point (start in deepest points in first and last row)
    j0 = img[1,:].argmax()
    end = N - 1
    jn = img[end,:].argmax()

    # mask cells that are not deep enough, non grid cells are also masked
    depth_masked = np.ma.masked_less(img, min_depth)

    # generate the cost matrix object
    # we probably want a more advanced cost function, let's do that later, for now, the rule is:
    # - deeper parts cost less
    # - too undeep areas need to be dredged, which costs 1e9 per cell
    # normalized depth_mask
    # deepest area cost 0, undeep areas cost 1.0
    depth_masked_normalized = (depth_masked - depth_masked.min())/(depth_masked.max() - depth_masked.min())

    # this is the main navigation object. See skimage.graph manual for details.
    mcp = skimage.graph.MCP((1 - depth_masked_normalized).filled(1e9))

    # generate cost matrices
    cost, traceback = mcp.find_costs(starts=[(0, j0)], ends=[(end,jn)])
    # compute how many cells we have to dredge and the cost function over the path
    dredge, distance = divmod(cost[end, jn], 1e9)
    # traceback from the end
    path = mcp.traceback((end, jn))
    # create a rowcolumn vector
    rowcolumn = np.array(path)
    # lookup path coordinates, not sure why we need to inverse y, guess we have negative pixels??
    xy = np.c_[x[rowcolumn[:,1]], y[rowcolumn[:,0]]]

    results = dict(
        xy=xy,
        cost=cost,
        dredge=dredge,
        rowcolumn=rowcolumn,
        traceback=traceback,
        distance=distance,
        depth_masked=depth_masked
    )
    return results
