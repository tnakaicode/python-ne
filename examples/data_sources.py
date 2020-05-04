#!/usr/bin/env python
# coding: utf-8

# # Data Sources
# 
# Below are examples of how to grab cross sections from the EAF 
# and simple data sources and re-discretize them.

# In[15]:


from pyne.xs.data_source import *
from pyne.bins import stair_step
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='serif', size=14)
import numpy as np
dst_e_g = np.logspace(1, -7, 11)


# ## EAF Data Source

# In[16]:


eds = EAFDataSource()
rx = eds.reaction('U235', 'gamma')
rx


# In[17]:


eds.dst_group_struct = dst_e_g
rxc = eds.discretize('U235', 'gamma')


# In[18]:


fig = plt.figure(figsize=(7,7))
plt.loglog(*stair_step(eds.src_group_struct, rx), figure=fig)
plt.loglog(*stair_step(eds.dst_group_struct, rxc), figure=fig)
plt.xlabel('E [MeV]')
plt.ylabel('Cross Section [barns]')


# ## Simple Data Source

# In[7]:


sds = SimpleDataSource(dst_group_struct=dst_e_g)
print(sds.exists)
rx = sds.reaction('U233', 'absorption')
rxc = sds.discretize('U233', 'absorption')


# In[8]:


fig = plt.figure(figsize=(7,7))
plt.loglog(sds.src_group_struct[:-1], rx, figure=fig)
plt.loglog(sds.dst_group_struct[:-1], rxc, figure=fig)
plt.xlabel('E [MeV]')
plt.ylabel('Cross Section [barns]')


# The data sources are caches, which means that subsequent requests for 
# the same data are very fast! 

# In[9]:


get_ipython().magic(u"time sds.reaction('U238', 'fiss')")
print()
get_ipython().magic(u"time sds.reaction('U238', 'fission')")
print()
get_ipython().magic(u"time sds.reaction('U238', 'fiss')")
print()


# In[7]:




