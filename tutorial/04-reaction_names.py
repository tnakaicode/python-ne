#!/usr/bin/env python
# coding: utf-8

# # Reaction Names
# 
# In the same way that nuclides have a vareity of different spelling, so do reactions.  Once again, PyNE aims to provide a canonical form while interfacing well with external spellings - such as MT numbers.  Similar to the `nucname` module, the canonical form is given as an integer that may be discovered via the `id()` function, while the human readable name is found via `name()`.
# 
# **Reaction Names:** The names themselves are strings chosen such
# that they are valid variable names in most programming languages
# (including Python and C/C++).  This strategy is known as *natural
# naming* and enables a *namespace* of reactions.  Therefore, all
# names must match the regular expression ``[A-Za-z_][A-Za-z0-9_]*``.
# For example, the elastic scattering cross section is simply
# "elastic" while the pair production reaction is given by
# "pair_prod".
# 
# A number of patterns dictate how a reaction should be named.
# Foremost among these are particle names.  Where required, "z" is a
# variable for any incident particle.  The following table displays
# particle types and their names:
# 
# | particle  | name (z) |
# |-----------|:--------:|
# | neutron   | n        |
# | proton    | p        |
# | deuterium | d        |
# | tritium   | t        |
# | Helium-3  | He3      |
# | alpha     | a        |
# | gamma     | gamma    |
# 
# From this we can see that a reaction that produces a neutron and a
# proton is called "np".  If multiple particles of the same type are
# produced, then the number precedes the particle type.  Thus, one
# neutron and two protons are given by "n2p".  However if this would
# result in the name starting with a number, then the name is
# prepended with ``z_`` to indicate a number of incident particles is coming.  For
# example, a reaction yielding two neutrons is "z_2n" (because
# "2n" is not a valid variable name in most programming languages).
# 
# Furthermore, if a reaction name ends in ``_[0-9]+`` (underscore plus
# digits), then this means that the nucleus is left in the nth excited
# state after the interaction.  For example, "n_0" produces a neutron
# and leaves the nucleus in the ground state, "n_1" produces a neutron
# and the nucleus is in the first excited state, and so on.  However,
# "_continuum" means that the nucleus in an energy state in the
# continuum.
# 
# If a reaction name begins with ``erel_``, then this channel is for
# the energy release from the reaction by the name without ``erel_``.
# E.g. "erel_p" is the energy release from proton emission.
# 
# **Reaction IDs:** While the reaction names are sufficient for
# defining all possible reactions in a partially physically meaningful
# way, they do so using a variable length format (strings).  It is
# often advantageous to have a fixed-width format, namely for storage.
# To this end, unique, unsigned, 32-bit integers are given to each name.
# These identifiers are computed based on a custom hash of the
# reaction name.  This hash function reserves space for MT numbers by
# not producing values below 1000.  It is recommended that the
# reaction identifiers be used for most performance-critical tasks,
# rather than the names from which they are calculated.
# 
# **Reaction Labels:** Reaction labels are short, human-readable
# strings.  These do not follow the naming convention restrictions
# that the names themselves are subject to.  Additionally, labels need
# not be unique.  The labels are provided as a convenience for
# building user interfaces.
# 
# **Reaction Docstrings:** Similar to labels, reactions also come with
# a documentation string that gives a description of the reaction in
# a sentence or two. These provide more help and information for a
# reaction.  This may be useful in a tool-tip context for user
# interfaces.
# 
# **Other Canonical Forms:** This module provides mappings between
# other reaction canonical forms and the naming conventions and IDs
# used here.  The most widespread of these are arguably the MT
# numbers.  MT numbers are a strict subset of the reactions used here.
# Further information may be found at NNDC, NEA, T2, and
# JAEA.
# 
# The rxname module implements a suite of functions for computing or
# retrieving reaction names and their associated data described above.
# These functions have a variety of interfaces. Lookup may occur either by
# name, ID, MT number, a string of ID, or a string of MT number.
# 
# However, lookup may also occur via alternate names or abbreviations.
# For example, "tot" and "abs" will give the names "total" and
# "absorption".  Spelling out particles will also work; "alpha" and "duet"
# will give "a" and "d".  For a listing of all alternative names see the
# ``altnames`` variable.
# 
# Furthermore, certain reactions may be inferred from the nuclide prior
# and post reaction.  For example, if an incident neutron hit U-235 and
# Th-232 was produced, then an alpha production reaction is assumed to have
# occurred. Thus, most of the functions in rxname will take a from nuclide,
# a to nuclide, and z -- the incident particle type (which defaults to "n",
# neutron).  Note that z may also be "decay", indicating a radioactive
# decay occurrence.

# In[1]:


from pyne import rxname


# Each reaction name has a unique id number

# In[6]:


print rxname.id("total")
print rxname.id(103)    # MT number for proton
print rxname.id("abs")


# These are defined on the range from `1000 < id <= 2^32` so that they do not conflict with MT numbers.
# 
# ----------
# 
# The string names are also unique:

# In[7]:


print rxname.name("total")
print rxname.name(103)    # MT number for proton production
print rxname.name("abs")  # an abbreviation for absorption


# ---------
# 
# Each reaction also has meta-data that is stored as short 'labels' and longer documentation strings

# In[8]:


print rxname.label('p')
print rxname.doc('p')


# ---------
# 
# Where possible, MT numbers may be looked up.

# In[9]:


print rxname.mt('elastic')
print rxname.mt('p')


# -----
# Finally, nuclides themselves may also be used to look up reactions.

# In[11]:


# From -> to
rxname.name("U235", "U236")


# This interface has a notion of the incident particle type (`z`).  This defaults to `n` for neutrons but may be any of the particle types listed above.

# In[12]:


rxname.name("U235", "Np236", "p")


# In[13]:


rxname.name(922350000, 912350000)


# There are also ``parent()`` and ``child()`` functions, which instead let you discover the parent or child from a nuclide, the reaction, and the incidnet particle type.

# In[14]:


rxname.parent("U236", 'abs')


# In[15]:


rxname.child("U235", 'abs', 'p')

