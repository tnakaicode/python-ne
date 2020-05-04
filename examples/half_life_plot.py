#!/usr/bin/env python
# coding: utf-8

# ## Half-life Plot

# In[2]:


import numpy as np
get_ipython().magic(u'matplotlib inline')
import matplotlib
matplotlib.rc('font', family='serif', size=14)
import matplotlib.pyplot as plt
from pyne import nucname, nuc_data

import tables as tb
f = tb.open_file(nuc_data)
anums = map(nucname.anum, f.root.decay.level_list[:]['nuc_id'])
#anums = map(nucname.anum, data.half_life_map.keys())


# In[3]:


fig = plt.figure(figsize=(7,7))
plt.semilogy(anums,  f.root.decay.level_list[:]['half_life'], 'ko')
plt.xlabel('A')
plt.ylabel('Half-life [s]')


# In[ ]:




