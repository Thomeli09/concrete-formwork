# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:12:41 2024

@author: Thommes Eliott
"""

# Element library

import matplotlib.pyplot as plt

from GeometryLib import Node, Line
from PlotLib import PLT2DCircle


"""
Noeuds d'élément
"""


class StructNode(Node):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)  # pour bénéficier de l'inhéritance
        self.Myy = None
        self.Mzz = None
        self.Tzz = None
        self.Tyy = None
        self.Nxx = None

    @property
    def getMt(self):
        return self.Mt

    @getMt.setter
    def getMt(self, val):
        self.Mt = val

    @property
    def getMyy(self):
        return self.Myy

    @getMyy.setter
    def getMyy(self, val):
        self.Myy = val

    @property
    def getMzz(self):
        return self.Mzz

    @getMzz.setter
    def getMzz(self, val):
        self.Mzz = val

    @property
    def getTzz(self):
        return self.Tzz

    @getTzz.setter
    def getTzz(self, val):
        self.Tzz = val

    @property
    def getTyy(self):
        return self.Tyy

    @getTyy.setter
    def getTyy(self, val):
        self.Tyy = val

    @property
    def getN(self):
        return self.Nxx

    @getN.setter
    def getN(self, val):
        self.Nxx = val


"""
Eléments
"""


class Element(Line):
    def __init__(self, node1, node2, section, CondAppuieN1, CondAppuieN2,
                 Name, Color):
        super().__init__(node1, node2)  # pour bénéficier de l'inhéritance
        self.LStructNode = []
        self.Section = section
        self.CondAppuieN1 = CondAppuieN1
        self.CondAppuieN2 = CondAppuieN2
        self.CondAppuieN1.getNSupport = node1
        self.CondAppuieN2.getNSupport = node2

    @property
    def getStructNodes(self):
        return self.LStructNode

    @getStructNodes.setter
    def getStructNodes(self, LStructNode):
        self.LStructNode = LStructNode

    @property
    def getSection(self):
        return self.Section

    @getSection.setter
    def getSection(self, section):
        self.Section = section

    @property
    def getSupportN1(self):
        self.CondAppuieN1.getNSupport = self.getn1
        return self.CondAppuieN1

    @property
    def getSupportN2(self):
        self.CondAppuieN2.getNSupport = self.getn2
        return self.CondAppuieN2

    def PLT2DElement(self, axis, paramPLT, BSupport=False, dAbsc=1, dOrdo=0):
        if axis[0] == 1:
            xValues = [self.getn1.getx, self.getn2.getx]
        elif axis[0] == 2:
            xValues = [self.getn1.gety, self.getn2.gety]
        else:
            xValues = [self.getn1.getz, self.getn2.getz]

        if axis[1] == 1:
            yValues = [self.getn1.getx, self.getn2.getx]
        elif axis[1] == 2:
            yValues = [self.getn1.gety, self.getn2.gety]
        else:
            yValues = [self.getn1.getz, self.getn2.getz]

        # Plot the line with specified parameters
        plt.plot(xValues, yValues,
                 color=paramPLT.getColour,
                 linestyle=paramPLT.getLineType,
                 marker=paramPLT.getMarker,
                 linewidth=paramPLT.getLineSize,
                 markersize=paramPLT.getLineSize,
                 label=paramPLT.getLegends)
        if BSupport:
            self.getSupportN1.PLT2DAppui(axis=axis, paramPLT=paramPLT,
                                         dAbsc=dAbsc, dOrdo=dOrdo)
            self.getSupportN2.PLT2DAppui(axis=axis, paramPLT=paramPLT,
                                         dAbsc=dAbsc, dOrdo=dOrdo)

"""
Plot the result of the element in 2d et juste l'élément avec les cond d'appuis
"""


"""
Section
"""


# Simplified cross section definition from properties (without shape)
class CrossSectionEasy:
    def __init__(self, Name=None, Color=None):
        self.Area = False
        self.Perimeter = False
        self.Inertia = False
        self.Material = False
        self.Name = Name
        self.Color = Color

    @property
    def get(self):
        return False

    @get.setter
    def get(self):
        return False

# Complexe cross section definition
class CrossSection(CrossSectionEasy):  # (Surface):
    def __init__(self, Name=None, Color=None):
        super().__init__(Name, Color)  # pour bénéficier de l'inhéritance
        self.Properties = False
        """
        Créer ici une structure surface 2d avec plus d'option
        Surface 2D qui est une classe fille de surface mais avec plus d'option
        """
        self.Surface = None
        """
        Liste de surface et de matériaux si différents matériaux
        """

    @property
    def getTemp(self):
        return False

    @getTemp.setter
    def getTemp(self):
        return False

    def PLT2DSection(self, axis, paramPLT):
        """
        Affiché la section qui a été utilisée
        """
        return False


"""
Condition d'appuis
"""


class Support(Node):
    def __init__(self, x, y, z,
                 DDL_Dx, DDL_Dy, DDL_Dz, DDL_Mx, DDL_My, DDL_Mz):
        # 'F' = unlocked, 'R' = locked, 'S' Spring
        super().__init__(x, y, z)  # pour bénéficier de l'inhéritance
        self.DDLDX = DDL_Dx
        self.DDLDY = DDL_Dy
        self.DDLDZ = DDL_Dz
        self.DDLMx = DDL_Mx
        self.DDLMy = DDL_My
        self.DDLMz = DDL_Mz

    @property
    def getDDl(self):
        return (self.DDLDX, self.DDLDY, self.DDLDZ,
                self.DDLMx, self.DDLMx, self.DDLMz)

    @property
    def getDDLDx(self):
        return self.DDLDX

    @getDDLDx.setter
    def getDDLDx(self, DDL_Dx):
        self.DDLDX = DDL_Dx

    @property
    def getDDLDy(self):
        return self.DDLDY

    @getDDLDy.setter
    def getDDLDy(self, DDL_Dy):
        self.DDLDY = DDL_Dy

    @property
    def getDDLDz(self):
        return self.DDLDZ

    @getDDLDz.setter
    def getDDLDz(self, DDL_Dz):
        self.DDLDZ = DDL_Dz

    @property
    def getDDLMx(self):
        return self.DDLMx

    @getDDLMx.setter
    def getDDLMx(self, DDL_Mx):
        self.DDLMx = DDL_Mx

    @property
    def getDDLMy(self):
        return self.DDLMy

    @getDDLMy.setter
    def getDDLMy(self, DDL_My):
        self.DDLMy = DDL_My

    @property
    def getDDLMz(self):
        return self.DDLMz

    @getDDLMz.setter
    def getDDLMz(self, DDL_Mz):
        self.DDLMz = DDL_Mz

    @property
    def getNSupport(self):
        return Node(self.getx, self.gety, self.getz)

    @getNSupport.setter
    def getNSupport(self, NSupport):
        self.getx = NSupport.getx
        self.gety = NSupport.gety
        self.getz = NSupport.getz

    def PLT2DAppui(self, axis, paramPLT, dAbsc=1, dOrdo=0):
        """
        passer à un système ou détecte pour se mettre du coté de l'ojet divers
        donc demande à l'obet les coord et prends le points le plus près
        """
        if axis == [1,2]:
            BoolDAbsc = self.getDDLDx
            BoolDOrdo = self.getDDLDy
            BoolM = self.getDDLMz
            AbscCoord = self.getx
            OrdoCoord = self.gety
        elif axis == [1,3]:
            BoolDAbsc = self.getDDLDx
            BoolDOrdo = self.getDDLDz
            BoolM = self.getDDLMy
            AbscCoord = self.getx
            OrdoCoord = self.getz
        elif axis == [2,3]:
            BoolDAbsc = self.getDDLDy
            BoolDOrdo = self.getDDLDz
            BoolM = self.getDDLMx
            AbscCoord = self.gety
            OrdoCoord = self.getz

        if BoolDAbsc and BoolDOrdo and BoolM:
            # Extrémité libre
            print("Info: Free end => No support to show")

        elif BoolDAbsc and (not BoolDOrdo) and BoolM:
            # Support à rouleau
            # s = size
            # facecolors = to make it hollow
            # edgecolors = to set the color of the border
            # linewidths = edge thickness of the hollow point
            print("Info: Roller support")
            PLT2DCircle(x=AbscCoord, y=OrdoCoord,
                        NPoints=30, Radius=paramPLT.getMarkerSize,
                        paramPLT=paramPLT, BFill=False)
            # Normalize the direction vector (dx, dy) to get unit vector
            Length = (dAbsc**2 + dOrdo**2)**0.5
            UnitAbsc, UnitOrdo = dAbsc / Length, dOrdo / Length
            # Perpendicular vector
            UnitAbscPerp, UnitOrdoPerp = -UnitOrdo, UnitAbsc
            Size = paramPLT.getMarkerSize * 5
            # Plot of the triangle
            PointAbsc = AbscCoord - UnitAbscPerp*Size*(3/4)**0.5
            PointOrdo = OrdoCoord - UnitOrdoPerp*Size*(3/4)**0.5
            AbscTriangleStart = PointAbsc-Size/2*UnitAbsc
            OrdoTriangleStart = PointOrdo-Size/2*UnitOrdo
            AbscTriangleEnd = PointAbsc+Size/2*UnitAbsc
            OrdoTriangleEnd = PointOrdo+Size/2*UnitOrdo
            AbscList = [AbscCoord, AbscTriangleStart, AbscTriangleEnd]
            OrdoList = [OrdoCoord, OrdoTriangleStart, OrdoTriangleEnd]
            plt.plot(AbscList, OrdoList,
                     color=paramPLT.getColour,
                     linestyle=paramPLT.getLineType,
                     marker=paramPLT.getMarker,
                     linewidth=paramPLT.getLineSize,
                     markersize=paramPLT.getLineSize,
                     label=paramPLT.getLegends)
            plt.fill(AbscList, OrdoList, paramPLT.getColour, zorder=0,
                     label=paramPLT.getLegends)
            # Plot of rollers
            NCircle = 3
            radius = Size/(NCircle*2+NCircle+1)
            AbscCircle = AbscTriangleStart - radius*UnitAbscPerp + 2*radius*UnitAbsc
            OrdoCircle = OrdoTriangleStart - radius*UnitOrdoPerp + 2*radius*UnitOrdo
            i = 1
            while i <= NCircle:
                PLT2DCircle(x=AbscCircle, y=OrdoCircle,
                            NPoints=15, Radius=radius,
                            paramPLT=paramPLT, BFill=False)
                AbscCircle += 3*radius*UnitAbsc
                OrdoCircle += 3*radius*UnitOrdo
                i += 1
            # Line for support
            AbscLine = AbscTriangleStart - 2*radius*UnitAbscPerp - 1*radius*UnitAbsc
            OrdoLine = OrdoTriangleStart - 2*radius*UnitOrdoPerp - 1*radius*UnitOrdo

            plt.plot([AbscLine, AbscLine+UnitAbsc*(Size+2*radius)],
                     [OrdoLine, OrdoLine+UnitOrdo*(Size+2*radius)],
                     color=paramPLT.getColour,
                     linestyle=paramPLT.getLineType,
                     marker=paramPLT.getMarker,
                     linewidth=paramPLT.getLineSize,
                     markersize=paramPLT.getLineSize,
                     label=paramPLT.getLegends)

        elif (not BoolDAbsc) and (not BoolDOrdo) and BoolM:
            # Appui rotulé :
            # s = size
            # facecolors = to make it hollow
            # edgecolors = to set the color of the border
            # linewidths = edge thickness of the hollow point
            print("Info: Pinned support")
            PLT2DCircle(x=AbscCoord, y=OrdoCoord,
                        NPoints=30, Radius=paramPLT.getMarkerSize,
                        paramPLT=paramPLT, BFill=False)

        elif BoolDAbsc and (not BoolDOrdo) and (not BoolM):
            # Appui simple
            print("Error: Simple support not currently defined ")

        elif (not BoolDAbsc) and (not BoolDOrdo) and (not BoolM):
            # Encastrement
            # s = size
            # c = to set the color of the filled dot
            print("Info: Contilever support")
            PLT2DCircle(x=AbscCoord, y=OrdoCoord,
                        NPoints=30, Radius=paramPLT.getMarkerSize,
                        paramPLT=paramPLT, BFill=True)
        else:
            print("Error: Unknown support")

        return False

    def PLT3DAppui(self, axis, paramPLT):
        """
        Affiché le noeuds de différentes façons
        """
        """
        Faire avec des barres continus si ok ddl ou flèches
        sinon barre avec droite perpendiculaire si bloquer

        plusieurs flèche à la base pour dire si ok rota ou rond en 2d
        """
        return False
