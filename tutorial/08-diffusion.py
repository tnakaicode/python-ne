#!/usr/bin/env python
# coding: utf-8

# # Neutron Diffusion in Python 
# 
# ----------------------
# NOTE: The plotting/display portion of example is currenty BROKEN! see [the forum discussion](https://groups.google.com/forum/#!topic/pyne-dev/rM7iIorXHJA) and [the PR](https://github.com/pyne/pyne/pull/667) and [the issue](https://github.com/pyne/pyne/issues/576). The code itself is completely valid and a great example of cool things you can do in PyNE.
# 
# 
# ------------------
# This notebook is an entirely self-contained solution to a basic [neutron diffision](http://mragheb.com/NPRE%20402%20ME%20405%20Nuclear%20Power%20Engineering/One%20Group%20Reactor%20Theory.pdf) equation for a reactor *rx* made up of a single fuel rod. The one-group diffusion equation that we will be stepping through time and space is, 
# 
# $\frac{1}{v}\frac{\partial \phi}{\partial t} = D \nabla^2 \phi + (k - 1) \Sigma_a \phi + S$
# 
# where 
# 
# * $\phi$ is the neutron flux [n/cm$^2$/s],
# * $D$ is the diffusion coefficient [cm],
# * $k$ is the multiplication factor of the material [unitless],
# * $S$ is a static source term [n/cm$^2$/s], and
# * $v$ is the neutron velocity, which for [thermal neutrons](http://en.wikipedia.org/wiki/Neutron_temperature) is 2.2e5 [cm/s]

# ## First, Make a Mesh
# 
# PyNE Meshes will be used to compute all of the nuclear data needs here and for a semi-structured MOAB Hex8 meshes. The simulation, analysis, and visulaization here takes place entirely within memory.

# In[ ]:


get_ipython().run_line_magic('pylab', 'inline')


# In[ ]:


from itertools import product 
from pyne.mesh import Mesh, NativeMeshTag
from pyne.xs.cache import XSCache
from pyne.xs.data_source import CinderDataSource, SimpleDataSource, NullDataSource
from pyne.xs.channels import sigma_a, sigma_s
from pyne.material import Material, from_atom_frac
import numpy as np
from yt.config import ytcfg; ytcfg["yt","suppressStreamLogging"] = "True"
from yt.frontends.moab.api import PyneMoabHex8Dataset
from yt.mods import *
from itaps import iBase, iMesh
from JSAnimation import IPython_display
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from IPython.display import HTML


# In[ ]:


xsc = XSCache([0.026e-6, 0.024e-6], (SimpleDataSource, NullDataSource))


# ### The Laplacian
# 
# The functions in the following cell solve for the laplacian ($\nabla^2$) for any index in in the mesh using a [3 point stencil](http://en.wikipedia.org/wiki/Five-point_stencil) along each axis. This implements reflecting boundary conditions along the edges of the domain.

# In[ ]:


def lpoint(idx, n, coords, shape, m):
    lidx = list(idx)
    lidx[n] += 1 if idx[n] == 0 else -1
    left = m.structured_get_hex(*lidx)
    l = m.mesh.getVtxCoords(left)[n]
    if idx[n] == 0:
        l = 2*coords[n] - l 
    return left, l

def rpoint(idx, n, coords, shape, m):
    ridx = list(idx)
    ridx[n] += -1 if idx[n] == shape[n]-2 else 1
    right = m.structured_get_hex(*ridx)
    r = m.mesh.getVtxCoords(right)[n]
    if idx[n] == shape[n]-2:
        r = 2*coords[n] - r
    return right, r

def laplace(tag, idx, m, shape):
    ent = m.structured_get_hex(*idx)
    coords = m.mesh.getVtxCoords(ent)
    lptag = 0.0
    for n in range(3):
        left, l = lpoint(idx, n, coords, shape, m)
        right, r = rpoint(idx, n, coords, shape, m)
        c = coords[n]
        lptag += (((tag[right] - tag[ent])/(r-c)) - ((tag[ent] - tag[left])/(c-l))) / ((r-l)/2)
    return lptag


# ### Solve in space
# 
# The ``timestep()`` function sweeps through the entire mesh and computes the new flux everywhere.  This operation takes place entirely on the mesh object.

# In[ ]:


def timestep(m, dt):
    nx = len(m.structured_get_divisions("x"))
    ny = len(m.structured_get_divisions("y"))
    nz = len(m.structured_get_divisions("z"))
    shape = (nx, ny, nz)
    D = m.mesh.getTagHandle("D")
    k = m.mesh.getTagHandle("k")
    S = m.mesh.getTagHandle("S")
    Sigma_a = m.mesh.getTagHandle("Sigma_a")
    phi = m.mesh.getTagHandle("flux")
    phi_next = m.mesh.getTagHandle("phi_next")
    for idx in product(*[range(xyz-1) for xyz in shape]):
        ent = m.structured_get_hex(*idx)
        phi_next[ent] = (max(D[ent] * laplace(phi, idx, m, shape) + 
                                    (k[ent] - 1.0) * Sigma_a[ent] * phi[ent], 0.0) + S[ent])*dt*2.2e5 + phi[ent]
    ents = m.mesh.getEntities(iBase.Type.region)
    phi[ents] = phi_next[ents]


# ### Solve in time
# 
# The ``render()`` function steps through time calling the ``timestep()`` function and then creating an image.  The images that are generated are then dumped into a movie.

# In[ ]:


def render(m, dt, axis="z", field="flux", frames=100):
    pf = PyneMoabHex8Dataset(m)
    s = SlicePlot(pf, axis, field, origin='native')
    fig = s.plots['pyne', field].figure
    fig.canvas = FigureCanvasAgg(fig)
    axim = fig.axes[0].images[0]

    def init():
        axim = s.plots['pyne', 'flux'].image
        return axim

    def animate(i):
        s = SlicePlot(pf, axis, field, origin='native')
        axim.set_data(s._frb['pyne', field])
        timestep(m, dt)
        return axim

    return animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=100, blit=False)


# ### Reactor
# 
# This setups up a simple light water reactor fuel pin in a water cell.  Note that our cells are allowed to have varing aspect ratios.  This allows us to be coarsely refined inside of the pin, finely refined around the edge of the pin, and then have a different coarse refinement out in the coolant.

# In[ ]:


def isinrod(ent, rx, radius=0.4):
    """returns whether an entity is in a control rod"""
    coord = rx.mesh.getVtxCoords(ent)
    return (coord[0]**2 + coord[1]**2) <= radius**2

def create_reactor(multfact=1.0, radius=0.4):
    fuel = from_atom_frac({'U235': 0.045, 'U238': 0.955, 'O16': 2.0}, density=10.7)
    cool = from_atom_frac({'H1': 2.0, 'O16': 1.0}, density=1.0)
    xpoints = [0.0, 0.075, 0.15, 0.225] + list(np.arange(0.3, 0.7, 0.025)) + list(np.arange(0.7, 1.201, 0.05))
    ypoints = xpoints
    zpoints = np.linspace(0.0, 1.0, 8)
    # Make Mesh
    rx = Mesh(structured_coords=[xpoints, ypoints, zpoints], structured=True)
    # Add Tags
    rx.D = NativeMeshTag(size=1, dtype=float)
    rx.k = NativeMeshTag(size=1, dtype=float)
    rx.S = NativeMeshTag(size=1, dtype=float)
    rx.Sigma_a = NativeMeshTag(size=1, dtype=float)
    rx.flux = NativeMeshTag(size=1, dtype=float)
    rx.phi_next = NativeMeshTag(size=1, dtype=float)
    # Assign initial conditions
    Ds = []; Sigma_as = []; phis = []; ks = [];
    for i, mat, ent in rx:
        if isinrod(ent, rx, radius=radius):
            Ds.append(1.0 / (3.0 * fuel.density * 1e-24 * sigma_s(fuel, xs_cache=xsc)))
            Sigma_as.append(fuel.density * 1e-24 * sigma_a(fuel, xs_cache=xsc))
            phis.append(4e14)
            ks.append(multfact)
        else:
            Ds.append(1.0 / (3.0 * cool.density * 1e-24 * sigma_s(cool, xs_cache=xsc)))
            Sigma_as.append(cool.density * 1e-24 * sigma_a(cool, xs_cache=xsc))
            r2 = (rx.mesh.getVtxCoords(ent)[:2]**2).sum()
            phis.append(4e14 * radius**2 / r2 if r2 < 0.7**2 else 0.0)
            ks.append(0.0)
    rx.D[:] = np.array(Ds)[:,0]
    rx.Sigma_a[:] = np.array(Sigma_as)[:,0]
    rx.flux[:] = np.array(phis)[:]
    rx.k[:] = ks
    rx.S[:] = 0.0
    rx.phi_next[:] = 0.0
    return rx


# In[ ]:


rx = create_reactor()


# In[ ]:


#this doesn't plot correctly
field= 'flux'
axis = 'z'
n = 2 
for i in range(n):
    timestep(rx,2.5e-31)
pf = PyneMoabHex8Dataset(rx)
s = SlicePlot(pf, axis, field, origin='native')
s.display()


# In[ ]:


# this is broken
render(rx, dt=2.5e-31, frames=10)


# ### Exercises:
# 
# Left to the reader is to modify this notebook to diffuse
# 
# * a point source, or
# * a line source.
