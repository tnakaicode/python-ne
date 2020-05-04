#!/usr/bin/env python
# coding: utf-8

# # Open ORIGEN data generation
# 
# This notebook generates data for the ORIGEN v2.2 TAPE9.INP file. The data format is described in http://web.ornl.gov/info/reports/1980/3445605762840.pdf on pages 63-66 in the text. 

# In[38]:


import numpy as np
import pyne
from pyne import nucname
from pyne import data


# ## Read data from nuc_data
# This uses the ENSDF data stored in nuc_data.h5

# In[40]:


import tables as tb
def getnuc(nuc = 430990001):
    """
    This computes ORIGEN data based on ENSDF data. 
    FIXME: calculate B- and EC decays that end in metastable state after gamma transition

    Parameters
    ----------
    nid : nuc_id
        a valid string or int that can be converted into a nuc_id
    meta_t : float
        minimum lifetime of metastable state (in seconds) to be included (default 1.0 s)

    Returns
    -------
    nuc_id : int
        nuc_id of parent
    t12 : float
        half life of parent in seconds
    fb : float
        percent of B- decays per decay of parent 
    fbx : float
        percent of B- decays that end in metastable state
    fsf : float
        percent of spontaneous fission decays per decay of parent
    fpec : float
        percent of B+ and EC decays per decay of parent
    fpecx : float
        percent of B+ and EC decays that end in metastable state
    fa : float
        percent of A decays per decay of parent
    fn : float
        percent of B- + neutron decays per decay of parent
    fit : float
        percent of internal transition decays per decay of parent
    """
    if nuc % 10000 > 0:
        nuc = pyne.nucname.id_to_state_id(nuc)
    t12 = np.inf
    f = tb.open_file(pyne.nuc_data)
    a = None
    bm =  None
    sf = None
    ec = None
    ecx = None
    it = None
    bmn = None
    bmx = None
    for item in f.root.decay.level_list.where('nuc_id == ' + str(nuc)):
        if item['rx_id'] != 0:
            if item['rx_id'] == 36565:
                sf = item['branch_ratio']
            elif item['rx_id'] == 1089:
                a = item['branch_ratio']
            elif item['rx_id'] == 4130566254:
                bm = item['branch_ratio']
            elif item['rx_id'] == 35974:
                ec = item['branch_ratio']
            elif item['rx_id'] == 36125:
                it = item['branch_ratio']
            elif item['rx_id'] == 1355894015:
                bmn = item['branch_ratio']
            #print item['rx_id'],rxname.name(item['rx_id']), item['branch_ratio']
        else:
            t12 = item['half_life']
    if bm is not None:
        beta_states = data.beta_child_byparent(nuc)
        beta_intens = data.beta_intensity(nuc)
        bmx = 0.0
        for index, state in enumerate(beta_states):
            try:
                pyne.nucname.state_id_to_id(state)
            except RuntimeError:
                pass
            else:
                bmx = bmx + beta_intens[index]
        bmx = bmx * data.decay_beta_branch_ratio(nuc,(state // 10000) * 10000)[0]
        bmx = bmx/bm*100.0
    if ec is not None:
        ec_states = data.ecbp_child_byparent(nuc)
        ec_intens = data.ec_intensity(nuc)
        bp_intens = data.beta_plus_intensity(nuc)
        ecx = 0.0
        for index, state in enumerate(ec_states):
            try:
                pyne.nucname.state_id_to_id(state)
            except RuntimeError:
                pass
            else:
                ecx = ecx + ec_intens[index] + bp_intens[index]
        ecx = ecx * data.decay_beta_branch_ratio(nuc,(state // 10000) * 10000)[0]
        ecx = ecx/ec*100.0
    return nuc, t12, bm, bmx, sf, ec, ecx, a, bmn, it


# In[41]:


getnuc(551370000)

