# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:20:19 2024

@author: Thommes Eliott
"""

# Soil library


# Other Lib


# Custom Lib
from GeometryLib import Surface2D
from PlotLib import ParamPLT


"""
Classe de sol
"""

class SoilEasy(Surface2D):
    def __init__(self, LNode, Axis, UnitWeight, BDefaultColor, Name=None):
        super().__init__(LNode, Axis, Name)
        self.UnitWeight = UnitWeight
        self.BDefaultColor = BDefaultColor

    @property
    def getUnitWeight(self):
        return self.UnitWeight

    @getUnitWeight.setter
    def getUnitWeight(self, UnitWeight):
        self.UnitWeight = UnitWeight

    @property
    def getBDefaultColor(self):
        return self.BDefaultColor

    @getBDefaultColor.setter
    def getBDefaultColor(self, BDefaultColor):
        self.BDefaultColor = BDefaultColor

    def PLT2DSoil(self, paramPLT):
        if self.getBDefaultColor:
            paramPLT.getColour = 'darkgoldenrod'
        self.PLT2DSurface(paramPLT)


class Soil2D(SoilEasy):
    def __init__(self, LNode, Axis, UnitWeight, BDefaultColor, Name=None):
        super().__init__(LNode, Axis, UnitWeight, BDefaultColor, Name)

    def ToContinue():
        return False

    "Définir des layers"


class Geotech2D:
    def __init__(self):
        self.Val = True
        self.Layer = []  # Liste de Soil2D ou SoilEasy

    'Calcul'
        

"""
class Soil3DEasy(Volume)
"""

