# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:12:42 2024

@author: Thommes Eliott
"""

# Loading library

import math
import matplotlib.pyplot as plt

from GeometryLib import Node, Line, Angle2Compo, Compo2Angle
from PlotLib import ParamPLT


"""
Chargement nodale
"""
class FNode(Node):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)  # pour bénéficier de l'inhéritance
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0

    @property
    def getF(self):
        return (self.Fx, self.Fy, self.Fz)

    @getF.setter
    def getF(self, val):
        self.Fx = val[0]
        self.Fy = val[1]
        self.Fz = val[2]

    @property
    def getFtot(self):
        FTot = (self.Fx**2 + self.Fy**2 + self.Fz**2)**0.5
        return FTot

    def PLT2DFNode(self, axis, paramPLT, ArrowLFactor=0.1):
        if axis[0] == 1:
            xVal = [self.getx, self.Fx]
        elif axis[0] == 2:
            xVal = [self.gety, self.Fy]
        else:
            xVal = [self.getz, self.Fz]

        if axis[1] == 1:
            yVal = [self.getx, self.Fx]
        elif axis[1] == 2:
            yVal = [self.gety, self.Fy]
        else:
            yVal = [self.getz, self.Fz]

        DeltaArrowPointx = xVal[1]*paramPLT.getScale
        DeltaArrowPointy = yVal[1]*paramPLT.getScale

        plt.arrow(xVal[0], yVal[0], DeltaArrowPointx, DeltaArrowPointy,
                  head_width=ArrowLFactor*0.6*self.getFtot*paramPLT.getScale,
                  head_length=ArrowLFactor*self.getFtot*paramPLT.getScale,
                  length_includes_head=True,
                  fc=paramPLT.getColour, ec=paramPLT.getColour,
                  label=paramPLT.getLegends)

    def PLT2DTextFNode(self, axis, paramPLT):
        if axis[0] == 1:
            xVal = [self.getx, self.Fx]
        elif axis[0] == 2:
            xVal = [self.gety, self.Fy]
        else:
            xVal = [self.getz, self.Fz]

        if axis[1] == 1:
            yVal = [self.getx, self.Fx]
        elif axis[1] == 2:
            yVal = [self.gety, self.Fy]
        else:
            yVal = [self.getz, self.Fz]

        ArrowPointx = xVal[0] + xVal[1] * paramPLT.getScale
        ArrowPointy = yVal[0] + yVal[1] * paramPLT.getScale

        plt.text(ArrowPointx, ArrowPointy, f"{self.getFtot:.2e} N",
                 color=paramPLT.getColour,
                 fontsize=paramPLT.getFontSize)

    def FTot2FCompo(Ftot, Alpha, Beta):
        # Alpha is the angle between the force vector and the y-axis in the XY
        # plane.
        # Beta remains the angle between the force vector and the z-axis.
        # Convert angles from degrees to radians
        AlphaRad = math.radians(Alpha)
        BetaRad = math.radians(Beta)

        # Calculate components using trigonometry
        Fx = Ftot * math.cos(BetaRad) * math.cos(AlphaRad)
        Fy = Ftot * math.cos(BetaRad) * math.sin(AlphaRad)
        Fz = Ftot * math.sin(BetaRad)
        return (Fx, Fy, Fz)

    def FCompo2FTot(Fx, Fy, Fz):
        # Alpha is the angle between the force vector and the y-axis in the XY
        # plane.
        # Beta remains the angle between the force vector and the z-axis.
        Ftot = (Fx**2 + Fy**2 + Fz**2)**0.5
        # Calculate angles in degrees
        Alpha = math.degrees(math.atan2(Fy, Fx)) if Ftot != 0 else 0  # Angle in x-y plane
        Beta = math.degrees(math.asin(Fz / Ftot)) if Ftot != 0 else 0  # Angle from z-axis
        return (Ftot, Alpha, Beta)


"""
Déplacement nodale
"""
class DNode(Node):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)  # pour bénéficier de l'inhéritance
        self.Dx = 0
        self.Dy = 0
        self.Dz = 0

    @property
    def getD(self):
        return (self.Dx, self.Dy, self.Dz)

    @getD.setter
    def getD(self, val):
        self.Dx = val[0]
        self.Dy = val[1]
        self.Dz = val[2]

    @property
    def getDtot(self):
        DTot = (self.Dx**2 + self.Dy**2 + self.Dz**2)**0.5
        return DTot

    def PLT2DDNode(self, axis, paramPLT, ArrowLFactor=0.1):
        if axis[0] == 1:
            xVal = [self.getx, self.Dx]
        elif axis[0] == 2:
            xVal = [self.gety, self.Dy]
        else:
            xVal = [self.getz, self.Dz]

        if axis[1] == 1:
            yVal = [self.getx, self.Dx]
        elif axis[1] == 2:
            yVal = [self.gety, self.Dy]
        else:
            yVal = [self.getz, self.Dz]

        ArrowPointx = xVal[1]*paramPLT.getScale
        ArrowPointy = yVal[1]*paramPLT.getScale

        plt.arrow(xVal[0], yVal[0], ArrowPointx, ArrowPointy,
                  head_width=ArrowLFactor*0.6*self.getDtot*paramPLT.getScale,
                  head_length=ArrowLFactor*self.getDtot*paramPLT.getScale,
                  length_includes_head=True,
                  fc=paramPLT.getColour, ec=paramPLT.getColour)

    def PLT2DTextDNode(self, axis, paramPLT):
        if axis[0] == 1:
            xVal = [self.getx, self.Dx]
        elif axis[0] == 2:
            xVal = [self.gety, self.Dy]
        else:
            xVal = [self.getz, self.Dz]

        if axis[1] == 1:
            yVal = [self.getx, self.Dx]
        elif axis[1] == 2:
            yVal = [self.gety, self.Dy]
        else:
            yVal = [self.getz, self.Dz]

        ArrowPointx = xVal[0] + xVal[1] * paramPLT.getScale
        ArrowPointy = yVal[0] + yVal[1] * paramPLT.getScale

        plt.text(ArrowPointx, ArrowPointy, f"{self.getDtot:.2e} m",
                 color=paramPLT.getColour,
                 fontsize=paramPLT.getFontSize)

    def DTot2DCompo(Dtot, Alpha, Beta):
        # Alpha is the angle between the vector and the y-axis in the XY plane.
        # Beta remains the angle between the vector and the z-axis.
        # Convert angles from degrees to radians
        AlphaRad = math.radians(Alpha)
        BetaRad = math.radians(Beta)

        # Calculate components using trigonometry
        Dx = Dtot * math.cos(BetaRad) * math.cos(AlphaRad)
        Dy = Dtot * math.cos(BetaRad) * math.sin(AlphaRad)
        Dz = Dtot * math.sin(BetaRad)
        return (Dx, Dy, Dz)

    def DCompo2DTot(Dx, Dy, Dz):
        # Alpha is the angle between the vector and the y-axis in the XY plane.
        # Beta remains the angle between the vector and the z-axis.
        Dtot = (Dx**2 + Dy**2 + Dz**2)**0.5
        # Calculate angles in degrees
        Alpha = math.degrees(math.atan2(Dy, Dx)) if Dtot != 0 else 0  # Angle in x-y plane
        Beta = math.degrees(math.asin(Dz / Dtot)) if Dtot != 0 else 0  # Angle from z-axis
        return (Dtot, Alpha, Beta)


"""
Chargement linéique ou surfacique
"""
# Classe de noeuds enregistrant une pression
class PNode(Node):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)  # pour bénéficier de l'inhéritance
        self.P = None

    @property
    def getP(self):
        return self.P

    @getP.setter
    def getP(self, val):
        self.P = val


"""
Ligne de chargement linéique
"""
class PLine(Line):
    def __init__(self, node1, node2, alpha=0, beta=0):
        super().__init__(node1, node2)  # pour bénéficier de l'inhéritance
        self.LPNode = []
        self.Alpha = alpha
        self.Beta = beta
        self.RFnode = None  # Noeud de la résultante
        """
        Angle relatif ou absolue des forces?
        Vérification que le calcul des résultantes est bien actalisé?
        """

    @property
    def getPNodes(self):
        return self.LPNode

    @getPNodes.setter
    def getPNodes(self, LPNode):
        self.LPNode = LPNode

    @property
    def getAlpha(self):
        return self.Alpha

    @getAlpha.setter
    def getAlpha(self, Val):
        self.Alpha = Val

    @property
    def getBeta(self):
        return self.Beta

    @getBeta.setter
    def getBeta(self, Val):
        self.Beta = Val

    @property
    def getRFnode(self):
        self.CMP_R
        return self.RFnode

    def PLT2DPline(self, axis, paramPLT, BoolArrow, ArrowLFactor,
                   BAllPNode=False):
        # Affichage du chargement
        UnitDx, UnitDy, UnitDz = self.Components
        Length, VectAlpha, VectBeta = Compo2Angle(UnitDx,
                                                  UnitDy,
                                                  UnitDz)

        UnitDx, UnitDy, UnitDz = Angle2Compo(Length,
                                             VectAlpha+self.getAlpha,
                                             VectBeta+self.getBeta)

        # Data memory of previous node
        PressureTemp = 0
        ArrowPointPreTempx = None
        ArrowPointPreTempy = None
        ArrowPointPreTempz = None
        for Pnode in self.getPNodes:
            PressureTemp = Pnode.getP
            ArrowPointTempx = Pnode.getx+UnitDx*PressureTemp*paramPLT.getScale
            ArrowPointTempy = Pnode.gety+UnitDy*PressureTemp*paramPLT.getScale
            ArrowPointTempz = Pnode.getz+UnitDz*PressureTemp*paramPLT.getScale
            # Abscisse Absc
            if axis[0] == 1:
                AbscNode = Pnode.getx
                AbscArrow = ArrowPointTempx
                AbscPreArrow = ArrowPointPreTempx
                AbscDeltaArrow = UnitDx*PressureTemp*paramPLT.getScale
            elif axis[0] == 2:
                AbscNode = Pnode.gety
                AbscArrow = ArrowPointTempy
                AbscPreArrow = ArrowPointPreTempy
                AbscDeltaArrow = UnitDy*PressureTemp*paramPLT.getScale
            else:
                AbscNode = Pnode.getz
                AbscArrow = ArrowPointTempz
                AbscPreArrow = ArrowPointPreTempz
                AbscDeltaArrow = UnitDz*PressureTemp*paramPLT.getScale
            # Ordonnées Ordo
            if axis[1] == 1:
                OrdoNode = Pnode.getx
                OrdoArrow = ArrowPointTempx
                OrdoPreArrow = ArrowPointPreTempx
                OrdoDeltaArrow = UnitDx*PressureTemp*paramPLT.getScale
            elif axis[1] == 2:
                OrdoNode = Pnode.gety
                OrdoArrow = ArrowPointTempy
                OrdoPreArrow = ArrowPointPreTempy
                OrdoDeltaArrow = UnitDy*PressureTemp*paramPLT.getScale
            else:
                OrdoNode = Pnode.getz
                OrdoArrow = ArrowPointTempz
                OrdoPreArrow = ArrowPointPreTempz
                OrdoDeltaArrow = UnitDz*PressureTemp*paramPLT.getScale

            # Flèches ou ligne pour les noeuds de fin
            if Pnode == self.getPNodes[0] or Pnode == self.getPNodes[-1] or BAllPNode:
                if BoolArrow:
                    plt.arrow(AbscNode, OrdoNode,
                              AbscDeltaArrow, OrdoDeltaArrow,
                              head_width=ArrowLFactor*0.6*PressureTemp*paramPLT.getScale,
                              head_length=ArrowLFactor*PressureTemp*paramPLT.getScale,
                              length_includes_head=True,
                              fc=paramPLT.getColour, ec=paramPLT.getColour)
                else:
                    plt.plot([AbscNode, AbscArrow],
                             [OrdoNode, OrdoArrow],
                             color=paramPLT.getColour,
                             linestyle=paramPLT.getLineType,
                             marker=paramPLT.getMarker,
                             linewidth=paramPLT.getLineSize,
                             markersize=paramPLT.getLineSize,
                             label=paramPLT.getLegends)

            # Link pressures between previous and current nodes
            if AbscPreArrow is not None:
                plt.plot([AbscPreArrow, AbscArrow],
                         [OrdoPreArrow, OrdoArrow],
                         color=paramPLT.getColour,
                         linestyle=paramPLT.getLineType,
                         marker=paramPLT.getMarker,
                         linewidth=paramPLT.getLineSize,
                         markersize=paramPLT.getLineSize,
                         label=paramPLT.getLegends)

            ArrowPointPreTempx = ArrowPointTempx
            ArrowPointPreTempy = ArrowPointTempy
            ArrowPointPreTempz = ArrowPointTempz

    def PLT2DTextPline(self, axis, paramPLT, BoolAllNode):
        # Affichage des valeurs du chargement
        UnitDx, UnitDy, UnitDz = self.Components
        Length, VectAlpha, VectBeta = self.Compo2Angle(UnitDx,
                                                       UnitDy,
                                                   UnitDz)
        UnitDx, UnitDy, UnitDz = self.Angle2Compo(Length,
                                                  VectAlpha+self.getAlpha,
                                                  VectBeta+self.getBeta)
        # Data memory of previous node
        PressureTemp = 0
        for Pnode in self.getPNodes:
            PressureTemp = Pnode.getP
            ArrowPointTempx = Pnode.getx+UnitDx*PressureTemp*paramPLT.getScale
            ArrowPointTempy = Pnode.gety+UnitDy*PressureTemp*paramPLT.getScale
            ArrowPointTempz = Pnode.getz+UnitDz*PressureTemp*paramPLT.getScale

            if Pnode == self.getPNodes[0] or Pnode == self.getPNodes[-1]:
                plt.text(ArrowPointTempx, ArrowPointTempz,
                         f"{PressureTemp:.2e}", color=paramPLT.getColour,
                         fontsize=paramPLT.getFontSize)
            elif BoolAllNode:
                plt.text(ArrowPointTempx, ArrowPointTempz,
                         f"{PressureTemp:.2e}", color=paramPLT.getColour,
                         fontsize=paramPLT.getFontSize)

    @property
    def CMP_R(self):
        # Calcul la résultante et les angles ou composantes
        UnitDx, UnitDy, UnitDz = self.Components
        Length, VectAlpha, VectBeta = Compo2Angle(UnitDx,
                                                  UnitDy,
                                                  UnitDz)

        UnitDx, UnitDy, UnitDz = Angle2Compo(Length,
                                             VectAlpha+self.getAlpha,
                                             VectBeta+self.getBeta)
        # Resultant of pressure
        # Ref is taken from the first node of the line
        MomentumFromRef = 0
        ForceFromRef = 0
        PressureTemp = 0
        PnodePreTemp = None
        PressurePreTemp = 0
        for Pnode in self.getPNodes:
            PressureTemp = Pnode.getP
            if PnodePreTemp and abs(PressurePreTemp+PressureTemp):
                LLocal = Pnode.Distance2(PnodePreTemp)
                ForceTemp = (PressurePreTemp+PressureTemp)/2*LLocal
                ForceFromRef += ForceTemp
                LLocalSupl = (2*PressurePreTemp+PressureTemp)/(PressurePreTemp+PressureTemp)*LLocal/3
                LeverArm = Pnode.Distance2(self.getn1)-LLocalSupl
                MomentumFromRef += ForceTemp*LeverArm

            PnodePreTemp = Pnode
            PressurePreTemp = PressureTemp
        if ForceFromRef:
            LFromRef = MomentumFromRef/ForceFromRef
            xResultant, yResultant, zResultant = self.InterpolCoordLine(LFromRef, 1)
        else:
            node = self.getn1
            xResultant = node.getx
            yResultant = node.gety
            zResultant = node.getz

        Fx = UnitDx*ForceFromRef
        Fy = UnitDy*ForceFromRef
        Fz = UnitDz*ForceFromRef
        TempNode = FNode(xResultant, yResultant, zResultant)
        TempNode.getF = (Fx, Fy, Fz)
        self.RFnode = TempNode

    def PLTPlineR(self, axis, paramPLT, ArrowLFactor=0.1):
        # Affichage de la résultante
        self.CMP_R
        self.RFnode.PLT2DFNode(axis, paramPLT, ArrowLFactor)

    def PLT2DTextPlineR(self, axis, paramPLT):
        # Affichage les valeurs de la résultante
        self.RFnode.PLT2DTextFNode(axis, paramPLT)

    def PLT2DNodeName(self, axis, paramPLT):
        # Affichage le nom des noeuds
        self.RFnode.PLT2DTextFNode(axis, paramPLT)

"""
Ligne de chargement (linéique ou nodale)
"""
class LLine(Line):
    def __init__(self, node1, node2):
        super().__init__(node1, node2)  # pour bénéficier de l'inhéritance
        self.Loading = []

    @property
    def getLoading(self):
        return self.Loading

    @getLoading.setter
    def getLoading(self, loading):
        self.Loading = loading

    def PLT2DLLine(self, axis, paramPLT, ArrowLFactor, BoolResultant):
        # Affichage des chargements
        for Load in self.getLoading:
            if isinstance(Load, (FNode)):
                Load.PLT2DFNode(axis, paramPLT, ArrowLFactor)
            elif isinstance(Load, (DNode)):
                Load.PLT2DDNode(axis, paramPLT, ArrowLFactor)
            elif isinstance(Load, (PLine)):
                BoolArrow = True
                Load.PLT2DPline(axis, paramPLT, BoolArrow, ArrowLFactor)
            elif BoolResultant and isinstance(Load, (PLine)):
                Load.PLTPlineR(axis, paramPLT, ArrowLFactor)
            else:
                print("Error : Unidentified Classes")

    def PLT2DTextLLine(self, axis, paramPLT, ArrowLFactor, BoolResultant):
        for Load in self.getLoading:
            if isinstance(Load, (FNode)):
                Load.PLT2DTextFNode(axis, paramPLT)
            elif isinstance(Load, (DNode)):
                Load.PLT2DTextDNode(axis, paramPLT)
            elif isinstance(Load, (PLine)):
                Load.PLT2DTextPline(axis, paramPLT)
            elif BoolResultant and isinstance(Load, (PLine)):
                Load.PLT2DTextPlineR(axis, paramPLT)
            else:
                print("Error : Unidentified Classes")

    def IsInLLine(self, loading, tol):
    # Vérifies si le chargement est bien sur la LLine avec une tol
    # et si doublon existe possibilités de lier automatiquement les chargements
        return False
