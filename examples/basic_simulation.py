# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:21:38 2024

@author: Thommes Eliott
"""

# Technologie des bétons : TP Coffrage

import math

from ElementLib import Element, CrossSectionEasy, Support
from GeometryLib import Node, AddNode
from FormworkLib import *
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, PLTScreenMaximize
from SoilLib import SoilEasy

# Delete olds plots
CloseAllPlots()

"""
Ex 1
"""
# Création des noeuds
nodes = []
n1 = AddNode(nodes, 0, 0, 0)
n2 = AddNode(nodes, 0, 0, -3.65)
n3 = AddNode(nodes, -0.7, 0, -3.75)
n4 = AddNode(nodes, -0.7, 0, -4.1)
n5 = AddNode(nodes, 0, 0, -4.1)
n6 = AddNode(nodes, 0, 0, -3.95)
n7 = AddNode(nodes, 0.35, 0, -3.95)
n8 = AddNode(nodes, 0.35, 0, -4.1)
n9 = AddNode(nodes, 1.05, 0, -4.1)
n10 = AddNode(nodes, 1.05, 0, -3.75)
n11 = AddNode(nodes, 0.35, 0, -3.65)
n12 = AddNode(nodes, 0.35, 0, 0)

# Création des segments du coffrage
lines = [PLine(n1, n2), PLine(n2, n3), PLine(n3, n4), PLine(n4, n5),
         PLine(n5, n6), PLine(n6, n7), PLine(n7, n8), PLine(n8, n9),
         PLine(n9, n10), PLine(n10, n11), PLine(n11, n12)]
# Règle de numérotation selon le sens anti-horaire

# Définition de la surface libre du béton
freesurface = FreeSurface([n1, n12])

# Définition des paramètres du béton
beton = ConcreteData(PVolumique=23*10**3, PouringSpeed=1.7, PouringT=10)

# Paramétrage du solver et résolution
paramsolver = ParamSolver(SolverType=2, dx=0)
CmptConcretePressures(lines, freesurface, beton, paramsolver)

Templines = [lines[0], lines[1], lines[2], lines[4], lines[5], lines[6], lines[8], lines[9], lines[10]]

# Affichage du coffrage
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Forme du coffrage", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
#PLTScreenMaximize()

# Remplissage du coffrage
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getLegends = ["Béton"]
PLT2DFormworkFill(lines, freesurface, paramPLT)
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Remplissage du coffrage", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
#PLTScreenMaximize()

# Affichage des pressions
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getLegends = ["Béton"]
PLT2DFormworkFill(lines, freesurface, paramPLT)
paramPLT.getLegends = ["Pressions"]
paramPLT.getScale = 10**(-5)
PLT2DFormworkPressure(Templines, freesurface, paramPLT)
paramPLT.getColour = 'black'
paramPLT.getLineType = 1
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Pressions sur le coffrage", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
#PLTScreenMaximize()

# Affichage des résultantes
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getLegends = ["Béton"]
PLT2DFormworkFill(lines, freesurface, paramPLT)
paramPLT.getLegends = ["Résultantes"]
paramPLT.getScale = 10**(-5)
PLT2DFormworkResultant(Templines, freesurface, paramPLT)
paramPLT.getColour = 'black'
paramPLT.getLineType = 1
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Résultantes des pressions sur le coffrage", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
#PLTScreenMaximize()

# Affichage des pressions et des résultantes
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getLegends = ["Béton"]
PLT2DFormworkFill(lines, freesurface, paramPLT)
paramPLT.getLegends = ["Pressions"]
paramPLT.getScale = 10**(-5)
PLT2DFormworkPressure(Templines, freesurface, paramPLT)
paramPLT.getLegends = ["Résultantes"]
paramPLT.getScale = 10**(-5)
PLT2DFormworkResultant(Templines, freesurface, paramPLT)
paramPLT.getColour = 'black'
paramPLT.getLineType = 1
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Résultantes et pressions sur le coffrage", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
#PLTScreenMaximize()

# Affichage du systèmes de soutènements
paramPLT = ParamPLT(colour='black', linetype=1, marker=0, linesize=2,
                    fontsize=20)
StartPlots()
paramPLT.getLegends = ["Coffrage"]
PLT2DFormworkLines(lines, paramPLT)
paramPLT.getLegends = ["Béton"]
PLT2DFormworkFill(lines, freesurface, paramPLT)

# Soil
SoilNodes = []
n1 = AddNode(SoilNodes, -2.75, 0, -4.1)
n2 = AddNode(SoilNodes, -2.75, 0, -4.6)
n3 = AddNode(SoilNodes, 3, 0, -4.6)
n4 = AddNode(SoilNodes, 3, 0, -4.1)
Soil = SoilEasy(SoilNodes, Axis=[1, 3], UnitWeight=20*10**3,
                BDefaultColor=True, Name='Sol')

paramPLT.getLegends = ["Sol"]
paramPLT.getColour = 'slategray'
Soil.PLT2DSoil(paramPLT)

# Ballast
BallastNodes1 = []
n1 = AddNode(BallastNodes1, 0.35, 0, -2.965)
n2 = AddNode(BallastNodes1, 0.35, 0, -3.65)
n3 = AddNode(BallastNodes1, 1.05, 0, -3.75)
n4 = AddNode(BallastNodes1, 1.05, 0, -3.065)
Ballast1 = SoilEasy(BallastNodes1, Axis=[1, 3], UnitWeight=20*10**3,
                    BDefaultColor=False, Name='Rock')
paramPLT.getLegends = ["Ballasts"]
paramPLT.getColour = 'darkorange'
paramPLT.getHatch = [2, 2]
Ballast1.PLT2DSoil(paramPLT)

BallastNodes2 = []
n1 = AddNode(BallastNodes2, 0, 0, -2.965)
n2 = AddNode(BallastNodes2, 0, 0, -3.65)
n3 = AddNode(BallastNodes2, -0.7, 0, -3.75)
n4 = AddNode(BallastNodes2, -0.7, 0, -3.065)
Ballast2 = SoilEasy(BallastNodes2, Axis=[1, 3], UnitWeight=20*10**3,
                    BDefaultColor=False, Name='Rock')
paramPLT.getColour = 'darkorange'
paramPLT.getHatch = [2, 2]
Ballast2.PLT2DSoil(paramPLT)

# Bracing
n1 = Node(0, 0, -2.35)
n2 = Node(0-1.75/math.tan(math.radians(35)), 0, -4.1)
sectionEtai = CrossSectionEasy()
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai1 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')

paramPLT.getLegends = ["Etais"]
paramPLT.getColour = 'slategray'
paramPLT.getMarkerSize = 0.03
Etai1.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

n1 = Node(0.35, 0, -2.35)
n2 = Node(0.35+1.75/math.tan(math.radians(35)), 0, -4.1)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai2 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
Etai2.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

n1 = Node(-0.7, 0, -3.75)
n2 = Node(-0.7-0.35/math.tan(math.radians(30)), 0, -4.1)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai3 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
Etai3.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

n1 = Node(1.05, 0, -3.75)
n2 = Node(1.05+0.35/math.tan(math.radians(30)), 0, -4.1)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai4 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
Etai4.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

# Coffrage perdu
n1 = Node(0.35, 0, -4.1)
n2 = Node(0.35, 0, -3.95)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=False, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=False, DDL_Mz=False)
Support2.getNSupport = n2
Etai4 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
paramPLT.getLegends = ["Coffrage perdu"]
paramPLT.getColour = 'burlywood'
Etai4.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

n1 = Node(0.35, 0, -3.95)
n2 = Node(0, 0, -3.95)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai4 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
Etai4.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

n1 = Node(0, 0, -3.95)
n2 = Node(0, 0, -4.1)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Etai4 = Element(node1=n1, node2=n2, section=sectionEtai,
                CondAppuieN1=Support1, CondAppuieN2=Support2,
                Name='Etai', Color='r')
Etai4.PLT2DElement(axis=[1, 3], paramPLT=paramPLT, BSupport=True,
                   dAbsc=1, dOrdo=0)

# Support
paramPLT.getColour = 'slategray'
n1 = Node(-0.7, 0, -4.1)
n2 = Node(1.05, 0, -4.1)
Support1 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support1.getNSupport = n1
Support2 = Support(x=0, y=0, z=0, DDL_Dx=False, DDL_Dy=False, DDL_Dz=False,
                   DDL_Mx=False, DDL_My=True, DDL_Mz=False)
Support2.getNSupport = n2
Support1.PLT2DAppui(axis=[1,3], paramPLT=paramPLT, dAbsc=1, dOrdo=0)
Support2.PLT2DAppui(axis=[1,3], paramPLT=paramPLT, dAbsc=1, dOrdo=0)


paramPLT.getColour = 'black'
paramPLT.getLineType = 1
paramPLT.getGrid(Axis=-1)
paramPLT.getLabelTitle(Title="Ex 1: Système de soutènement", XLabel="X [m]", YLabel="Z [m]")
paramPLT.getAspect = True
PLTShow(paramPLT)
