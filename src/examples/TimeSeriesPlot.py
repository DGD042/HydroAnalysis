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
# HydroAnalysis
import HydroAnalysis as HA

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
HP = HA.HydroPlotter.HydroPlotter() # Create an instance of the HydroPlotter Class

# Call the method to create the time series plot
HP.TimeSeriesPlot(Dates,Values,'Values',Title='Random Series',PathImg=PathImg,
        Date_Format='%Y/%m')

