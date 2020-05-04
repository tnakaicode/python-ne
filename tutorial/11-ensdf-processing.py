#!/usr/bin/env python
# coding: utf-8

# # ENSDF Processing Tutorial

# ensdf_processing is a pyne module that contains ensdf (Evaluated Nuclear Structure Data File) evaluation tools.  It includes ALPHAD, BRICC, DELTA, GABS, GTOL, BLDHST, HSICC, HSMRG, SEQHST, LOGFT, RADLIST, RADD and RULER.  FUll documentation for the internal structure of each can be found at:
# 
# http://www.nndc.bnl.gov/nndcscr/ensdf_pgm/analysis/
# 
# Examples of the Python interface for these evaluation tools follows.

# In[1]:


import pyne
from pyne import ensdf_processing


# All of the evaluation tools have a single dictionary parameter.

# In[3]:


input_dict = {}


# This input dictionary must have all of the key-pair values specified in the documentation for the specific evaluation tool being run.  In this example, alphad will be run, which requires the following keys: 
# * 'input_file'
# * 'report_file'
# * 'rewrite_input_with_hinderance_factor'
# * 'output_file'.

# In[4]:


input_dict['input_file'] = 'ensdf_processing/alphad/ref_a228.ens'
input_dict['report_file'] = '/alphad.rpt'
input_dict['rewrite_input_with_hinderance_factor'] = 1
input_dict['output_file'] = '/alphad.out'
output_dict = ensdf_processing.alphad(input_dict)


# To run the evaluation tool, call ensdf_processing.<name of tool>(dictionary)

# In[6]:


output_dict = ensdf_processing.alphad(input_dict)


# A dictionary is returned, with all the input key-pairs, as well as any other information the evaluation tool returns.  In this case, no additional key-pair values have been added to the returned dictionary.  Alphad wrote the resulting output file to '/alphad.out', and has a report file at 'alphad.rpt', both specified by the input dicitonary.

# In[7]:


print(output_dict)


# # Following are examples of each of the evaluation tools packaged with PyNE:

# ## ALPHAD (calculates alpha HF's and theoretical half-lives)

# In[9]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/alphad/ref_a228.ens'
input_dict['report_file'] = '/tmp_alphad.rpt'
input_dict['rewrite_input_with_hinderance_factor'] = 1
input_dict['output_file'] = '/tmp_alphad.out'
output_dict = ensdf_processing.alphad(input_dict)


# ## BRICC (Calculates the conversion electron, electron-positron pair conversion coeffcients and the E0 electronic factors)

# In[11]:


input_dict = {}
input_dict['input_type'] = 'evaluation'
input_dict['input_file'] = 'ensdf_processing/bricc/ref_a228.ens'
input_dict['BrIccNH'] = 0
output_dict = ensdf_processing.bricc(input_dict)


# ## BLDHST

# In[14]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/bldhst/ref_bldhst_iccseq.dat'
input_dict['output_table_file'] = '/tmp_bldhst_icctbl.dat'
input_dict['output_index_file'] = '/tmp_bldhst_iccndx.dat'
output_dict = ensdf_processing.bldhst(input_dict)


# ## DELTA (analyzes gamma-gamma angular correlations from unaligned states)

# In[36]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/delta/ref_inp.dat'
input_dict['output_file'] = '/tmp_delta.dat'
output_dict = ensdf_processing.delta(input_dict)


# ## GABS (gamma-ray absolute intensity and normalization calculation)

# In[37]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/gabs/ref_gabs_80Br.in'
input_dict['output_file'] = '/tmp_gabs_80Br.rpt'
input_dict['dataset_file'] = '/tmp_gabs_80Br.new'
output_dict = ensdf_processing.gabs(input_dict)


# ## GTOL (performs a least-squares fit to the gamma-energies to obtain level energies and calculates the net feedings to levels)

# In[38]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/gtol/ref_gtol.inp'
input_dict['report_file'] = '/tmp_gtol.rpt'
input_dict['new_ensdf_file_with_results'] = 0
input_dict['output_file'] = '/tmp_gtol.out'
input_dict['supress_gamma_comparison'] = 1
input_dict['supress_intensity_comparison'] = 1
input_dict['dcc_theory_percent'] = 1.4
output_dict = ensdf_processing.gtol(input_dict)


# ## HSICC (interpolates Hager-Seltzer and Dragoun internal conversion coefficients)

# In[39]:


input_dict = {}
input_dict['data_deck'] = 'ensdf_processing/hsicc/ref_hsicc_data.tst'
input_dict['icc_index'] = 'ensdf_processing/hsicc/ref_hsicc_iccndx.dat'
input_dict['icc_table'] = 'ensdf_processing/hsicc/ref_hsicc_icctbl.dat'
input_dict['complete_report'] = '/tmp_out_hsicc_hscalc.lst'
input_dict['new_card_deck'] = '/tmp_out_hsicc_cards.new'
input_dict['comparison_report'] = '/tmp_out_hsicc_compar.lst'
input_dict['is_multipol_known'] = 'Y'
output_dict = ensdf_processing.hsicc(input_dict)


# ## HSMRG

# In[40]:


input_dict = {}
input_dict['data_deck'] = 'ensdf_processing/hsmrg/ref_hsmrg_data.tst'
input_dict['card_deck'] = 'ensdf_processing/hsmrg/ref_hsmrg_cards.new'
input_dict['merged_data_deck'] = '/tmp_out_cards.mrg'
output_dict = ensdf_processing.hsmrg(input_dict)


# ## SEQHST

# In[41]:


input_dict = {}
input_dict['binary_table_input_file'] = 'ensdf_processing/seqhst/ref_seqhst_icctbl.dat'
input_dict['sequential_output_file'] = '/tmp_out_iccseq.dat'
output_dict = ensdf_processing.seqhst(input_dict)


# ## LOGFT (calculates log ft values for beta and electron-capture decay, average beta energies, and capture fractions)

# In[47]:


input_dict = {}
input_dict['input_data_set'] = 'ensdf_processing/logft/ref_logft.inp'
input_dict['output_report'] = '/tmp_logft.rpt'
input_dict['data_table'] = 'ensdf_processing/logft/ref_logft.dat'
input_dict['output_data_set'] = '/tmp_logft.new'
output_dict = ensdf_processing.logft(input_dict)


# ## RADD

# In[49]:


input_dict = {}
input_dict['atomic_number'] = '86'
input_dict['neutron_number'] = '113'
input_dict['output_file'] = 'tmp_output.out'
radd_output = ensdf_processing.radd(input_dict)


# ## RADLIST (calculates atomic & nuclear radiations; checks energy balance)

# In[50]:


input_dict = {}
input_dict['output_radiation_listing'] = 'Y'
input_dict['output_ensdf_like_file'] = 'N'
input_dict['output_file_for_nudat'] = 'N'
input_dict['output_mird_listing'] = 'N'
input_dict['calculate_continua'] = 'N'
input_dict['input_file'] = 'ensdf_processing/radlst/ref_radlst.inp'
input_dict['output_radlst_file'] =  '/tmp_radlst.rpt'
input_dict['input_radlst_data_table'] = 'ensdf_processing/radlst/ref_mednew.dat'
input_dict['output_ensdf_file'] =  '/tmp_ensdf.rpt'
output_dict = ensdf_processing.radlist(input_dict)


# ## RULER (calculates reduced transition probabilities)

# In[45]:


input_dict = {}
input_dict['input_file'] = 'ensdf_processing/ruler/ref_ruler.inp'
input_dict['output_report_file'] = '/tmp_ruler.rpt'
input_dict['mode_of_operation'] = 'R'
input_dict['assumed_dcc_theory'] = '1.4'
output_dict = ensdf_processing.ruler(input_dict)


# In[ ]:




