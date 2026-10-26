# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 09:24:39 2024

@author: Thommes Eliott
"""

# Formwork library

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from GeometryLib import Node, Line, Surface, AddNode, Compo2Angle
from LoadingLib import PLine, PNode


# Surface du béton (Hérite de surface car peut-être différentes surfaces)

class FreeSurface(Surface):
    """FreeSurface Class."""

    def __init__(self, LNode):
        super().__init__(LNode)  # Listes de noeuds
        self.FreeSurfaceHeight = LNode[0].getz
        self.DefinitionFromHeight = False

    @property
    def getNodes(self):
        return self.LNode

    @getNodes.setter
    def getNodes(self, LNode):
        self.LNode = LNode
        self.FreeSurfaceHeight = LNode[0].getz
        self.DefinitionFromHeight = False

    @property
    def getFreeSurface(self):
        return self.FreeSurfaceHeight

    @getFreeSurface.setter
    def getFreeSurface(self, val):
        self.FreeSurfaceHeight = val
        self.DefinitionFromHeight = True

    @property
    def getDefFromHeight(self):
        return self.DefinitionFromHeight

    @property
    def __repr__(self):
        return f"FreeSurface({self.getNodes})"

    # Verification of planar surface
    @property
    def Verif(self):
        height = self.getFreeSurface
        status = all(node.getz == height for node in self.getNodes)
        if status:
            print("OK: Free surface is planar")
        else:
            print("Error: Free surface is not horizontal")
        return status

    # Verification of boundaries for surface height
    def VerifBound(self, Plines):
        FreeSurfaceHeight = self.getFreeSurface
        Nodes = []
        for Pline in Plines:
            Nodes.append(Pline.getn1)
            Nodes.append(Pline.getn2)

        MinHeight = min(node.getz for node in Nodes)
        MaxHeight = max(node.getz for node in Nodes)

        if MaxHeight >= FreeSurfaceHeight >= MinHeight:
            print("OK: Free surface is within bounds")
            return True
        else:
            print("Error: Free surface is outside bounds")
            return False


# Definition of concrete properties and pouring data
class ConcreteData:
    def __init__(self, PVolumique, PouringSpeed, PouringT):
        self.Gamma = PVolumique
        self.PouringSpeed = PouringSpeed
        self.PouringT = PouringT

    @property
    def getGamma(self):
        return self.Gamma

    @getGamma.setter
    def getGamma(self, val):
        self.Gamma = val

    @property
    def getPSpeed(self):
        return self.PouringSpeed

    @getPSpeed.setter
    def getPSpeed(self, val):
        self.PouringSpeed = val

    @property
    def getPouringT(self):
        return self.PouringT

    @getPouringT.setter
    def getPouringT(self, val):
        self.PouringT = val


# Définition des paramètres de résolution
class ParamSolver:
    def __init__(self, SolverType, dx):
        self.SolverType = SolverType
        self.dx = dx

    @property
    def getdx(self):
        return self.dx

    @getdx.setter
    def getdx(self, val):
        self.dx = val

    @property
    def getSolver(self):
        return self.SolverType

    @getSolver.setter
    def getSolver(self, val):
        self.SolverType = val


# Functions to calculate pressure for a Pline
def PComputerHydrostat(Pline, freesurface, beton):
    # Creates the differents PNodes
    x1 = Pline.getn1.getx
    y1 = Pline.getn1.gety
    z1 = Pline.getn1.getz
    x2 = Pline.getn2.getx
    y2 = Pline.getn2.gety
    z2 = Pline.getn2.getz
    Pnode1 = PNode(x1, y1, z1)
    Pnode2 = PNode(x2, y2, z2)

    FreeSurfaceHeigh = freesurface.getFreeSurface
    # Add first Pnode
    Pline.getPNodes = [Pnode1]
    # Add a Pnode if went through interface
    if (z1 > FreeSurfaceHeigh > z2) or (z2 > FreeSurfaceHeigh > z1):
        x = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        y = y1+(y2-y1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        z = FreeSurfaceHeigh
        PnodeInter = PNode(x, y, z)
        Pline.getPNodes.append(PnodeInter)
    # Add last Pnode
    Pline.getPNodes.append(Pnode2)

    # Compute the pressure for each Pnodes
    for Pnode in Pline.getPNodes:
        depth = FreeSurfaceHeigh - Pnode.getz
        if depth > 0:
            Pressure = beton.Gamma*depth
        else:
            Pressure = 0  # No pressure above the free surface
        Pnode.getP = Pressure


def PComputerMur(Pline, freesurface, beton):
    # Creates the differents PNodes
    x1 = Pline.getn1.getx
    y1 = Pline.getn1.gety
    z1 = Pline.getn1.getz
    x2 = Pline.getn2.getx
    y2 = Pline.getn2.gety
    z2 = Pline.getn2.getz
    Pnode1 = PNode(x1, y1, z1)
    Pnode2 = PNode(x2, y2, z2)

    FreeSurfaceHeigh = freesurface.getFreeSurface
    if beton.getPSpeed <= 2.1:
        e = (7.33+(144*beton.getPSpeed)/(3.2+0.18*beton.getPouringT))*10**3
    else:
        e = (7.33+(212+44.9*beton.getPSpeed)/(3.2+0.18*beton.getPouringT))*10**3
    Pmax = min(e, 98000)
    PMaxHeighRel = Pmax/24000
    PMaxHeigh = FreeSurfaceHeigh - PMaxHeighRel

    # Add first Pnode
    Pline.getPNodes = [Pnode1]
    # Add a Pnode if went through interface
    if (z1 > FreeSurfaceHeigh > z2) or (z2 > FreeSurfaceHeigh > z1):
        x = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        y = y1+(y2-y1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        z = FreeSurfaceHeigh
        PnodeInter = PNode(x, y, z)
        Pline.getPNodes.append(PnodeInter)
    # Add a Pnode at max pressure
    if (z1 > PMaxHeigh > z2) or (z2 > PMaxHeigh > z1):
        x = x1+(x2-x1)/(z2-z1)*(PMaxHeigh-z1)
        y = y1+(y2-y1)/(z2-z1)*(PMaxHeigh-z1)
        z = PMaxHeigh
        PnodeInter = PNode(x, y, z)
        Pline.getPNodes.append(PnodeInter)
    # Add last Pnode
    Pline.getPNodes.append(Pnode2)

    # Compute the pressure for each Pnodes
    for Pnode in Pline.getPNodes:
        depth = FreeSurfaceHeigh - Pnode.getz
        if depth > 0:
            Pressure = min(Pmax, 24000*depth)*beton.Gamma/24000
        else:
            Pressure = 0  # No pressure above the free surface
        Pnode.getP = Pressure


def PComputerColonne(Pline, freesurface, beton):
    # Creates the differents PNodes
    x1 = Pline.getn1.getx
    y1 = Pline.getn1.gety
    z1 = Pline.getn1.getz
    x2 = Pline.getn2.getx
    y2 = Pline.getn2.gety
    z2 = Pline.getn2.getz
    Pnode1 = PNode(x1, y1, z1)
    Pnode2 = PNode(x2, y2, z2)

    FreeSurfaceHeigh = freesurface.getFreeSurface
    e = (7.33+(144*beton.getPSpeed)/(3.2+0.18*beton.getPouringT))*10**3
    Pmax = min(e, 147000)
    PMaxHeighRel = Pmax/24000
    PMaxHeigh = FreeSurfaceHeigh - PMaxHeighRel

    # Add first Pnode
    Pline.getPNodes = [Pnode1]
    # Add a Pnode if went through interface
    if (z1 > FreeSurfaceHeigh > z2) or (z2 > FreeSurfaceHeigh > z1):
        x = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        y = y1+(y2-y1)/(z2-z1)*(FreeSurfaceHeigh-z1)
        z = FreeSurfaceHeigh
        PnodeInter = PNode(x, y, z)
        Pline.getPNodes.append(PnodeInter)
    # Add a Pnode at max pressure
    if (z1 > PMaxHeigh > z2) or (z2 > PMaxHeigh > z1):
        x = x1+(x2-x1)/(z2-z1)*(PMaxHeigh-z1)
        y = y1+(y2-y1)/(z2-z1)*(PMaxHeigh-z1)
        z = PMaxHeigh
        PnodeInter = PNode(x, y, z)
        Pline.getPNodes.append(PnodeInter)
    # Add last Pnode
    Pline.getPNodes.append(Pnode2)

    # Compute the pressure for each Pnodes
    for Pnode in Pline.getPNodes:
        depth = FreeSurfaceHeigh - Pnode.getz
        if depth > 0:
            Pressure = min(Pmax, 24000*depth)*beton.Gamma/24000
        else:
            Pressure = 0  # No pressure above the free surface
        Pnode.getP = Pressure


# Function to compute pressure for Pline
def CmptConcretePressures(Plines, freesurface, beton, paramsolver):
    for Pline in Plines:
        if paramsolver.getSolver == 0:  # Solveur hydrostatique
            PComputerHydrostat(Pline, freesurface, beton)
        elif paramsolver.getSolver == 1:  # Solveur Mur
            PComputerMur(Pline, freesurface, beton)
        elif paramsolver.getSolver == 2:  # Solveur Colonne
            PComputerColonne(Pline, freesurface, beton)
        else:                           # Solveur hydrostatique by default
            PComputerHydrostat(Pline, freesurface, beton)



# Print the pressure values
def PrintPressure(Plines):
    for Pline in Plines:
        for Pnode in Pline.getPNodes:
            print(f"Pressure at ({Pnode.getx},{Pnode.gety},{Pnode.getz}) : {Pnode.getP:.2f} Pa")


# Function to plot 2D formwork
# By default (x-z)

def PLT2DFormworkLines(Plines, paramPLT):
    for Pline in Plines:
        axis = [1,3]
        paramPLT.getColour = 'k'
        paramPLT.getLineType = 1
        Pline.PLT2DLine(axis, paramPLT)


def PLT2DFormworkFill(Plines, freesurface, paramPLT):
    # Collect x and z values for filling the area (assumed to be closed shape)
    x_fill = []
    z_fill = []

    # Get the nodes of the free surface
    FreeSurfaceHeigh = freesurface.getFreeSurface

    for Pline in Plines:
        if Pline.getn1.getz < FreeSurfaceHeigh or Pline.getn2.getz < FreeSurfaceHeigh:
            # Append coordinates for the fill
            # mais remplace les noeuds qui sont juste au dessus de la surface.
            x1 = Pline.getn1.getx
            z1 = Pline.getn1.getz
            x2 = Pline.getn2.getx
            z2 = Pline.getn2.getz

            if Pline.getn1.getz > FreeSurfaceHeigh:
                x1 = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
                z1 = FreeSurfaceHeigh
            if Pline.getn2.getz > FreeSurfaceHeigh:
                x2 = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
                z2 = FreeSurfaceHeigh

            x_values = [x1, x2]
            z_values = [z1, z2]

            x_fill.extend(x_values)
            z_fill.extend(z_values)

    # Fill the shape defined by the Plines and free surface with grey color
    # (concrete-like appearance)
    plt.fill(x_fill, z_fill, 'lightgrey', zorder=0, label=paramPLT.getLegends)


def PLT2DFormworkPressure(Plines, freesurface, paramPLT):
    for Pline in Plines:
        axis = [1,3]
        # Best look
        paramPLT.getLineType = 2
        BoolArrow = True
        paramPLT.getColour = 'red'
        ArrowLFactor = 0.1
        UnitDx, UnitDy, UnitDz = Pline.Components
        Length, VectAlpha, VectBeta = Compo2Angle(UnitDx,
                                                  UnitDy,
                                                  UnitDz)
        PLine.getBeta = 90 if abs(VectAlpha) >= 90 else -90
        Pline.PLT2DPline(axis, paramPLT, BoolArrow, ArrowLFactor,
                         BAllPNode=True)


def PLT2DFormworkResultant(Plines, freesurface, paramPLT):
    for Pline in Plines:
        axis = [1,3]
        paramPLT.getColour = 'green'
        paramPLT.getLineType = 2
        BoolArrow = True
        ArrowLFactor = 0.1

        UnitDx, UnitDy, UnitDz = Pline.Components
        Length, VectAlpha, VectBeta = Compo2Angle(UnitDx,
                                                  UnitDy,
                                                  UnitDz)
        PLine.getBeta = 90 if abs(VectAlpha) >= 90 else -90
        Pline.PLTPlineR(axis, paramPLT, ArrowLFactor)

def plot_2d_formwork(Plines, freesurface, ScalePressure):
    plt.figure()

    # Collect x and z values for filling the area (assumed to be closed shape)
    x_fill = []
    z_fill = []


    # Get the nodes in the free surface
    free_surface_nodes = freesurface.getNodes
    FreeSurfaceHeigh = freesurface.getFreeSurface

    # Printing pressures
    for Pline in Plines:
        if Pline.getn1.getz < FreeSurfaceHeigh or Pline.getn2.getz < FreeSurfaceHeigh:
            # Calculate the pressure vectors (perpendicular to the Plines)
            dx = Pline.getn2.getx - Pline.getn1.getx
            dz = Pline.getn2.getz - Pline.getn1.getz
            length = np.sqrt(dx**2 + dz**2)
            # Unit vectors perpendicular to the Pline (for outward direction)
            unit_dx = dz / length
            unit_dz = -dx / length

            # Append coordinates for the fill
            # mais remplace les noeuds qui sont juste au dessus de la limite.
            x1 = Pline.getn1.getx
            z1 = Pline.getn1.getz
            x2 = Pline.getn2.getx
            z2 = Pline.getn2.getz

            if Pline.getn1.getz > FreeSurfaceHeigh:
                x1 = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
                z1 = FreeSurfaceHeigh
            if Pline.getn2.getz > FreeSurfaceHeigh:
                x2 = x1+(x2-x1)/(z2-z1)*(FreeSurfaceHeigh-z1)
                z2 = FreeSurfaceHeigh

            x_values = [x1, x2]
            z_values = [z1, z2]

            x_fill.extend(x_values)
            z_fill.extend(z_values)

            # Plot pressure at both nodes with arrows perpendicular to the Pline
            # (pointing outward), but skip free surface nodes
            ArrowLFactor = 0.1  # Length parameter

            PTol = 10**(-3)
            LengthTol = 10**(-3)
            LFreeSurfaceNode = []

            # Data memory of previous node
            arrow_point_xPretemp = None
            arrow_point_zPretemp = None
            PrePnode = None
            P_Pretemp = 0

            # Resultant of pressure
            # Ref is taken from the first node
            MomentumFromRef = 0
            ForceFromRef = 0

            for Pnode in Pline.getPNodes:
                pressure_temp = Pnode.getP

                arrow_point_xtemp = Pnode.getx + unit_dx * pressure_temp * ScalePressure
                arrow_point_ztemp = Pnode.getz + unit_dz * pressure_temp * ScalePressure
                if Pnode == Pline.getPNodes[0] or Pnode == Pline.getPNodes[-1]:
                    plt.arrow(Pnode.getx, Pnode.getz,
                              unit_dx*(pressure_temp-ArrowLFactor*pressure_temp)*ScalePressure,
                              unit_dz*(pressure_temp-ArrowLFactor*pressure_temp)*ScalePressure,
                              head_width=ArrowLFactor*0.6*pressure_temp*ScalePressure,
                              head_length=ArrowLFactor*pressure_temp*ScalePressure,
                              fc='red', ec='red')
                    plt.text(arrow_point_xtemp, arrow_point_ztemp, f"{pressure_temp:.2f} Pa", color='black', fontsize=8)

                # Link pressures between previous and current nodes with a
                # dashed Pline (for visual connection), even if on free surface
                if abs(pressure_temp) > PTol or abs(P_Pretemp) > PTol:
                    plt.plot([arrow_point_xtemp, arrow_point_xPretemp],
                             [arrow_point_ztemp, arrow_point_zPretemp],
                             'r--')  # Red dashed Pline to link pressures between nodes
                    # Calul de la résultante
                    if PrePnode:
                        L = ((Pnode.getx-PrePnode.getx)**2+(Pnode.getz-PrePnode.getz)**2)**0.5
                        ForceTemp = (P_Pretemp+pressure_temp)/2*L
                        ForceFromRef += ForceTemp
                        Lsupl = (2*P_Pretemp+pressure_temp)/(P_Pretemp+pressure_temp)*L/3
                        LeverArm = ((Pnode.getx-Pline.getn1.getx)**(2)+(Pnode.getz-Pline.getn1.getz)**(2))**0.5-Lsupl
                        MomentumFromRef += ForceTemp*LeverArm

                arrow_point_xPretemp = arrow_point_xtemp
                arrow_point_zPretemp = arrow_point_ztemp
                PrePnode = Pnode
                P_Pretemp = pressure_temp
                # Limite de la surface libre
                if abs(pressure_temp) < PTol and abs(Pnode.getz-FreeSurfaceHeigh) < LengthTol:
                    LFreeSurfaceNode.append(Pnode)

            LFromRef = MomentumFromRef/ForceFromRef
            xResultant, yResultant, zResultant = Pline.InterpolCoordLine(LFromRef, 1)
            ArrowPointXResultantTemp = xResultant + unit_dx*(ForceFromRef-ArrowLFactor*ForceFromRef)*ScalePressure
            ArrowPointZResultantTemp = zResultant + unit_dz*(ForceFromRef-ArrowLFactor*ForceFromRef)*ScalePressure
            plt.arrow(xResultant, zResultant,
                      unit_dx*(ForceFromRef-ArrowLFactor*ForceFromRef)*ScalePressure,
                      unit_dz*(ForceFromRef-ArrowLFactor*ForceFromRef)*ScalePressure,
                      head_width=ArrowLFactor*0.6*ForceFromRef*ScalePressure,
                      head_length=ArrowLFactor*ForceFromRef*ScalePressure,
                      fc='green', ec='green')
            plt.text(ArrowPointXResultantTemp, ArrowPointZResultantTemp, f"{ForceFromRef:.2f} N", color='black', fontsize=8)

    # Collect free surface nodes for closing the shape (filling the concrete-like grey area)
    for Pnode in LFreeSurfaceNode:
        x_fill.append(Pnode.getx)
        z_fill.append(Pnode.getz)

    # Fill the shape defined by the Plines and free surface with grey color (concrete-like appearance)
    plt.fill(x_fill, z_fill, 'lightgrey', zorder=0)  # Grey fill behind the Plines

    plt.xlabel('X [m]')
    plt.ylabel('Z [m]')
    plt.title('2D Formwork with Pressure Distribution and Filled Concrete')
    plt.gca().set_aspect('equal', adjustable='box')  # Keep aspect ratio consistent
    plt.show()