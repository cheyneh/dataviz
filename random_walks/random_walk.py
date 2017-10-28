
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import seaborn as sns
sns.set_style('dark')
rs = np.random.RandomState()

num_steps = 50000
pal_args = {'start' : 2,
            'rot'   : .5,
            'gamma' : 1,
            'hue'   : 2,
            'dark'  : 0.2,
            'light' : 0.8}
# pal = sns.cubehelix_palette(as_cmap = True, **pal_args)
pal = 'magma'


pts = rs.normal( size = (num_steps, 2) ).cumsum(axis = 0)

max_x = np.max( pts[:, 0] )
min_x = np.min( pts[:, 0] )
max_y = np.max( pts[:, 1] )
min_y = np.min( pts[:, 1] )


pts = pts.reshape(-1, 1,  2)
segs = np.concatenate([pts[:-1], pts[1:]], axis = 1)

lc = LineCollection(segs, cmap = pal)
lc.set_array(np.array(range(num_steps)))


fig = plt.figure()
ax = fig.gca()
ax.add_collection(lc)
ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)



plt.show()
