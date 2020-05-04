#!/usr/bin/env python
# coding: utf-8

# Material Library
# ================
# 
# PyNE comes with a pre-built library of materials  Most of this data comes from [a materials compendium by PNNL](http://www.pnnl.gov/main/publications/external/technical_reports/PNNL-15870Rev1.pdf), which is gives canonical values for normal materials.  This notebook demonstrates how to load and use this data via the `MaterialLibrary` class.  First the imports!

# In[6]:


# the path to the nuc_data.h5 database
from pyne import nuc_data

# the material library class itself
from pyne.material import MaterialLibrary


# The `MaterialLibrary` class is a dict-like class which maps string names to `Material` objects.  We can instantiate this class directly from the database as follows.

# In[7]:


mats = MaterialLibrary(nuc_data, datapath='/material_library/materials', nucpath='/material_library/nucid')


# We can also take a gander at the keys in this dictionary.

# In[9]:


list(mats.keys())[:10]


# And the values too!

# In[10]:


mats['Steel, Stainless 440']


# You can do everything you normaly would with these materials, like print them out in MCNP form!

# In[11]:


print(mats['Steel, Stainless 440'].mcnp())

