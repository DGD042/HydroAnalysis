# -*- coding: utf-8 -*-
#______________________________________________________________________________
#______________________________________________________________________________
#
#                       Coded by Daniel González Duque
#______________________________________________________________________________
#______________________________________________________________________________

'''

This is an example of how to use the HydroAnalysis to analyse cicles in 
different time scales
____________________________________________________________________________
This class is of free use and can be modify, if you have some 
problem please contact the programmer to the following e-mails:

- daniel.gonzalez@vanderbilt.edu
- danielgondu@gmail.com 
- dagonzalezdu@unal.edu.co
____________________________________________________________________________

'''

# ---------
# Imports
# ---------
# Data Management
import numpy as np
import matplotlib.pyplot as plt
# Time
from datetime import date, datetime, timedelta
# System
import sys
import os
sys.path.append(os.getcwd())
# HydroAnalysis
import HydroAnalysis.HydroAnalysis as HA
import HydroAnalysis.HydroPlotter as HP

# --------------------------
# Parameters
# --------------------------
PathImg = 'TimeSeriesImgTest/'
# --------------------------
# Import Data
# --------------------------
# For this exercise a synthetic time series would be created
# Hourly 10 year date vector
Dates = np.array([datetime(2000,1,1,0,0)+timedelta(0,i*3600) for i in range((365*10)*24+3*24)])
x = np.arange(len(Dates))
# Values
noise = np.random.normal(0,0.5,size=len(Dates))*2
Values = 10*np.sin(2*np.pi*x/24) + 20*np.cos(np.pi*x/(45*24)) + noise

# Time series plot of the first 10 days
Days = 365
HPI = HP.HydroPlotter(dpi=120) # Create an instance of the HydroPlotter Class

HPI.TimeSeriesPlot(Dates[:10*Days],Values[:10*Days],'Values',Title='Synthetic Time Series',PathImg=PathImg,
        Name='TimeSeries.png',Date_Format='%d/%m/%y %H:%M')

# Use HA to Calculate the Diurnal Cycle from the hourly data
HAi = HA.HydroAnalysis(DateH=Dates,VarH=Values,DTH=24,PathImg=PathImg,
        Info=['DiurnalCycle','Values','Values','Values [-]','k'])
RDCycle = HAi.CiclD()

