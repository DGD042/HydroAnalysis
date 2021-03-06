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
from scipy import stats as st
from datetime import date, datetime, timedelta
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
    from HydroAnalysis.src.Gen_Functions import *
except ImportError:
    from src.Utilities import Utilities as utl
    from src.Utilities import Data_Man as DM
    from src.Dates.DatesC import DatesC
    from src.Dates import DatesFunctions as DUtil
    from src.Gen_Functions import *

def PrecDryDays(Date,Prec,Ind=0.1):
    '''
        DESCRIPTION:
    
    This function calculates the number of consecutive days without 
    precipitation.
    _______________________________________________________________________

        INPUT:
    + Date: Vector of dates.
    + Prec: Precipitation vector in days.
    + Ind: Indicator of the minimum precipitation value.
    _______________________________________________________________________
    
        OUTPUT:
    - TotalNumDays: Vector with total number of consecutive days without 
                    precipitation.
    - MaxNumDays: Maximum number of consecutive days without precipitation.
    '''
    
    # Number of days below the indicated (Ind) value
    x = np.where(Prec <= Ind)[0]

    TotalNumDays = [] # List with all the days
    TotalPrecCount = [] # List for the total precipitation
    TotalDateB = [] # List of dates

    # Loop to calculate all the days
    DaysCount = 1 # Days counter
    PrecCount = Prec[x[0]] # Precipitation counter
    for i in range(1,len(x)):
        if x[i] == x[i-1]+1:
            DaysCount += 1
            PrecCount += Prec[x[i]]
        else:
            TotalNumDays.append(DaysCount)
            TotalPrecCount.append(PrecCount)
            TotalDateB.append(Date[x[i]-DaysCount])
            DaysCount = 1
            PrecCount = 0

    TotalNumDays = np.array(TotalNumDays)
    # Maximum number of days withput precipitation
    MaxNumDays = np.max(TotalNumDays)

    TotalPrecCount = np.array(TotalPrecCount)
    # Maximum value of total precipitation in those days
    MaxPrecCount = np.max(TotalPrecCount)

    # Beginning date of the maximum dry days
    TotalDateB = np.array(TotalDateB)
    xx = np.where(TotalNumDays == MaxNumDays)[0]
    DateMaxDays = TotalDateB[xx]

    return TotalNumDays,MaxNumDays,TotalPrecCount,MaxPrecCount,TotalDateB,DateMaxDays

def PrecMoistDays(Date,Prec,Ind=0.1):
    '''
    DESCRIPTION:
    
        This function calculates the number of consecutive days with 
        precipitation above certain value.
    _______________________________________________________________________

    INPUT:
        + Date: Vector of dates.
        + Prec: Precipitation vector in days.
        + Ind: Indicator of the minimum precipitation value.
    _______________________________________________________________________
    
    OUTPUT:
        - TotalNumDays: Vector with total number of consecutive days 
                        without precipitation.
        - MaxNumDays: Maximum number of consecutive days without 
                      precipitation.
    '''
    
    # Number of days below the indicated (Ind) value
    x = np.where(Prec >= Ind)[0]

    TotalNumDays = [] # List with all the days
    TotalPrecCount = [] # List for the total precipitation
    TotalDateB = [] # List of dates

    # Loop to calculate all the days
    DaysCount = 1 # Days counter
    PrecCount = Prec[x[0]] # Precipitation counter
    for i in range(1,len(x)):
        if x[i] == x[i-1]+1:
            DaysCount += 1
            PrecCount += Prec[x[i]]
        else:
            TotalNumDays.append(DaysCount)
            TotalPrecCount.append(PrecCount)
            TotalDateB.append(Date[x[i]-DaysCount])
            DaysCount = 1
            PrecCount = 0

    TotalNumDays = np.array(TotalNumDays)
    # Maximum number of days with precipitation
    MaxNumDays = np.max(TotalNumDays)
    x = np.where(TotalNumDays == MaxNumDays)[0]

    TotalPrecCount = np.array(TotalPrecCount)
    # Maximum of precipitation of number of days that was max
    MaxPrecCount_MaxDay = np.max(TotalPrecCount[x])

    # Maximum value of total precipitation in those days
    MaxPrecCount = np.max(TotalPrecCount)
    x = np.where(TotalPrecCount == MaxPrecCount)[0]
    # Maximum number of days of the max precipitation
    MaxNumDays_MaxPrec = np.max(TotalNumDays[x])


    # Beginning date of the maximum dry days
    TotalDateB = np.array(TotalDateB)
    xx = np.where(TotalNumDays == MaxNumDays)[0]
    DateMaxDays = TotalDateB[xx]

    return TotalNumDays,MaxNumDays,TotalPrecCount,MaxPrecCount,TotalDateB,DateMaxDays,MaxPrecCount_MaxDay,MaxNumDays_MaxPrec

def DaysOverOrLower(Data,Dates,Value,flagMonths=False,Comparation='Over'):
    '''
    DESCRIPTION:

        This function calculates the days over or lower one specific value
        in every year or month and year of the series.
    _______________________________________________________________________

    INPUT:
        + Data: Data that needs to be counted.
        + Dates: Dates of the data, can be in datetime or string vector.
                 if the Dates are in a string vector it has to be in
                 yyyy/mm/dd.
        + Value: Value to search days over or lower.
        + flagMonths: flag to know if the count would be monthly.
                      True: to make the count monthly.
                      False: to make the count annualy.
        + Comparation: String with the comparation that is going to be 
                       done.
                       
                       It can recognize the following strings:

                             String           |       Interpretation 
                       'Over', 'over' or '>'  |             >
                       'Lower', 'lower' or '<'|             <
                              '>='            |             >=
                              '<='            |             <=

    _______________________________________________________________________
    
    OUTPUT:
    
        - results: number of days over or lower a value for every year or
                   month.
        - An: Dates where the operation was made.
    '''
    # Determine operation
    Comp = utl.Oper_Det(Comparation)
    # ----------------
    # Error managment
    # ----------------
    if Comp == -1:
        return -1, -1
    # Dates Error managment
    if isinstance(Dates[0],str):
        DatesP = DUtil.Dates_str2datetime(Dates)
        if list(DatesP)[0] == -1:
            return -1, -1
        elif isinstance(DatesP[0],datetime):
            Er = utl.ShowError('DaysOverOrLower','Hydro_Analysis','Dates are not in days')
            return Er, Er
    else:
        DatesP = Dates
        if isinstance(DatesP[0],datetime):
            Er = utl.ShowError('DaysOverOrLower','Hydro_Analysis','Dates are not in days')
            return Er, Er
    # ----------------
    # Dates managment
    # ----------------
    if flagMonths:
        An = DUtil.Dates_datetime2str(DatesP,Date_Format='%Y/%m')
        if list(An)[0] == -1:
            return -1,-1
    else:
        An = DUtil.Dates_datetime2str(DatesP,Date_Format='%Y')
        if list(An)[0] == -1:
            return -1,-1
    # ----------------
    # Calculations
    # ----------------
    results = []
    if flagMonths:      
        for i in range(DatesP[0].year,DatesP[-1].year+1):
            for j in range(1,13):
                if j < 10:
                    m = '%s/0%s' %(i,j)
                else:
                    m = '%s/%s' %(i,j)
                x = np.where(An == m)[0]
                P = Data[x]
                xx = np.where(Comp(P,Value))[0]
                if sum(~np.isnan(P)) >= 0.70*len(P):
                    results.append(len(xx))
                else:
                    results.append(np.nan)
    else:
        for i in range(DatesP[0].year,DatesP[-1].year+1):
            x = np.where(An == str(i))[0]

            P = Data[x]
            xx = np.where(Comp(P,Value))[0]
            if sum(~np.isnan(P)) >= 0.70*len(P):
                results.append(len(xx))
            else:
                results.append(np.nan)

    return results,An

def ConsDaysOverOrLower(Data,Dates,Value,Comparation='Over'):
    '''
    DESCRIPTION:
    
        This function calculates the number of consecutive days with 
        values over or lower a specific value and also gives the dates at
        the beginning and end of evey season.
    _______________________________________________________________________

    INPUT:
        + Data: Data that needs to be counted.
        + Dates: Dates of the data, can be in datetime or string vector.
                 if the Dates are in a string vector it has to be in
                 yyyy/mm/dd.
        + Value: Value to search days over or lower.
        + Comparation: String with the comparation that is going to be 
                       done.
                       
                       It can recognize the following strings:

                             String           |       Interpretation 
                       'Over', 'over' or '>'  |             >
                       'Lower', 'lower' or '<'|             <
                              '>='            |             >=
                              '<='            |             <=
    _______________________________________________________________________
    
    OUTPUT:

        The output is the dictionary results with the following keys:

        - TotalNumDays: Vector with total number of consecutive days 
                        above or below the value.
        - TotalPrecCount: Vector with the total of values during the
                          different number of days, works with
                          precipitation, averages needs to be 
                          determined manually.
        - TotalDateB: Starting dates of the different events.
        - MaxNumDays: Maximum number of consecutive days above 
                      or below the value.
        - MaxPrecCount_MaxDay: Maximum values in the maximum day.
        - MaxNumDays_MaxPrec: Maximum days in the maximum values.
        - DateMaxDays: Beginnig date of the maximum days count.
    '''
    # keys
    keys = ['TotalNumDays','TotalPrecCount','TotalDateB','MaxNumDays',\
        'MaxPrecCount','DateMaxDays','MaxPrecCount_MaxDay','MaxNumDays_MaxPrec']
    # Determine operation
    Comp = utl.Oper_Det(Comparation)
    # ----------------
    # Error managment
    # ----------------
    if Comp == -1:
        return -1
    # Dates Error managment
    if isinstance(Dates[0],str):
        DatesP = DUtil.Dates_str2datetime(Dates)
        if list(DatesP)[0] == -1:
            return -1
        elif isinstance(DatesP[0],datetime):
            Er = utl.ShowError('DaysOverOrLower','Hydro_Analysis','Dates are not in days')
            return Er
    else:
        DatesP = Dates
        if isinstance(DatesP[0],datetime):
            Er = utl.ShowError('DaysOverOrLower','Hydro_Analysis','Dates are not in days')
            return Er
    # --------------
    # Calculations
    # --------------
    results = dict()
    results['TotalNumDays'] = [] # List with all the days
    results['TotalPrecCount'] = [] # List for the total
    results['TotalDateB'] = [] # List of dates
    x = np.where(Comp(Data,Value))[0]
    if len(x) > 1:
        # Loop to calculate all the days
        DaysCount = 1 # Days counter
        PrecCount = Data[x[0]] # Value counter
        for i in range(1,len(x)):
            if x[i] == x[i-1]+1:
                DaysCount += 1
                PrecCount += Data[x[i]]
            else:
                results['TotalNumDays'].append(DaysCount)
                results['TotalPrecCount'].append(PrecCount)
                results['TotalDateB'].append(DatesP[x[i]-DaysCount])
                DaysCount = 0
                PrecCount = 0

            if i == len(x)-1:
                results['TotalNumDays'].append(DaysCount)
                results['TotalPrecCount'].append(PrecCount)
                results['TotalDateB'].append(DatesP[x[i]-DaysCount])
                DaysCount = 0
                PrecCount = 0

        results['TotalNumDays'] = np.array(results['TotalNumDays'])
        # Maximum number of days
        results['MaxNumDays'] = np.max(results['TotalNumDays'])
        x = np.where(results['TotalNumDays'] == results['MaxNumDays'])[0]

        results['TotalPrecCount'] = np.array(results['TotalPrecCount'])
        # Maximum value counter of number of days that was max
        results['MaxPrecCount_MaxDay'] = np.max(results['TotalPrecCount'][x])

        # Maximum value in those days
        results['MaxPrecCount'] = np.max(results['TotalPrecCount'])
        x = np.where(results['TotalPrecCount'] == results['MaxPrecCount'])[0]
        # Maximum number of days of the maximum value
        results['MaxNumDays_MaxPrec'] = np.max(results['TotalNumDays'][x])

        # Beginning date of the maximum 
        results['TotalDateB'] = np.array(results['TotalDateB'])
        xx = np.where(results['TotalNumDays'] == results['MaxNumDays'])[0]
        results['DateMaxDays'] = results['TotalDateB'][xx]
    else:
        for ikey,key in enumerate(keys):
            if ikey > 2:
                results[key] = 0
            else:
                results[key] = np.array([0])

    return results

def PrecCount(Prec,DatesEv,dt=1,M=60):
    '''
    DESCRIPTION:
        
        This functions calculates the duration of precipitation events 
        from composites.
    _________________________________________________________________________

    INPUT:
        :param PrecC:   A ndarray, Array with composite of precipitation.
        :param DatesEv: A ndarray, Array with all the events dates, format 
                                   yyyy/mm/dd-HHMM or datetime.
        :param dt:      An int, Time delta in minutes.
        :param M:       An int, Place where the maximum of precipitation 
                                is presented.
    _________________________________________________________________________

    OUTPUT:
        :return DurPrec:    A ndarray, Precipitation duration in hours.
        :return TotalPrec:  A ndarray, Total of precipitation in that time.
        :return IntPrec:    A ndarray, Event Intensity.
        :return MaxPrec:    A ndarray, Maximum of precipitation during the event.
        :return DatesEvst:  A ndarray, Date where the event begins.
        :return DatesEvend: A ndarray, Date where the event ends.
    '''

    # --------------------------------------
    # Error managment
    # --------------------------------------

    
    # --------------------------------------
    # Dates
    # --------------------------------------
    
    # Manage Data Size
    if len(DatesEv.shape) == 1:
        if not(isinstance(DatesEv[0],str)): 
            E = utl.ShowError('PrecCount','MeteoFunctions','Not dates given, review format')
            raise E
        EvN = 1 # Events number
    else:
        if not(isinstance(DatesEv[0][0],str)): 
            E = utl.ShowError('PrecCount','MeteoFunctions','Not dates given, review format')
            raise E
        EvN = len(DatesEv) # Events number


    # Variables for benining and end of the event
    DatesEvst_Aft = []
    DatesEvend_Aft = []
    for i in range(EvN):
        if isinstance(M,list):
            MP = M[i]
        else:
            MP = M
        x = [MP]
        # Minimum of precipitation
        if dt == 1:
            MinPrec = 0.001
        else:
            MinPrec = 0.10
        # Precipitation beginning
        if EvN == 1:
            xm = np.where(Prec[:MP]<=MinPrec)[0]
        else:
            xm = np.where(Prec[i,:MP]<=MinPrec)[0]

        k = 1
        a = len(xm)-1
        I = 10
        while k == 1:   
            if dt == 1:
                if a == -1:
                    xmm = 0
                    k = 2
                    break
                while a-I < 0:
                    I -= 1
                if xm[a] == xm[a-I]+I:
                    xmm = xm[a]
                    k = 2
                else:
                    a = a-1
                    if a == 0:
                        xmm = xm[0]
                        k = 2
            elif dt == 5:
                if a == -1:
                    xmm = 0
                    k = 2
                    break
                if xm[a] == xm[a-1]+1:
                    xmm = xm[a]
                    k = 2
                else:
                    a = a-1
                    if a == 0:
                        xmm = xm[0]
                        k = 2                       
        
        # Precipitation ending
        if EvN == 1:
            xM = np.where(Prec[x[0]+1:]<=MinPrec)[0]+x[0]+1
        else:
            xM = np.where(Prec[i,x[0]+1:]<=MinPrec)[0]+x[0]+1

        k = 1
        a = 0
        while k == 1:
            aa = len(xM)
            if aa == 1 or aa == 0:
                if EvN == 1:
                    xMM = len(Prec)-1
                else:
                    xMM = len(Prec[i,:])-1
                k = 2
                break
            if dt == 1:
                # print('a',a)
                try:
                    if xM[a] == xM[a+10]-10:
                        xMM = xM[a]
                        k = 2
                    else:
                        a = a+1
                        if a == len(xM)-1:
                            xMM = xM[len(xM)-1]
                            k = 2
                except:
                    try:
                        if xM[a] == xM[a+5]-5:
                            xMM = xM[a]
                            k = 2
                        else:
                            a = a+1
                            if a == len(xM)-1:
                                xMM = xM[len(xM)-1]
                                k = 2
                    except:
                        xMM = xM[a]
                        k = 2
                        
            elif dt == 5:
                if xM[a] == xM[a+1]-1:
                    xMM = xM[a]
                    k = 2
                else:
                    a = a+1
                    if a == len(xM)-1:
                        xMM = xM[len(xM)-1]
                        k = 2
            else:
                xMM = xM[a]
                k = 2
        if EvN == 1:
            DatesEvst_Aft.append(DatesEv[xmm])
            DatesEvend_Aft.append(DatesEv[xMM])
        else:
            DatesEvst_Aft.append(DatesEv[i][xmm])
            DatesEvend_Aft.append(DatesEv[i][xMM])
    
    DatesEvst = DUtil.Dates_str2datetime(DatesEvst_Aft,Date_Format=None)
    DatesEvend = DUtil.Dates_str2datetime(DatesEvend_Aft,Date_Format=None)
    DatesEvst_Aft = np.array(DatesEvst_Aft)
    DatesEvend_Aft = np.array(DatesEvend_Aft)
    
    # ---------------
    # Calculations
    # ---------------
    # Variables
    DurPrec = []
    TotalPrec = []
    IntPrec = []
    IntPrecMax = []
    MaxPrec = []
    Pindex = []
    TasaPrec = []
    DatesMax = []

    if EvN == 1:
        # Verify event data
        q = sum(~np.isnan(Prec))
        if q <= len(DatesEv)*.90:
            DurPrec.append(np.nan)
            TotalPrec.append(np.nan)
            IntPrec.append(np.nan)
            IntPrecMax.append(np.nan)
            MaxPrec.append(np.nan)
            Pindex.append(np.nan)
            TasaPrec.append(np.nan)
            DatesMax.append(np.nan)
        else:
            # ------------------------
            # Rainfall duration
            # ------------------------
            Dxi = np.where(DatesEv == DatesEvst_Aft)[0]
            Dxf = np.where(DatesEv == DatesEvend_Aft)[0]
            DurPrec.append((Dxf[0]-Dxi[0]+1)*dt/60) # Duración en horas
            # Se verifica que haya información
            q = sum(~np.isnan(Prec[Dxi[0]:Dxf[0]+1]))
            if q <= len(Prec[Dxi[0]:Dxf[0]+1])*.50:
                DurPrec[-1] = np.nan
                TotalPrec.append(np.nan)
                IntPrec.append(np.nan)
                IntPrecMax.append(np.nan)
                MaxPrec.append(np.nan)
                Pindex.append(np.nan)
                TasaPrec.append(np.nan)
                DatesMax.append(np.nan)
            else:
                # ------------------------
                # Precipitation total
                # ------------------------
                TotalP = np.nansum(Prec[Dxi[0]:Dxf[0]+1])
                TotalPrec.append(TotalP)
                # -----------------------------
                # Mean Intensity precipitation
                # -----------------------------
                IntPrec.append(TotalP/DurPrec[-1])
                if IntPrec[-1] >= 100:
                    DurPrec[-1] = np.nan
                    TotalPrec[-1] = np.nan
                    IntPrec[-1] = np.nan
                    IntPrecMax.append(np.nan)
                    MaxPrec.append(np.nan)
                    Pindex.append(np.nan)
                    TasaPrec.append(np.nan)
                    DatesMax.append(np.nan)
                else:
                    # ------------------------
                    # Maximum Precipitation
                    # ------------------------
                    MaxPrec.append(np.nanmax(Prec[Dxi[0]:Dxf[0]+1]))
                    # -----------------------------
                    # Max Intensity precipitation
                    # -----------------------------
                    IntPrecMax.append(MaxPrec[-1]/(dt/60))
                    # ------------------------
                    # P Index
                    # ------------------------
                    Pindex.append(IntPrecMax[-1]/IntPrec[-1])
                    # ------------------------
                    # Dates Max 
                    # ------------------------
                    x = np.where(Prec[Dxi[0]:Dxf[0]]==MaxPrec[-1])[0][-1]
                    DatesMax.append(DatesEv[Dxi[0]+x])
                    DatesMax[-1] = DUtil.Dates_str2datetime([DatesMax[-1]],Date_Format=None)[0]
                    # ------------------------
                    # Precipitation Rate
                    # ------------------------
                    TasaPrec.append((MaxPrec[-1]-Prec[Dxi[0]])/((x)*dt/60))

        DatesEvMax = np.array(DatesMax)[0]
        DurPrec = np.array(DurPrec)[0]
        TotalPrec = np.array(TotalPrec)[0]
        IntPrec = np.array(IntPrec)[0]
        IntPrecMax = np.array(IntPrecMax)[0]
        MaxPrec = np.array(MaxPrec)[0]
        Pindex = np.array(Pindex)[0]
        TasaPrec = np.array(TasaPrec)[0]

    else:
        for i in range(len(DatesEv)):
            # Verify event data
            q = sum(~np.isnan(Prec[i]))
            if q <= len(DatesEv[i])*.90:
                DurPrec.append(np.nan)
                TotalPrec.append(np.nan)
                IntPrec.append(np.nan)
                IntPrecMax.append(np.nan)
                MaxPrec.append(np.nan)
                Pindex.append(np.nan)
                TasaPrec.append(np.nan)
                DatesMax.append(np.nan)
            else:
                # ------------------------
                # Rainfall duration
                # ------------------------
                Dxi = np.where(DatesEv[i] == DatesEvst_Aft[i])[0]
                Dxf = np.where(DatesEv[i] == DatesEvend_Aft[i])[0]
                DurPrec.append((Dxf[0]-Dxi[0]+1)*dt/60) # Duración en horas
                # Se verifica que haya información
                q = sum(~np.isnan(Prec[i,Dxi[0]:Dxf[0]+1]))
                if q <= len(Prec[i,Dxi[0]:Dxf[0]+1])*.50:
                    DurPrec[-1] = np.nan
                    TotalPrec.append(np.nan)
                    IntPrec.append(np.nan)
                    IntPrecMax.append(np.nan)
                    MaxPrec.append(np.nan)
                    Pindex.append(np.nan)
                    TasaPrec.append(np.nan)
                    DatesMax.append(np.nan)
                else:
                    # ------------------------
                    # Precipitation total
                    # ------------------------
                    TotalP = np.nansum(Prec[i,Dxi[0]:Dxf[0]+1])
                    TotalPrec.append(TotalP)
                    # -----------------------------
                    # Mean Intensity precipitation
                    # -----------------------------
                    IntPrec.append(TotalP/DurPrec[-1])
                    if IntPrec[-1] >= 100:
                        DurPrec[-1] = np.nan
                        TotalPrec[-1] = np.nan
                        IntPrec[-1] = np.nan
                        IntPrecMax.append(np.nan)
                        MaxPrec.append(np.nan)
                        Pindex.append(np.nan)
                        TasaPrec.append(np.nan)
                        DatesMax.append(np.nan)
                    else:
                        # ------------------------
                        # Maximum Precipitation
                        # ------------------------
                        MaxPrec.append(np.nanmax(Prec[i,Dxi[0]:Dxf[0]+1]))
                        # -----------------------------
                        # Max Intensity precipitation
                        # -----------------------------
                        IntPrecMax.append(MaxPrec[-1]/(5/60))
                        # ------------------------
                        # P Index
                        # ------------------------
                        Pindex.append(IntPrecMax[-1]/IntPrec[-1])
                        # ------------------------
                        # Dates Max 
                        # ------------------------
                        x = np.where(Prec[i,Dxi[0]:Dxf[0]]==MaxPrec[-1])[0][-1]
                        DatesMax.append(DatesEv[i,Dxi[0]+x])
                        DatesMax[-1] = DUtil.Dates_str2datetime([DatesMax[-1]],Date_Format=None)[0]
                        # ------------------------
                        # Precipitation Rate
                        # ------------------------
                        TasaPrec.append((MaxPrec[-1]-Prec[i,Dxi[0]])/((x)*dt/60))

        DatesEvMax = np.array(DatesMax)
        DurPrec = np.array(DurPrec)
        TotalPrec = np.array(TotalPrec)
        IntPrec = np.array(IntPrec)
        IntPrecMax = np.array(IntPrecMax)
        MaxPrec = np.array(MaxPrec)
        Pindex = np.array(Pindex)
        TasaPrec = np.array(TasaPrec)


    Results = {'DurPrec':DurPrec,'TotalPrec':TotalPrec,'IntPrec':IntPrec,
    'MaxPrec':MaxPrec,'DatesEvst':DatesEvst,'DatesEvend':DatesEvend,
    'DatesEvMax':DatesEvMax,'Pindex':Pindex,'IntPrecMax':IntPrecMax,'TasaPrec':TasaPrec}
    return Results



