#!/usr/bin/env python
# coding: utf-8

# In[1]:


from yt.mods import *
import h5py


# In[2]:


# If necessary files aren't in the current dir, download them
if not os.path.isfile("mcnp_n_impr_fluka.h5m"):
    from urllib import urlretrieve
    urlretrieve("http://data.pyne.io/mcnp_n_impr_fluka.h5m", "mcnp_n_impr_fluka.h5m")
    
if not os.path.isfile("fng_usrbin22.h5m"):
    # fng_usrbin22.h5m is a large file
    # needs to be downloaded in chunks
    import requests
    r = requests.get("http://data.pyne.io/fng_usrbin22.h5m", stream=True)
    with open("fng_usrbin22.h5m" , 'wb') as file:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                file.flush()


# In[4]:


# Load data file
pf = load("fng_usrbin22.h5m")


# In[5]:


# Create the desired slice plot
s = SlicePlot(pf, 'z', ('moab','TALLY_TAG'), origin='lower-native')
# Load the facet file
f = h5py.File("mcnp_n_impr_fluka.h5m", "r")
# Get the triangle vertices
coords = f["/tstt/nodes/coordinates"][:]
conn = f["/tstt/elements/Tri3/connectivity"][:]
points = coords[conn-1]
# Annotate slice-triangle intersection contours to the plot
s.annotate_triangle_facets(points, plot_args={"colors": 'black'})
s.display()


# In[4]:





# In[4]:




