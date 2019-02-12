# What is HydroAnalysis?

HydroAnalysis is a Python library that carries out some simple hydrological and thermodynamical analysis. It supports making Diurnal and Annual Cycles from hourly and monthly data, calculating and fitting vertical temperature profiles and estimating evaportanspiration with several methods. Furthermore the HydroPlotter library has all kinds of plotting methods to get the information plotted in a nice way in the desired directory.

It is important to note that the modules do not work with Pandas DataFrames, there is still work in including this modules 

# Current Status

**It is still a work in progress and some of the submodules are deactivated for now.**

For the created classes, methods and functions are being replace for a better way of presenting all the documentation, I estimate a month to get everything up and running, having the installation on PyPy as well.


# Installation

There is still no setup installation of the packages so far, I'm still working on it

# Basic Usage

For example scripts you can visit the [example scripts](https://github.com/DGD042/HydroAnalysis/tree/master/docs/examples).
 
## Diurnal Cycle

To calculate the Diurnal Cycle of an hourly series first the series implemented must be complete, including missing data, this application can give you the diurnal cycle of the whole series as well as the individual monthly cycles in a response as a dictionary, It would give as well 2 graphs showing this information. The user can change some of the graphs parameters and turn off the generation of the graphs as well. For more information please see [this example](https://github.com/DGD042/HydroAnalysis/blob/master/docs/examples/MeteoAnalysis/Cycles.py). Further documentation would be generated.
