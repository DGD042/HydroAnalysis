# -*- coding: utf-8 -*-
#______________________________________________________________________________
#______________________________________________________________________________
#
#                       Coded by Daniel González Duque
#______________________________________________________________________________
#______________________________________________________________________________

'''

This class have different routines for hydrological and 
thermo-dynamical analysis in relation with climatology and 
hydrology.

This package also graph all the different intervals required from the
given data.

____________________________________________________________________________
This class is of free use and can be modify, if you have some 
problem please contact the programmer to the following e-mails:

- daniel.gonzalez@vanderbilt.edu
- danielgondu@gmail.com 
- dagonzalezdu@unal.edu.co
____________________________________________________________________________

'''

try:
    from HydroAnalysis.src import *
    from HydroAnalysis.HydroAnalysis import HydroAnalysis 
    from HydroAnalysis.HydroPlotter import HydroPlotter
except ImportError:
    from HydroAnalysis.src import *
    from HydroAnalysis import HydroAnalysis
    from HydroAnalysis import HydroPlotter

