#!/usr/bin/env python
# coding: utf-8

# ## Materials
# 
# Materials are the primary container for radionuclides. They map nuclides to **mass weights**,
# though they contain methods for converting to/from atom fractions as well.
# In many ways they take inspiration from numpy arrays and python dictionaries.  Materials
# have two main attributes which define them.
# 
# 1. **comp**: a normalized composition mapping from nuclides (zzaaam-ints) to mass-weights (floats).
# 1. **mass**: the mass of the material.
# 
# By keeping the mass and the composition separate, operations that only affect one attribute
# may be performed independent of the other.  Additionally, most of the functionality is
# implemented in a C++ class by the same name, so this interface is very fast and light-weight.
# Materials may be initialized in a number of different ways.  For example, initializing from
# dictionaries of compositions are shown below.

# In[1]:


from pyne.material import Material

leu = Material({'U238': 0.96, 'U235': 0.04}, 42)
leu


# In[2]:


nucvec = {10010:  1.0, 80160:  1.0, 691690: 1.0, 922350: 1.0,
          922380: 1.0, 942390: 1.0, 942410: 1.0, 952420: 1.0,
          962440: 1.0}
mat = Material(nucvec)
print mat


# ### Normalization
# 
# Materials may also be initialized from plain text or HDF5 files (see ``Material.from_text`` and
# ``Material.from_hdf5``).  Once you have a Material instance, you can always obtain the unnormalized
# mass vector through ``Material.mult_by_mass``.  Normalization routines to normalize the mass 
# ``Material.normalize`` or the composition ``Material.norm_comp`` are also available.

# In[3]:


leu.mult_by_mass()


# In[4]:


mat.normalize()
mat.mult_by_mass()


# In[5]:


mat.mass


# ### Material Arithmetic
# 
# Furthermore, various arithmetic operations between Materials and numeric types are also defined.
# Adding two Materials together will return a new Material whose values are the weighted union
# of the two original. Multiplying a Material by 2, however, will simply double the mass.

# In[6]:


other_mat = mat * 2
other_mat


# In[7]:


other_mat.mass


# In[8]:


weird_mat = leu + mat * 18
print weird_mat


# ### Raw Member Access
# 
# You may also change the attributes of a material directly without generating a new 
# material instance.

# In[9]:


other_mat.mass = 10
other_mat.comp = {10020: 3, 922350: 15.0}
print other_mat


# Of course when you do this you have to be careful because the composition and mass may now be out
# of sync.  This may always be fixed with normalization.

# In[10]:


other_mat.norm_comp()
print other_mat


# ### Indexing & Slicing
# Additionally (and very powerfully!), you may index into either the material or the composition 
# to get, set, or remove sub-materials.  Generally speaking, the composition you may only index 
# into by integer-key and only to retrieve the normalized value.  Indexing into the material allows the 
# full range of operations and returns the unnormalized mass weight.  Moreover, indexing into
# the material may be performed with integer-keys, string-keys, slices, or sequences of nuclides.

# In[11]:


leu.comp[922350000]


# In[12]:


leu['U235']


# In[13]:


weird_mat['U':'Am']


# In[14]:


other_mat[:920000000] = 42.0
print other_mat


# In[15]:


del mat[962440, 'TM169', 'Zr90', 80160]
mat[:]


# Other methods also exist for obtaining commonly used sub-materials, such as gathering the Uranium or 
# Plutonium vector.  

# ### Molecular Mass & Atom Fractions
# 
# You may also calculate the molecular mass of a material via the ``Material.molecular_mass`` method.
# This uses the ``pyne.data.atomic_mass`` function to look up the atomic mass values of
# the constituent nuclides.

# In[16]:


leu.molecular_mass()


# Note that by default, materials are assumed to have one atom per molecule.  This is a poor
# assumption for more complex materials.  For example, take water.  Without specifying the 
# number of atoms per molecule, the molecular mass calculation will be off by a factor of 3.
# This can be remedied by passing the correct number to the method.  If there is no other valid
# number of molecules stored on the material, this will set the appropriate attribute on the 
# class.

# In[17]:


h2o = Material({10010000: 0.11191487328808077, 80160000: 0.8880851267119192})
h2o.molecular_mass()


# In[18]:


h2o.molecular_mass(3.0)
h2o.atoms_per_molecule


# It is often also useful to be able to convert the current mass-weighted material to 
# an atom fraction mapping.  This can be easily done via the :meth:`Material.to_atom_frac`
# method.  Continuing with the water example, if the number of atoms per molecule is 
# properly set then the atom fraction return is normalized to this amount.  Alternatively, 
# if the atoms per molecule are set to its default state on the class, then a truly 
# fractional number of atoms is returned.

# In[19]:


h2o.to_atom_frac()


# In[20]:


h2o.atoms_per_molecule = -1.0
h2o.to_atom_frac()


# Additionally, you may wish to convert the an existing set of atom fractions to a 
# new material stream.  This can be done with the :meth:`Material.from_atom_frac` method, 
# which will clear out the current contents of the material's composition and replace
# it with the mass-weighted values.  Note that 
# when you initialize a material from atom fractions, the sum of all of the atom fractions
# will be stored as the atoms per molecule on this class.  Additionally, if a mass is not 
# already set on the material, the molecular mass will be used.

# In[21]:


h2o_atoms = {10010: 2.0, 'O16': 1.0}
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

# In[22]:


uox = Material()
uox.from_atom_frac({leu: 1.0, 'O16': 2.0})
print uox


# **NOTE:** Materials may be used as keys in a dictionary because they are hashable.

# ### User-defined Metadata
# 
# Materials also have an ``attrs`` attribute which allows users to store arbitrary 
# custom information about the material.  This can include things like units, comments, 
# provenance information, or anything else the user desires.  This is implemented as an
# in-memory JSON object attached to the C++ class.  Therefore, what may be stored in
# the ``attrs`` is subject to the same restrictions as JSON itself.  The top-level 
# of the attrs *should* be a dictionary, though this is not explicitly enforced.

# In[23]:


leu = Material({922350: 0.05, 922380: 0.95}, 15, attrs={'units': 'kg'})
leu


# In[24]:


print leu


# In[25]:


leu.metadata


# In[26]:


m = leu.metadata
m['comments'] = ['Anthony made this material.']
leu.metadata['comments'].append('And then Katy made it better!')
m['id'] = 42
leu.metadata


# In[27]:


leu.metadata = {'units': 'solar mass'}
leu.metadata


# In[28]:


m


# In[29]:


leu.metadata['units'] = 'not solar masses'
leu.metadata['units']


# As you can see from the above, the attrs interface provides a view into the underlying 
# JSON object.  This can be manipulated directly or by renaming it to another variable.
# Additionally, ``attrs`` can be replaced with a new object of the appropriate type. 
# Doing so invalidates any previous views into this container.
