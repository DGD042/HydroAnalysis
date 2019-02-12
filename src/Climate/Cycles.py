# -*- coding: utf-8 -*-
#______________________________________________________________________________
#______________________________________________________________________________
#
#                       Coded by Daniel González Duque
#                           Last revised 11/03/2016
#______________________________________________________________________________
#______________________________________________________________________________

'''


 CLASS DESCRIPTION:
   This class have different routines for hydrological analysis. 

   This class do not use Pandas in any function, it uses directories and save
   several images in different folders. It is important to include the path 
   to save the images.
   
______________________________________________________________________________
'''
# ------------------------
# Importing Modules
# ------------------------ 
# Manipulate Data
import numpy as np
import scipy.io as sio
from scipy import stats as st
from datetime import date, datetime, timedelta
import time
# Graph
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
# System
import sys
import os
import glob as gl
import re
import operator
import warnings

# ------------------
# Personal Modules
# ------------------
# Importing Modules
try:
    from HydroAnalysis.src.Utilities import Utilities as utl
    from HydroAnalysis.src.Utilities import Data_Man as DM
    from HydroAnalysis.src.Dates.DatesC import DatesC
    from HydroAnalysis.src.Dates import DatesFunctions as DUtil
except ImportError:
    from src.Utilities import Utilities as utl
    from src.Utilities import Data_Man as DM
    from Dates.DatesC import DatesC
    from Dates import DatesFunctions as DUtil

def CiclA(VMes,Years,flagA=False,oper='mean'):
    '''
    DESCRIPTION:
        This function calculates the annual cycle of a variable, also
        calculates the annual series of required.

        Additionally, this function can makes graphs of the annual cycle 
        and the annual series if asked.
    _______________________________________________________________________

    INPUT:
        :param VMes:  A ndarray, Variable with the monthly data.
        :param Years: A list or ndarray, Vector with the initial and 
                                         final year.
        :param flagA: A boolean, flag to know if the annual series 
                                 is required.
        :param oper:  A ndarray, Operation for the annual data.
    _______________________________________________________________________
    
    OUTPUT:

    '''

    # --------------------
    # Error Managment
    # --------------------
    if len(Years) > 2:
        return utl.ShowError('CiclA','Hydro_Analysis','Years index vector larger than 2, review vector')
    
    # --------------------
    # Years Managment
    # --------------------
    Yi = int(Years[0])
    Yf = int(Years[1])
    VarM = np.reshape(VMes,(-1,12))
    # --------------------
    # Annual Cycle 
    # --------------------
    # Verify NaN data from the cycle
    MesM = np.empty(12)
    VarMNT = []
    for i in range(12):
        q = sum(~np.isnan(VarM[:,i]))
        VarMNT.append(sum(~np.isnan(VarM[:,i])))
        if q < round(len(VarM[:,i])*0.70,0):
            MesM[i] = np.nan
        else:
            MesM[i] = np.nanmean(VarM[:,i]) # Multianual Mean
    
    MesD = np.nanstd(VarM,axis=0) # annual strandard deviation.
    MesE = np.array([k/np.sqrt(VarMNT[ii]) for ii,k in enumerate(MesD)]) # annual Error

    # --------------------
    # Annual Series
    # --------------------
    if flagA:
        # Determine operation
        Operation = DM.Oper_Det(oper)
        # ----------------
        # Error managment
        # ----------------
        if Operation == -1:
            return -1
        # Calculations
        AnM = np.empty(VarM.shape[0])
        AnMNT = []
        for i in range(VarM.shape[0]):
            q = sum(~np.isnan(VarM[i,:]))
            if q <= len(VarM[i,:])*0.70:
                AnM[i] = np.nan
                AnMNT.append(np.nan)
            else:
                AnM[i] = Operation(VarM[i,:])
                AnMNT.append(q)

        AnD = np.nanstd(VarM,axis=1) # Annual deviation
        AnE = np.array([k/np.sqrt(AnMNT[ii]) for ii,k in enumerate(AnD)]) # Annual Error 

    # Return values
    results = dict()

    if flagA:
        results['MesM'] = MesM 
        results['MesD'] = MesD 
        results['MesE'] = MesE 
        results['AnM'] = AnM
        results['AnD'] = AnD
        results['AnE'] = AnE
        return results
    else:
        results['MesM'] = MesM 
        results['MesD'] = MesD 
        results['MesE'] = MesE 
        return results



