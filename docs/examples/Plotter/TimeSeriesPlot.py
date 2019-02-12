# -*- coding: utf-8 -*-
#______________________________________________________________________________
#______________________________________________________________________________
#
#                       Coded by Daniel González Duque
#______________________________________________________________________________
#______________________________________________________________________________

'''

This is an example of how to use the Hydro Plotter package to plot a time
series.
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
import HydroAnalysis.HydroPlotter as HP

# --------------------------
# Parameters
# --------------------------
PathImg = 'TimeSeriesImgTest/'
Name = 'test.png'
# --------------------------
# For Single line Graphs
# --------------------------
# Creating data
Dates = np.array([date(2000,1,1)+timedelta(i) for i in range(365*3)])
Values = np.random.normal(0,1,size=Dates.shape[0])

# Plot
HPI = HP.HydroPlotter(dpi=120) # Create an instance of the HydroPlotter Class

# Call the method to create the time series plot
HPI.TimeSeriesPlot(Dates,Values,'Values',Title='Random Series',PathImg=PathImg,
        Name='SingleLineTest.png',Date_Format='%Y/%m')


# --------------------------
# Multiple line Graphs
# --------------------------
# Creating data
Dates = np.array([date(2000,1,1)+timedelta(i) for i in range(365*3)])
Values = np.array([np.random.normal(0,1,size=(Dates.shape[0],)),
        np.random.normal(0,1,size=(Dates.shape[0],))+2,
        np.random.normal(0,1,size=(Dates.shape[0],))-2,
        ])
# In this case we need to include the labels of the graphs
Labels = ['S1','S2','S3']

# Plot
HPI = HP.HydroPlotter(dpi=120,loc=1) # Create an instance of the HydroPlotter Class

# Call the method to create the time series plot
# As we did not called the 
HPI.TimeSeriesPlot(Dates,Values,'Values',Title='Random Series',PathImg=PathImg,
        Name='MultipleSeriesTest.png',Labels=Labels,
        Date_Format='%d/%m/%y')

# --------------------------------
# Multiple line Graphs set Colors
# --------------------------------
# In this case we need to include the labels of the graphs
Labels = ['S1','S2','S3']
# Colors for the set
Colors = ['b','k','g']

# Plot
HPI = HP.HydroPlotter(dpi=120,loc=1) # Create an instance of the HydroPlotter Class

# Call the method to create the time series plot
# As we did not called the 
HPI.TimeSeriesPlot(Dates,Values,'Values',Title='Random Series',PathImg=PathImg,
        Name='MultipleSeriesColorsTest.png',Labels=Labels,Colors=Colors,
        Date_Format='%d/%m/%y')

# ------------------------------------
# Multiple line Graphs set Line Style
# ------------------------------------
# In this case we need to include the labels of the graphs
Labels = ['S1','S2','S3']
# LineStyle for the set
Linestyles = ['-','-.','--']

# Plot
HPI = HP.HydroPlotter(dpi=120,loc=1) # Create an instance of the HydroPlotter Class

# Call the method to create the time series plot
# As we did not called the 
HPI.TimeSeriesPlot(Dates,Values,'Values',Title='Random Series',PathImg=PathImg,
        Name='MultipleSeriesLinestyleTest.png',Labels=Labels,Linestyles=Linestyles,
        Date_Format='%d/%m/%y')
