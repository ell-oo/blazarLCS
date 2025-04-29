import numpy as np
import logging
import matplotlib.pyplot as plt


def hop(x):
    """
    Run HOP algorithm
    
    Parameters
    ----------
    x: `~numpy.ndarray`
        array with density (fluxes, ...)
    
    Returns
    -------
    Three `~numpy.ndarrays` with ids of peaks,
    the working id_hop vector, and a list with the 
    ids of the sheds

    Notes
    -----
    Adopted from Jeff Scargle's implementation 
    in MatLab
    """
    id_hop_vec = list(range(len(x)))
    
    # Exceptions for end points:

    if x[1] > x[0]:
        id_hop_vec[0] = 1

    if x[-2] > x[-1]:
        id_hop_vec[-1] = len(x) - 2
    
    for ii in range(2, len(x) - 1):

        x_left = x[ii-1]
        x_this = x[ii]
        x_rite = x[ii+1]
        
        id_next = np.argmax([x_left, x_rite])
        x_next = [x_left, x_rite][id_next]
    
        if x_next > x_this:
            if not id_next:
                id_hop_vec[ii] = ii - 1
            else:
                id_hop_vec[ii] = ii + 1
    
    #===================================
    #         now do HOP
    #===================================
    id_hop_vec = np.array(id_hop_vec)
    id_hop_work = np.array(id_hop_vec)
    id_hop_old = np.array(id_hop_work)


    while True:
    
    # update pointers via local hill climbing
        
        id_hop_work = id_hop_vec[ id_hop_work ]
        delt = np.sum( id_hop_work - id_hop_old )
        if delt == 0:
            break
        id_hop_old = id_hop_work
    
    id_peaks_vec = np.unique(id_hop_work)
    id_sheds = []
    for ii,idp in enumerate(id_peaks_vec):
        id_sheds.append(np.where(id_hop_work == idp)[0])
    return  id_peaks_vec#,id_hop_work, id_sheds
