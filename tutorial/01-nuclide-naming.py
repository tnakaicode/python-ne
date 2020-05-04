#!/usr/bin/env python
# coding: utf-8

# Nuclide Naming Conventions
# ==========================
# One of the most basic aspects of nuclear software is how to uniquely represent 
# nuclide names.  There exists a large number of different ways that people choose 
# to spell these names.  Functionally, there are three pieces of information that *should* 
# be included in every radionuclide's name:
# 
# 1. **Z Number**: The number of protons.
# 2. **A Number**: The number of nucleons (neutrons + protons).
# 3. **S Number**: The internal energy excitation state of the nucleus.
# 
# Some common naming conventions exist. The following are currently supported by PyNE:
# 
#  * **id (ZAS)**: This type places the charge of the nucleus out front, then has three
#    digits for the atomic mass number, and ends with four state digits (0 = ground,
#    1 = first metastable state, 2 = second metastable state, etc).  Uranium-235 has
#    92 protons and an atomic mass number of 235. It would be expressed as '922350000'
#    This is the canonical form for nuclides.
#  * **name**: This is the more common, human readable notation.  The chemical symbol
#    (one or two characters long) is first, followed by the atomic weight.  Lastly if
#    the nuclide is metastable, the letter *M* is concatenated to the end.  For
#    example, 'H-1' and 'Am242M' are both valid.  Note that nucname will always
#    return name form with the dash removed and all letters uppercase.
#  * **zzaaam**: This type places the charge of the nucleus out front, then has three
#    digits for the atomic mass number, and ends with a metastable flag (0 = ground,
#    1 = first excited state, 2 = second excited state, etc).  Uranium-235 here would
#    be expressed as '922350'.
#  * **SZA**: This type places three state digits out front, the charge of the nucleus in 
#    the middle, and then has three digits for the atomic mass number. Uranium-235M here 
#    would be expressed as '1092235'.  
#  * **MCNP**: The MCNP format for entering nuclides is unfortunately
#    non-standard.  In most ways it is similar to zzaaam form, except that it
#    lacks the metastable flag.  For information on how metastable isotopes are
#    named, please consult the MCNPX documentation for more information.
#  * **Serpent**: The serpent naming convention is similar to name form.
#    However, only the first letter in the chemical symbol is uppercase, the
#    dash is always present, and the the meta-stable flag is lowercase.  For
#    instance, 'Am-242m' is the valid serpent notation for this nuclide.
#  * **NIST**: The NIST naming convention is also similar to the Serpent form.
#    However, this convention contains no metastable information.  Moreover, the
#    A-number comes before the element symbol.  For example, '242Am' is the
#    valid NIST notation.
#  * **CINDER**: The CINDER format is similar to zzaaam form except that the
#    placement of the Z- and A-numbers are swapped. Therefore, this format is
#    effectively aaazzzm.  For example, '2420951' is the valid cinder notation
#    for 'AM242M'.
#  * **ALARA**: In ALARA format, elements are denoted by the lower case atomic symbol. Isotopes are
#    specified by appending a semicolon and A-number. For example, "fe" and "fe:56" represent
#    elemental iron and iron-56 respectively. No metastable flag exists.
#  * **state_id**: State id format is similar to **id** except that it refers to each energy level in
#    the order they are reported in the ENSDF file. This can change between ENSDF releases as more 
#    levels are added so it is not the default id form.

# ----------------
# 
# Canonical Form
# --------------
# A [canonical form](http://en.wikipedia.org/wiki/Canonical_form) is 
# *"a representation such that every object has a unique representation."*
# Since there are many ways to represent nuclides, PyNE chooses one of them
# to be *the* canonical form.  **Note:** this idea of 
# canonical forms will come up many times in PyNE.
# 
# The **id** integer form of nuclide names is the fundamental form of nuclide naming because
# it accurately captures all of the needed information in the smallest amount of space.  Given that the 
# Z-number may be up to three digits, A-numbers are always three digits, and the excitation level is
# 4 digits, all possible nuclides are represented on the range ``10000000 < zzaaam < 2130000000``. 
# This falls well within 32 bit integers.
# 
# The ``id()`` function converts other representations to the id format. 

# In[2]:


from pyne import nucname


# In[2]:


nucname.id('U-235')


# In[3]:


nucname.id('Am-242m')


# While applications and backends should use the **id** form under-the-covers, the **name** form provides an easy way to covert nuclide to a consistent and human readable representation.

# In[4]:


nucname.name(922350000)


# In[5]:


nucname.name(10010000)


# In[6]:


nucname.name('CM-244m')


# The **name** string representations may be anywhere from two characters (16 bits)
# up to six characters (48 bits).  So in general, **id** is smaller by 50%.  
# 
# Other forms do not necessarily contain all of the required information (``MCNP``) or require additional 
# storage space (``Serpent``).  It may seem pedantic to quibble over the number of bits per nuclide name, 
# but these identifiers are used everywhere throughout nuclear code, so it behooves us to be as small
# and fast as possible.

# The other distinct advantage that integer forms have is that you can natively perform arithmetic
# on them.  For example::

# In[6]:


# Am-242m
nuc = 942420001

# Z-number
z = nuc/10000000
print z

# A-number
a = (nuc/10000)%1000
print a

# state
s = nuc%10000
print s


# Of course, there are built in functions to do exactly this as well.

# In[7]:


print nucname.znum(nuc)
print nucname.anum(nuc)
print nucname.snum(nuc)


# Code internal to PyNE uses **id**, and except for human readability, you should too! Natural elements are specified in this form by having zero A-number and excitation flags.

# In[8]:


nucname.id('U')


# ---------
# 
# # Ambiguous Forms
# 
# For some nuclides and forms, ambiguities may arise. For example "10000" is elemental neon in MCNP and elemental hydrogen in ZZAAAM. To resolve such ambiquities when you *know* which form you are coming from, PyNE provides a suite of `*_to_id()` functions. For example:

# In[3]:


nucname.mcnp_to_id(10000)


# In[4]:


nucname.zzaaam_to_id(10000)


# -------------------
# 
# Examples of Use
# ---------------

# In[12]:


nucname.zzaaam('U235')


# In[13]:


nucname.name(10010)


# In[14]:


nucname.serpent('AM242M')


# In[15]:


nucname.name_zz['Sr']


# In[16]:


nucname.zz_name[57]


# In[6]:


nucname.alara('FE56')


# In[13]:


nucname.id_to_state_id(952420001)

