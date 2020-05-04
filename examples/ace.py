#!/usr/bin/env python
# coding: utf-8

# ACE Module
# ==========
# 
# This notebook demonstrates basic usage of the ``pyne.ace`` module.

# In[1]:


import os
import matplotlib.pyplot as plt
import pyne.ace
if not os.path.isfile("W180.ace"):
    from urllib import urlretrieve
    urlretrieve("https://www-nds.iaea.org/wolfram/w180/beta3/W180.ace", "W180.ace")


# The main class in ``pyne.ace`` is called ``Library``. It is instantiated using the name of an ACE file, in this case one distributed with MCNP.

# In[2]:


lib = pyne.ace.Library('W180.ace')


# One can choose to read all tables in the file or selectively read a subset by specifying an argument to the ``read`` method.

# In[3]:


lib.read('74180.21c')


# After the call to ``read()``, the Library instance will have a dictionary called ``tables``.

# In[4]:


lib.tables


# In[5]:


w180 = lib.tables['74180.21c']


# Once a table is selected, we can inspect, e.g., the energy grid and the total cross section.

# In[6]:


w180.energy


# In[7]:


w180.sigma_t


# To get data on a reaction, such as fission or $(n,2n)$, there is an attribute called ``reactions``.

# In[8]:


w180.reactions


# In[9]:


elastic = w180.reactions[2]


# An instance of a Reaction contains the reaction cross section and any angular or energy distributions that may be present.

# In[10]:


elastic.sigma


# With the energy grid (stored on the table), and the cross section (stored on the reaction), one can generate plots of the cross section.

# In[11]:


plt.loglog(w180.energy, elastic.sigma)

