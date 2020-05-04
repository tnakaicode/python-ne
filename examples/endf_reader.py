#!/usr/bin/env python
# coding: utf-8

# # ENDF Files
# 
# ## Library class
# 
# Below is an example of how to grab and graph cross section data from ENDF files using the `Library` class.

# In[1]:


get_ipython().magic(u'matplotlib inline')

import os
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
    
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
from tabulate import tabulate

from pyne.endf import Library, Evaluation


# In[2]:


if not os.path.isfile("U235-VII.txt"):
    urlretrieve("http://t2.lanl.gov/nis/data/data/ENDFB-VII-neutron/U/235", "U235-VII.txt")


# In[3]:


u235 = Library("U235-VII.txt")
xs_data = u235.get_xs(922350000, 16)[0]


# In[4]:


fig = plt.figure()
Eints, sigmas = xs_data['e_int'], xs_data['xs']
plt.step(Eints, sigmas, where = "pre")
plt.suptitle(r'(n, 2n) Reaction in $^{235}$U')
plt.ylabel(r'$\sigma(E)$ (barns)')
plt.xlabel(r'$E_{int} (eV)$')
plt.xscale('log')
plt.yscale('log')
plt.savefig('u235_2n.eps')


# In[5]:


if not os.path.isfile("U238-VII.txt"):
    urlretrieve("http://t2.lanl.gov/nis/data/data/ENDFB-VII-neutron/U/238", "U238-VII.txt")


# In[6]:


u238 = Library("U238-VII.txt")
xs_data = u238.get_xs(922380000, 1)[0]


# In[7]:


fig = plt.figure()
Eints, sigmas = xs_data['e_int'], xs_data['xs']
plt.step(Eints, sigmas, where = "pre")
plt.suptitle(r'Total Cross Section for $^{238}$U')
plt.ylabel(r'$\sigma(E)$ (barns)')
plt.xlabel(r'$E_{int} (eV)$')
plt.xlim(xmin = 10000)
plt.xscale('log')
plt.yscale('log')


# ## Evaluation class
# 
# The `pyne.endf.Evaluation` class provides a facility for parsing data in an ENDF file. Parsing of all data other than covariances (MF=30+) is supported has been tested against the ENDF/B-VII.1 neutron, photoatomic, electroatomic, atomic relaxation, and photonuclear sublibraries. In this example, we will use the `Evaluation` class to look at typical data in the ENDF/B-VII.1 evaluation of U-235.

# In[8]:


u235 = Evaluation("U235-VII.txt")


# By default, when an `Evaluation` is instantiated, only the descriptive data in MF=1, MT=451 is parsed. This allows us to get basic information about an evaluation without necessarily reading the whole thing. This useful data can be found in the `info` and `target` attributes.

# In[9]:


u235.info


# In[10]:


u235.target


# To look at cross sections, secondary energy and angle distributions, and resonance data, we need to parse the rest of the data in the file, which can be done through the `Evaluation.read(...)` method.

# In[11]:


u235.read()


# Most of the data that is parsed resides in the `reactions` attribute, which is a dictionary that is keyed by the MT value.

# In[12]:


elastic = u235.reactions[2]
print('Elastic scattering has the following attributes:')
for attr in elastic.__dict__:
    if elastic.__dict__[attr]:
        print('  ' + attr)


# Now with our reaction we can look at the cross section and any other associated data. The cross section `elastic.xs` is a `Tab1` object whose (x,y) pairs can be accessed from the `x` and `y` attributes. The first ten values of the cross section are:

# In[13]:


zip(elastic.xs.x[:10], elastic.xs.y[:10])


# Since resonances haven't been reconstructed, everything below the unresolved resonance range at 2250 keV is zero. Above that energy, we can use `elastic.xs` like a function to get a value at a particular energy. For example, to get the elastic cross section at 1 MeV:

# In[14]:


elastic.xs(1.0e6)


# We can also take a look at the angular distribution for elastic scattering.

# In[15]:


esad = elastic.angular_distribution
print(esad)


# In[16]:


# Elastic scattering angular distribution at 100 keV
E = esad.energy[5]
pdf = esad.probability[5]

theta = np.linspace(0., 2*np.pi, 1000)
mu = np.cos(theta)

plt.subplot(111, polar=True)
plt.plot(theta, pdf(mu))


# Ah, but elastic scattering is a simple reaction you say. What if I want information about something more complicated like fission! In the special case of fission, there is the normal reaction data as well as a special attribute on the Evaluation class called `fission`:

# In[17]:


print(u235.reactions[18])
print(u235.fission.keys())


# We can look at the neutrons released per fission:

# In[18]:


E = np.logspace(-5, 6)
plt.semilogx(E, u235.fission['nu']['total'](E))
plt.xlabel('Energy (eV)')
plt.ylabel('Neutrons per fission')            


# The components of energy release from fission are also available to us:

# In[19]:


for component, coefficients in u235.fission['energy_release'].items():
    if component != 'order':
        print('{}: {} +/- {} MeV'.format(component, coefficients[0,0], coefficients[1,0]))


# To look at the fission energy distribution, we must use the normal reaction data:

# In[20]:


# Get prompt fission neutron spectra
fission = u235.reactions[18]
pfns = fission.energy_distribution[0]

# Plot the distribution for the lowest incoming energy
plt.semilogx(pfns.pdf[0].x, pfns.pdf[0].y)
plt.xlabel('Energy (eV)')
plt.ylabel('Probability / eV')
plt.title('Neutron spectrum at E={} eV'.format(pfns.energy[0]))


# Finally, let's take a look at resolved resonance data, which can be found in the `resonances` dictionary.

# In[21]:


rrr = u235.resonances['resolved']
print(rrr)

# Show all (l,J) combinations
print(rrr.resonances.keys())


# In[22]:


# Set up headers for table
headers = ['Energy', 'Neutron width', 'Capture width', 'FissionA width', 'FissionB width']

# Get resonance data for l=0, J=3
l = 0
J = 3.0

# Create table data
data = [[r.energy, r.width_neutron, r.width_gamma, r.width_fissionA, r.width_fissionB]
        for r in rrr.resonances[l,J]]

# Render table
HTML(tabulate(data, headers=headers, tablefmt='html'))

