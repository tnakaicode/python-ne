#!/usr/bin/env python
# coding: utf-8

# In[10]:


from urllib import urlretrieve
from os import path, getcwd, remove
from numpy import linspace, bitwise_or

from pyne.mesh import Mesh, NativeMeshTag
from pyne.dagmc import load, discretize_geom

from yt.config import ytcfg; ytcfg["yt","suppressStreamLogging"] = "True"
from yt.frontends.moab.api import PyneMoabHex8Dataset
from yt.visualization.plot_window import SlicePlot


# In[11]:


faceted_file = path.join(getcwd(), 'teapot.h5m')
if not path.isfile(faceted_file):
    url = "http://data.pyne.io/teapot.h5m"
    urlretrieve(url, faceted_file)
load(faceted_file)


# In[12]:


num_divisions = 50
num_rays = 3

coords0 = linspace(-6, 6, num_divisions)
coords1 = linspace(0, 7, num_divisions)
coords2 = linspace(-4, 4, num_divisions)


# In[ ]:


m = Mesh(structured=True, structured_coords=[coords0, coords1, coords2], structured_ordering='zyx')


# In[ ]:


results = discretize_geom(m, num_rays=num_rays, grid=False)


# In[ ]:


m.vols = NativeMeshTag(1, float)
mask = bitwise_or(results['cell'] == 1, results['cell'] == 2)
m.vols[results['idx'][mask]] = results[mask]['vol_frac']


# In[ ]:


pf = PyneMoabHex8Dataset(m)


# In[ ]:


s = SlicePlot(pf, 'z', 'vols')
s.display()

