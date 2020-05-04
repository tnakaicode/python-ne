#!/usr/bin/env python
# coding: utf-8

# # Spatial Solver Tutorial

# Spatialsolver is a pyne module that contains seven neutron transport equation solvers.
# The neutron transport equation is a balance statement that conserves neutrons.

# In[2]:


import pyne
import pyne.spatialsolver
import numpy as np


# In[3]:


input_dict = {'Name': 'Jane', 'Age': 27};


# The spatial solver module takes in a dictionary that contains all of the input information required to run the solvers.  There are many entries to allow a high degree of customization, not all of which are required.  To find which entries are required, see the spatial solver documentation in the python api.

# In[4]:


input_dict['solver'] = "AHOTN"


# There are many different ways to solve the neutron transport equations.  The spatial solver method supports seven different methods, described in the theory manual.  The 'solver' key allows you to select which family of these solvers you would like to use, out of the following three options.  
#     1.  "AHOTN" - Arbitrarily higher order transport method
#     2.  "DGFEM" - Discontinuous Galerkin Finite Element Method
#     3.  "SCTSTEP" - SCT Step algorithm similar to Duo’s SCT algorithm implemented in three dimensional Cartesian geometry.

# In[5]:


input_dict['solver_type'] = "LN" 


# Each family of solvers except for SCTSTEP offers a number of different choices for the specific way the neutron transport equation is solved.  For full descriptions of each, consult the theory manual.
# For AHOTN, the supported solver_type's are:
#     1.  "LN" - Arbitrarily higher order transport method of the nodal type linear-nodal method
#     2.  "LL" - Arbitrarily higher order transport method of the nodal type linear-linear method
#     3.  "NEFD" - Arbitrarily higher order transport method of the nodal type that makes use of the unknown nodal flux moments (NEFD algorithm).
#     
# DGFEM
#     1.  "LD"  -  The Discontinuous Galerkin Finite Element Method (DGFEM) with a linear discontinuous (LD) approximation for angular flux.
#     2.  "DENSE" - The Discontinuous Galerkin Finite Element Method (DGFEM) that uses dense lagrange polynomials
#     3.  "LAGRANGE" - The Discontinuous Galerkin Finite Element Method (DGFEM) that use lagrange polynomials    
#     
# SCTSTEP
# 
#     SCT Step algorithm similar to Duo’s SCT algorithm implemented in three dimensional Cartesian geometry.

# In[6]:


input_dict['spatial_order'] = 1


# The Spatial expansion order is the expansion order of the spatial moment.  It is also known as lambda, and for all AHOTN solvers it must be 0, 1 or 2.

# In[7]:


input_dict['angular_quadrature_order'] = 4


#   The angular quadrature order is the number of angles to be used per octant.  
#   For N sets of angles, there will be (N * (N + 2) / 8) ordinates per octant. 
#   The quadrature order may only be an even number!

# In[8]:


input_dict['angular_quadrature_type'] = 1


#   The quadrature type is the type of quadrature scheme the code uses.  
#   The possibilities are:
#   
#     1 - TWOTRAN
#     2 - EQN
#     3 - Read-in

# In[9]:


input_dict['nodes_xyz'] = [4,4,4]


# 'nodes_xyz' is the number of node's in the x y and z directions.  It should be stored in a 1 by 3 array, with the following entries:<br /> 
#     [0] = number of nodes in x direction (integer)<br /> 
#     [1] = number of nodes in y direction (integer)<br /> 
#     [2] = number of nodes in z direction (integer)

# In[10]:


input_dict['num_groups'] = 1


# 'num_groups' specifies the number of material groups you are using in the material id and cross section files found in later entries.

# In[11]:


input_dict['num_materials'] = 1


# 'num_materials' is the number of different materials used in the mesh ('material_id').

# In[12]:


input_dict['x_cells_widths'] = [0.25, 0.25, 0.25, 0.25]


# In[13]:


input_dict['y_cells_widths'] = [0.25, 0.25, 0.25, 0.25]


# In[14]:


input_dict['z_cells_widths'] = [0.25, 0.25, 0.25, 0.25]


# 'x_cells_widths', 'y_cells_widths', and 'z_cells_widths' are the cell widths for each cell in the x, y and z direction.  Every unique cell cannot be a unique size, adjacent edges all must match up.  Therefore, each cell width you specify is the width of all the cells in the plane orthogonal to the axis of the cell you specified.  For example, if you selected 1 to be the first entry in x_cell_width, all of the cells with x dimension 1 would be 1 unit wide. 
# 
# This entry takes an array, which must be 1 by the number of nodes in that specific axis, and have all entries filled.

# In[15]:


input_dict['x_boundry_conditions'] = [2, 2]


# In[16]:


input_dict['y_boundry_conditions'] = [2, 2]


# In[17]:


input_dict['z_boundry_conditions'] = [2, 2]


# 'x_boundry_conditions', 'y_boundry_conditions', and 'z_boundry_conditions' are the boundry conditions for each face of the cubic mesh.  The entries are as follows: x is the array set to the key 'x_boundry_conditions', y to 'y_boundry_conditions' and z to 'z_boundry_conditions'.
# 
#     x[0] = xsbc
#     x[1] = xebc
#     y[0] = ysbc
#     y[1] = yebc
#     z[0] = zsbc
#     z[1] = zebc
# 
# The following are supported boundry conditions:
#     1.  0 - vacuum
#     2.  1 - reflective
#     3.  2 - fixed inflow

# In[18]:


input_dict['material_id'] = [ [ [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1] ], 
                              [ [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1] ],  
                              [ [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1] ],  
                              [ [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1] ] ]


# 'material_id' is an array containing the material infomation for the cubic mesh for which the neutron transport method is to be solved.  
# note: Dimensions must match cells such that there is one material number
#        in each spatial cell. The cells are ordered as x, y, z.

# In[19]:


input_dict['quadrature_file'] = 'quad_file'


# 'quad_file' is the quadrature file.  It is only used if the quadrature_type is 2; in this case it is a required entry.  If your quadrature_type is not 2, just create a blank file to pass in for this entry.  See formatting notes in the Spatial Solver Python API.

# In[20]:


input_dict['xs_file'] = 'xs'


# 'xs_file' is the file containing the cross sectional data for the materials in your mesh ('material_id').  They should be formatted similar to the following 2 material example xs file:
#       
#     ! Cross section file
#     ! Material # 1
#     ! Group #1
#     5.894     ! Total XS
#     1.8       ! Scattering matrix
#     ! Material # 2
#     ! Group #1
#     1.237      ! Total XS
#     0.12       ! Scattering matrix

# In[21]:


input_dict['source_input_file'] = 'src_4.dat'


# Note: see input file formatting notes in the Source File Formatting section.

# In[22]:


input_dict['bc_input_file'] = 'bc_4.dat'


# 'bc_input_file' is the boundry condition input file.  It contains the boundry neutron inflow for any faces of the mesh with the boundry condition specified as 2 (fixed inflow).  See the Boundry Condition formatting notes in the Spatial Solver Python API for more information.

# In[23]:


input_dict['flux_output_file'] = 'phi_4.ahot'


# 'flux_output_file' is the output file for the angular flux to be printed to.

# In[24]:


input_dict['convergence_criterion'] = 1.e-12


#  The solution is considered converged and the calculation completes when the flux
#  in each cell at the current iteration is within "convergence_criterion" of the
#  previous iterate. This is generally the relative difference, but in cases of 
#  very small flux values the absolute difference is used instead (see the 
#  Convergence Tolerance entry below). 

# In[25]:


input_dict['max_iterations'] = 6000


# 'max_iterations' is the maximum number of times the mesh should be sweeped.
#  Note: if this number of iterations is reached before the convergence criterion
#        is satisfied, the calculation will terminate and report the current flux
#        estimate.

# In[26]:


input_dict['moments_converged'] = 0


#  Moments converged is the number of moments that should be converged upon for each quadrature in the
#  solution space.  Value for moments converged must be in range [0, spatial_order_in].

# In[27]:


input_dict['converge_tolerence'] = 1.e-10


#  <pre>Converge tolerance is the tolerance that determines how the difference between
#  flux iterates (df) that is used to determine convergence will be calculated. 
#  df is calculated as follows:
#    f = current flux value
#    ct = convergence tolerance (value for this key, "converge_tolerance")
#    f1 = flux value from the previous iteration
#    If f1 > ct:
#      df = absolute(f - f1) / f1
#    Else
#      df = absolute(f - f1)
#  The idea is to use the absolute difference instead of the relative difference
#  between iterates when the flux is very small to help avoid rounding error.</pre>

# In[28]:


dict_results = {}
dict_results = pyne.spatialsolver.solve(input_dict)


# Before doing anything with the resulting data, you should check if the solver succesfully ran.
# If the dictionary key 'success' is 1 (true), the job ran succesfully.  If it is 0 (false), you
# were not so succesfull.

# In[29]:


if(dict_results['success']):
    print('Yay, job ran succesfully!')
print(dict_results['success'])


# If you were not so lucky, and your job failed, the following key will give you the error message.  It will be 0 if the codes ran succesfully.

# In[30]:


print(dict_results['error_msg'])


# To get the results of the solver, create a output dictionary to store all the data from the solver, and then use solve to populate it!

# In[31]:


print(dict_results['flux'])


# There are a few other useful keys remaining in the dictionary.  If you want to know the total time your job took, you can get it using the 'total_time' key.

# In[32]:


print('Total solving time was: ')
print(dict_results['total_time'])


# The 'time_start' key will give you the system time when your solver call began.  If you need the absoulte system time when the solver call finished, you can easily get it by adding the total job time ('total_time' key) and the solver start time ('time_start' key).

# In[33]:


print('Solver call started at: ')
print(dict_results['time_start'])
print('Solver call finished at: ')
print(dict_results['time_start'] + dict_results['total_time'])


# Thats it!
