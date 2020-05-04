#!/usr/bin/env python
# coding: utf-8

# # Materials
# 
# PyNE `Material` objects provide a way of representing, manipulating, and storing materials. A `Material` object is a collection of nuclides with various mass fractions (though methods for converting to/from atom fractions are present as well). Optionally, a `Material` object may have an associated mass. By keeping the mass and the composition separate, operations that only affect one attribute may be performed independent of the other. Most of the functionality of the `Material` class is
# implemented in a C++, so this interface is very fast and light-weight.
# 
# `Material`s may be initialized in a number of different ways.  For example, initializing from
# dictionaries of compositions are shown below. First import the `Material` class:

# In[6]:


from pyne.material import Material


# Now create a low enriched uranium (leu) with a mass of 42:

# In[7]:


leu = Material({'U238': 0.96, 'U235': 0.04}, 42)
leu


# Create another `Material`, this one with more components. Notice that the mass is 9 x 1.0 = 9.0: 

# In[8]:


nucvec = {10010:  1.0, 80160:  1.0, 691690: 1.0, 922350: 1.0,
          922380: 1.0, 942390: 1.0, 942410: 1.0, 952420: 1.0,
          962440: 1.0}
mat = Material(nucvec)
print mat


# Materials may also be initialized from plain text or HDF5 files (see ``Material.from_text()`` and
# ``Material.from_hdf5()``).

# ------
# 
# ## Normalization
# 
# Upon instantiation, the mass fraction that define a `Material` are normalized. However, you can always obtain the unnormalized mass vector through ``Material.mult_by_mass()``.  Normalization routines to normalize the mass ``Material.normalize()`` or the composition ``Material.norm_comp()`` are also available. Here we see that our 42 units of LEU consists of 1.68 units of U-235 and 40.32 units of U-238:

# In[4]:


leu.mult_by_mass()


# Recall that `mat` has a mass of 9. Here it is normalized to a mass of 1:

# In[12]:


mat.normalize()
mat


# In[6]:


mat.mass


# -----------
# 
# ## Material Arithmetic
# 
# Various arithmetic operations between Materials and numeric types are also defined.
# Adding two Materials together will return a new Material whose values are the weighted union
# of the two original. Multiplying a Material by 2, however, will simply double the mass of the original Material.

# In[7]:


other_mat = mat * 2
other_mat


# In[8]:


other_mat.mass


# In[9]:


weird_mat = leu + mat * 18
print weird_mat


# Note that there are also ways of mixing `Materials` by volume using known densities. See the `pyne.MultiMaterial` class for more information.

# ---------------
# 
# ## Raw Member Access
# 
# You may also change the attributes of a material directly without generating a new 
# material instance.

# In[10]:


other_mat.mass = 10
other_mat.comp = {10020000: 3, 922350000: 15.0}
print other_mat


# Of course when you do this you have to be careful because the composition and mass may now be out
# of sync.  This may always be fixed with normalization.

# In[11]:


other_mat.norm_comp()
print other_mat


# --------
# 
# ## Indexing & Slicing
# 
# Additionally (and very powerfully!), you may index into either the material or the composition 
# to get, set, or remove sub-materials.  Generally speaking, you may only index into the 
# composition by integer-key and only to retrieve the normalized value.  Indexing into the material allows the 
# full range of operations and returns the unnormalized mass weight.  Moreover, indexing into
# the material may be performed with integer-keys, string-keys, slices, or sequences of nuclides.

# In[12]:


leu.comp[922350000]


# In[13]:


leu['U235']


# In[14]:


weird_mat['U':'Am']


# In[15]:


other_mat[:920000000] = 42.0
print other_mat


# In[16]:


del mat[962440, 'TM169', 'Zr90', 80160]
mat[:]


# Other methods also exist for obtaining commonly used sub-materials, such as gathering the Uranium or 
# Plutonium vector.  

# ### Molecular Weights & Atom Fractions
# 
# You may also calculate the molecular weight of a material via the ``Material.molecular_weight`` method.
# This uses the ``pyne.data.atomic_mass`` function to look up the atomic mass values of
# the constituent nuclides.

# In[17]:


leu.molecular_mass()


# Note that by default, materials are assumed to have one atom per molecule.  This is a poor
# assumption for more complex materials. Take water for example.  Without specifying the 
# number of atoms per molecule, the molecular weight calculation will be off by a factor of 3.
# This can be remedied by passing the correct number to the method.  If there is no other valid
# number of molecules stored on the material, this will set the appropriate attribute on the 
# class.

# In[18]:


h2o = Material({'H1': 0.11191487328808077, 'O16': 0.8880851267119192})
h2o.molecular_mass()


# In[19]:


h2o.molecular_mass(3.0)
h2o.atoms_per_molecule


# It is also useful to be able to convert the current mass-weighted material to 
# an atom fraction mapping.  This can be easily done via the `Material.to_atom_frac()`
# method.  Continuing with the water example, if the number of atoms per molecule is 
# properly set then the atom fraction returned is normalized to this amount.  Alternatively, 
# if the atoms per molecule are set to its default state on the class, then a truly 
# fractional number of atoms is returned.

# In[20]:


h2o.to_atom_frac()


# In[21]:


h2o.atoms_per_molecule = -1.0
h2o.to_atom_frac()


# Additionally, you may wish to convert an existing set of atom fractions to a 
# new material stream.  This can be done with the `Material.from_atom_frac()` method, 
# which will clear out the current contents of the material's composition and replace
# it with the mass-weighted values.  Note that when you initialize a material from atom 
# fractions, the sum of all of the atom fractions will be stored as the atoms per molecule 
# on this class.  Additionally, if a mass is not already set on the material, the molecular
# weight will be used.

# In[22]:


h2o_atoms = {10010000: 2.0, 'O16': 1.0}
h2o = Material()
h2o.from_atom_frac(h2o_atoms)

print h2o.comp
print h2o.atoms_per_molecule
print h2o.mass
print h2o.molecular_mass()


# Moreover, other materials may also be used to specify a new material from atom fractions.
# This is a typical case for reactors where the fuel vector is convolved inside of another 
# chemical form.  Below is an example of obtaining the Uranium-Oxide material from Oxygen
# and low-enriched uranium.

# In[23]:


uox = Material()
uox.from_atom_frac({leu: 1.0, 'O16': 2.0})
print uox


# **NOTE:** Materials may be used as keys in a dictionary because they are hashable.

# ### User-defined Metadata
# 
# Materials also have an ``metadata`` attribute which allows users to store arbitrary 
# custom information about the material.  This can include things like units, comments, 
# provenance information, or anything else the user desires.  This is implemented as an
# in-memory JSON object attached to the C++ class.  Therefore, what may be stored in
# the `metadata` is subject to the same restrictions as JSON itself.  The top-level 
# of the `metadata` *should* be a dictionary, though this is not explicitly enforced.

# In[24]:


leu = Material({922350: 0.05, 922380: 0.95}, 15, metadata={'units': 'kg'})
leu


# In[25]:


print leu


# In[26]:


leu.metadata


# In[27]:


m = leu.metadata
m['comments'] = ['Anthony made this material.']
leu.metadata['comments'].append('And then Katy made it better!')
m['id'] = 42
leu.metadata


# In[28]:


leu.metadata = {'units': 'solar mass'}
leu.metadata


# In[29]:


m


# In[30]:


leu.metadata['units'] = 'not solar masses'
leu.metadata['units']


# As you can see from the above, the attrs interface provides a view into the underlying 
# JSON object.  This can be manipulated directly or by renaming it to another variable.
# Additionally, ``metadata`` can be replaced with a new object of the appropriate type. 
# Doing so invalidates any previous views into this container.

# In[ ]:




