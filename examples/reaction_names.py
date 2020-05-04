#!/usr/bin/env python
# coding: utf-8

# # Reaction Names
# 
# This demonstrates how the rxname module may be used to find and manipulate the PyNE cannonical reaction names.

# In[1]:


from pyne.rxname import *


# In[2]:


print name("total")
print name(103)    # MT number for proton production
print name("abs")  # an abbreviation for absorption


# Each reaction name has a unique id number

# In[3]:


print id("total")
print id(103)    # MT number for proton
print id("abs")  # an abbreviation


# Each reaction also has labels and documentation strings

# In[4]:


print label('p')
print doc('p')


# Where possible, MT numbers may be looked up.

# In[5]:


print mt('elastic')
print mt('p')


# Finally, nuclides themselves may also be used to look up reactions.

# In[6]:


print name("U235", "U236")
print name("U235", "Np236", "p")
print name(922350, 912350)


# In[6]:




