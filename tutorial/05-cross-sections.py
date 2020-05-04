#!/usr/bin/env python
# coding: utf-8

# # Cross Section Interface
# 
# PyNE provides a top-level interface for computing (and caching) multigroup neutron cross sections.
# These cross sections will be computed from a variety of available data sources (stored in `nuc_data.h5`).
# This interface remains the same across all data sources, allowing the user to easily swap out which 
# cross section library they wish to use.
# 
# The following cross section formats are included with PyNE.
# 
# * The ENDF file format (experimental), 
# * The ACE file format, 
# * EAF 175-group cross sections,
# * CINDER 63-group cross sections,
# * A two-point fast/thermal interpolation (using 'simple_xs' data from KAERI),
# * Physical models, and
# * Null data.
# 
# This functionality may be be found in the `xs` sub-package.  This package is 
# separated out into the following modules:
# 
#     models
#     data_source
#     cache
#     channels

# ## Data Sources
# 
# Data sources are classes that provide the common interface for grabbing cross section data from a data source.  Unless otherwise specified, this is lazily evaluated.  The data source object itself then acts as an in-memory cache, making further look ups of the raw data very quick! 
# 
# To get a sense of how this works, let's pull in some data that we know about.  

# ### EAF Data Source

# In[1]:


from pyne.xs.data_source import EAFDataSource, SimpleDataSource, NullDataSource


# In[2]:


eds = EAFDataSource()
# reaction returns a dictionary containing source group structure, energy values, 
# cross-section data, and interpolation data.
gamma = eds.reaction('U235', 'gamma')
gamma


# The data source also provides a method to re-discretize this data to another group structure.

# In[3]:


import numpy as np
dst_e_g = np.logspace(1, -7, 11)

# dst_group_struct is the group structure of the destination cross sections.
eds.dst_group_struct = dst_e_g

# discreatizes the reaction channel from the source group structure to that of the
# destination, weighted by the group fluxes.
gamma_c = eds.discretize('U235', 'gamma')
print gamma_c
print dst_e_g


# Now let's plot it!

# In[6]:


from pyne.bins import stair_step
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='serif', size=14)


# In[13]:


fig = plt.figure(figsize=(7,7))
plt.loglog(*stair_step(eds.src_group_struct, gamma), figure=fig) # original
plt.loglog(*stair_step(eds.dst_group_struct, gamma_c), figure=fig) # new group structure
plt.xlabel('E [MeV]')
plt.ylabel('Cross Section [barns]')
plt.legend(('original', 'rediscretized'))


# ### Simple Data Source
# 
# This interface is independent of where the data came from. As it should be!

# In[8]:


sds = SimpleDataSource(dst_group_struct=dst_e_g)
print sds.exists
rx = sds.reaction('U233', 'absorption') # cross section data
rxc = sds.discretize('U233', 'absorption') # discretization of data


# In[12]:


fig = plt.figure(figsize=(7,7))
plt.loglog(sds.src_group_struct[:-1], rx, figure=fig)
plt.loglog(sds.dst_group_struct[:-1], rxc, figure=fig)
plt.xlabel('E [MeV]')
plt.ylabel('Cross Section [barns]')
plt.legend(('original', 'rediscretized'))


# Since data sources are caches, subsequent requests for 
# the same data are very fast! 

# In[10]:


get_ipython().run_line_magic('time', "sds.reaction('U238', 'fiss')")
print
get_ipython().run_line_magic('time', "sds.reaction('U238', 'fission')")
print
get_ipython().run_line_magic('time', "sds.reaction('U238', 'fiss')")
print


# ## Cross Section Caching
# 
# Now suppose you want to perform the same discretization and wish to pull cross sections from many sources (with some precedence) based on whether the data is available or not.  Enter `XSCache`.  This is a class to do exactly that.  
# 
# This class acts like a dictionary whose keys are `(nuclide, rx)` or `(nuclide, rx, temp)` tuples for the nuclide, reaction id, and temperature that you wish to know.  

# In[14]:


from pyne.xs.cache import XSCache


# In[16]:


xscache = XSCache(group_struct=dst_e_g,
                  data_sources=[EAFDataSource, SimpleDataSource, NullDataSource])


# In[17]:


xscache['U235', 'abs']


# In[18]:


xscache['H42', 'gamma']


# ## Reading ACE Files
# 
# To load data from an ACE file, one needs to simply initialize an instance of the `Library` class specifying the path to the `Library` file:
# 
#     from pyne import ace
#     libFile = ace.Library('endf70a')
#     libFile.read()
#     

# ## Reading ENDF Files
# Similarly, ENDF file reading and cross-section discretization is supported.

# In[19]:


from pyne.xs.data_source import ENDFDataSource
from pyne import nucname
from urllib import urlretrieve
from os.path import isfile

# Download the data file if it isn't there
if not isfile("Ni59.txt"):
    urlretrieve("http://t2.lanl.gov/nis/data/data/ENDFB-VII.1-neutron/Ni/59",
                "Ni59.txt")
    


# In[20]:


endfds = ENDFDataSource("Ni59.txt")

# get the nonelastic reaction data for Ni-59
nonelastic_rx = endfds.reaction("Ni59", "nonelastic")

# set the group structure and re-discretize
nonelastic_rx['dst_group_struct'] = np.logspace(7, -5, 33)
nonelastic_c = endfds.discretize("Ni59", "nonelastic")


# Now let's plot it!!
# 

# In[22]:


fig = plt.figure(figsize=(7,7))

# e_int is the array of energy values over which to integrate
E_g = nonelastic_rx['e_int']
# xs is the array of cross-sections corresponding to e_int
nonelastic = nonelastic_rx['xs']

# with base group structure
plt.loglog(*stair_step(E_g, nonelastic[:-1]), figure=fig) 
# discretized with new group structure
plt.loglog(*stair_step(nonelastic_rx['dst_group_struct'], nonelastic_c), figure=fig) 
plt.xlabel('E [MeV]')
plt.ylabel('Cross Section [barns]')
plt.legend(('original', 'rediscretized'))


# ## Cross Section Channels
# 
# PyNE also provides an easy interface to very quickly grab multigroup cross sections from the cross section cache and collapse them to the appropriate group structure. This is done in the `pyne.xs.channels` module.  This contains functions such as `sigma_f()` for computing the fission cross section.
# 
# The functions in the channels module are extended from what you would normally be able to see from the cache.  For example, you may compute cross sections for materials, fission energy spectra, metastable ratios, etc.

# In[23]:


from pyne.xs import channels
from pyne.material import Material, from_atom_frac


# In[24]:


fuel = from_atom_frac({'U235': 0.045, 'U238': 0.955, 'O16': 2.0}, mass=1.0, density=10.7)

# the cross section is mapped to fuel with group structure dist_e_g
# the default temp is 300K; this uses a group flux.
channels.sigma_f(fuel, group_struct=dst_e_g)


# In[ ]:




