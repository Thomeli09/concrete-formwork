# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:54:03 2024

@author: Thommes Eliott
"""

# Geometrical library


# Other Lib
import math
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt


# Custom Lib
from PlotLib import ParamPLT


"""
Noeuds
"""
class Node:
    def __init__(self, x, y, z, Name=None, Color=None):
        self.x = x
        self.y = y
        self.z = z
        self.Name = Name
        self.Color = Color

    # Using Python property decorators for cleaner syntax
    @property
    def getx(self):
        return self.x

    @getx.setter
    def getx(self, val):
        self.x = val

    @property
    def gety(self):
        return self.y

    @gety.setter
    def gety(self, val):
        self.y = val

    @property
    def getz(self):
        return self.z

    @getz.setter
    def getz(self, val):
        self.z = val

    def __repr__(self):
        return f"Node({self.getx}, {self.gety}, {self.getz})"

    def Distance2(self, node):
        """Calculate the Euclidean distance between this node and another node."""
        return ((self.getx-node.getx)**2 +
                (self.gety-node.gety)**2 +
                (self.getz-node.getz)**2)**0.5

    def MidpointNode2Node(self, node):
        """Define the midpoint between this node and another node."""
        x = (self.getx+node.getx)/2
        y = (self.gety+node.gety)/2
        z = (self.getz+node.getz)/2
        return (x, y, z)

    def InterpolNode2Node(self, val, node):
        Length = self.Distance2(node)
        x = self.getx+(node.getx-self.getx)*val/Length
        y = self.gety+(node.gety-self.gety)*val/Length
        z = self.getz+(node.getz-self.getz)*val/Length
        return (x, y, z)

    def ComponentsNode2Node(self, node):
        Length = self.Distance2(node)
        dx = (node.getx-self.getx)/Length
        dy = (node.gety-self.gety)/Length
        dz = (node.getz-self.getz)/Length
        return (dx, dy, dz)


# Function to add and check for duplicate node in a list of node
def AddNode(LNode, x, y, z):
    NewNode = Node(x, y, z)
    for node in LNode:
        if node.getx == NewNode.getx and node.gety == NewNode.gety and node.getz == NewNode.getz:
            return node  # Avoid duplicating nodes
    LNode.append(NewNode)
    return NewNode


"""
Ligne
"""
class Line:
    def __init__(self, node1, node2, Name=None, Color=None):
        self.node1 = node1
        self.node2 = node2
        self.Length = ((node1.getx-node2.getx)**(2) +
                       (node1.gety-node2.gety)**(2) +
                       (node1.getz-node2.getz)**(2))**0.5
        self.Name = Name
        self.Color = Color

    @property
    def getn1(self):
        return self.node1

    @getn1.setter
    def getn1(self, node):
        self.node1 = node
        self.UpdateLength()

    @property
    def getn2(self):
        return self.node2

    @getn2.setter
    def getn2(self, node):
        self.node2 = node
        self.UpdateLength()

    @property
    def getLength(self):
        return self.Length

    @property
    def UpdateLength(self):
        # Update Length whenever node1 or node2 changes
        self.Length = ((self.node1.getx-self.node2.getx)**2 +
                       (self.node1.gety-self.node2.gety)**2 +
                       (self.node1.getz-self.node2.getz)**2)**0.5

    def __repr__(self):
        return f"Line({self.getn1}, {self.getn2}, {self.getLength})"

    def InterpolCoordLine(self, val, FromNode_1_2):
        if FromNode_1_2 == 1:
            x = self.getn1.getx+(self.getn2.getx-self.getn1.getx)*val/self.getLength
            y = self.getn1.gety+(self.getn2.gety-self.getn1.gety)*val/self.getLength
            z = self.getn1.getz+(self.getn2.getz-self.getn1.getz)*val/self.getLength
        elif FromNode_1_2 == 2:
            x = self.getn2.getx+(self.getn1.getx-self.getn2.getx)*val/self.getLength
            y = self.getn2.gety+(self.getn1.gety-self.getn2.gety)*val/self.getLength
            z = self.getn2.getz+(self.getn1.getz-self.getn2.getz)*val/self.getLength
        else:
            x = self.getn1.getx+(self.getn2.getx-self.getn1.getx)*val/self.getLength
            y = self.getn1.gety+(self.getn2.gety-self.getn1.gety)*val/self.getLength
            z = self.getn1.getz+(self.getn2.getz-self.getn1.getz)*val/self.getLength
        return (x, y, z)

    @property
    def Components(self):
        dx = (self.getn2.getx-self.getn1.getx)/self.getLength
        dy = (self.getn2.gety-self.getn1.gety)/self.getLength
        dz = (self.getn2.getz-self.getn1.getz)/self.getLength
        return (dx, dy, dz)

    def PLT2DLine(self, axis, paramPLT):
        if axis[0] == 1:
            AbscValues = [self.getn1.getx, self.getn2.getx]
        elif axis[0] == 2:
            AbscValues = [self.getn1.gety, self.getn2.gety]
        else:
            AbscValues = [self.getn1.getz, self.getn2.getz]

        if axis[1] == 1:
            OrdoValues = [self.getn1.getx, self.getn2.getx]
        elif axis[1] == 2:
            OrdoValues = [self.getn1.gety, self.getn2.gety]
        else:
            OrdoValues = [self.getn1.getz, self.getn2.getz]

        # Plot the line with specified parameters
        plt.plot(AbscValues, OrdoValues,
                 color=paramPLT.getColour,
                 linestyle=paramPLT.getLineType,
                 marker=paramPLT.getMarker,
                 linewidth=paramPLT.getLineSize,
                 markersize=paramPLT.getLineSize,
                 label=paramPLT.getLegends)
    """
    Need ability to swap nodes to change normal direction
    """


def Angle2Compo(Length, Alpha, Beta):
    # Alpha is the angle between the force vector and the y-axis in the XY plane.
    # Beta remains the angle between the force vector and the z-axis.
    # Convert angles from degrees to radians
    AlphaRad = math.radians(Alpha)
    BetaRad = math.radians(Beta)

    # Calculate components using trigonometry
    Dx = Length * math.cos(BetaRad) * math.cos(AlphaRad)
    Dy = Length * math.cos(BetaRad) * math.sin(AlphaRad)
    Dz = Length * math.sin(BetaRad)
    return (Dx, Dy, Dz)


def Compo2Angle(Dx, Dy, Dz):
    # Alpha is the angle between the force vector and the y-axis in the XY plane.
    # Beta remains the angle between the force vector and the z-axis.
    Length = (Dx**2 + Dy**2 + Dz**2)**0.5
    # Calculate angles in degrees
    Alpha = math.degrees(math.atan2(Dy, Dx)) if Length != 0 else 0  # Angle in x-y plane
    Beta = math.degrees(math.asin(Dz / Length)) if Length != 0 else 0  # Angle from z-axis
    return (Length, Alpha, Beta)


"""
Ligne courbe
"""
class CurviLine:
    def __init__(self, LNode, Stype, Name=None, Color=None):
        if len(LNode) < 2:
            raise ValueError("A CurviLine requires at least two nodes.")

        TotalLength = 0.0
        for i in range(len(LNode)-1):
            TotalLength += LNode[i].Distance2(LNode[i+1])

        self.LNode = LNode  # Control points for the curve
        self.Stype = Stype
        self.Length = TotalLength
        self.Name = Name
        self.Color = Color

    @property
    def getNodes(self):
        return self.LNode

    @getNodes.setter
    def getNodes(self, LNode, Stype=None):
        if len(LNode) < 2:
            raise ValueError("A CurviLine requires at least two nodes.")

        self.LNode = LNode  # Control points for the curve

        if Stype:
            self.Stype = Stype

        self.UpdateLength

    @property
    def getStype(self):
        return self.Stype

    @getStype.setter
    def getStype(self, Stype):
        self.Stype = Stype

    @property
    def getLength(self):
        """Calculate the total length of the curve."""
        return self.Length

    @property
    def UpdateLength(self):
        """Calculate the total length of the curve."""
        LNode = self.getNodes
        TotalLength = 0.0
        for i in range(len(LNode) - 1):
            TotalLength += LNode[i].Distance2(LNode[i + 1])
        self.Length = TotalLength

    def __repr__(self):
        return f"CurviLine({self.getNodes}, {self.getLength}, {self.getStype})"

    def Interpolate(self, val):
        """Linear interpolation along the CurviLine using parameter val (0 <= t <= Length)."""
        TotalLength = self.getLength
        if not (0 <= val <= TotalLength):
            raise ValueError("Val must be between 0 and TotalLength")

        CurrentLength = 0.0
        LNode = self.getNodes
        for i in range(len(LNode) - 1):
            SegmentLength = LNode[i].Distance2(LNode[i + 1])
            if CurrentLength + SegmentLength >= val:
                ratio = (val-CurrentLength)/SegmentLength
                x = LNode[i].getx+(LNode[i+1].getx-LNode[i].getx)*ratio
                y = LNode[i].gety+(LNode[i+1].gety-LNode[i].gety)*ratio
                z = LNode[i].getz+(LNode[i+1].getz-LNode[i].getz)*ratio
                return (x, y, z)
            CurrentLength += SegmentLength
        LastNode = LNode[-1]
        return (LastNode.getx, LastNode.gety, LastNode.getz)

    @property
    def Components(self):
        """Return normalized components (dx, dy, dz) for each segment of the curve."""
        ComponentsList = []
        LNode = self.getNodes
        for i in range(len(LNode)-1):
            node1, node2 = LNode[i], LNode[i+1]
            Length = node1.Distance2(node2)
            dx = (node2.getx-node1.getx)/Length
            dy = (node2.gety-node1.gety)/Length
            dz = (node2.getz-node1.getz)/Length
            ComponentsList.append((dx, dy, dz))
        return ComponentsList


"""
Surface
"""
class Surface:
    def __init__(self, LNode, Name=None):
        self.LNode = LNode  # List of nodes that define the surface
        self.SpaceDim = None
        self.Perimeter = None
        self.Area = None
        self.Name = Name
        """
        self.UpdateSpaceDim
        self.UpdatePerimeter
        self.UpdateArea
        """
    @property
    def getNodes(self):
        return self.LNode

    @getNodes.setter
    def getNodes(self, LNode):
        self.LNode = LNode
        """
        self.UpdateSpaceDim
        self.UpdatePerimeter
        self.UpdateArea
        """

    @property
    def getSpaceDim(self):
        return self.SpaceDim

    @property
    def getPerimeter(self):
        return self.Perimeter

    @property
    def getArea(self):
        return self.Area

    def __repr__(self):
        return f"Surface({self.getNodes}, {self.getSpaceDim}, {self.getPerimeter}, {self.getArea})"

    @property
    def UpdateSpaceDim(self, RelTol=1e-5):
        """Determine the spatial dimension of the nodes using SVD."""
        if len(self.LNode) < 2:
            self.SpaceDim = 0
            # raise ValueError("At least two nodes are required to determine dimension.")

        Coords = np.array([[node.getx, node.gety, node.getz] for node in self.getNodes])
        Centroid = np.mean(Coords, axis=0)
        CenteredCoords = Coords - Centroid
        u, s, vh = np.linalg.svd(CenteredCoords)

        # Normalize singular values and determine rank
        SNormalized = s / s[0]
        Rank = np.sum(SNormalized > RelTol)
        self.SpaceDim = Rank

    @property
    def UpdatePerimeter(self):
        """Calculate the perimeter of the surface if it is a polygon."""
        LNode = self.getNodes
        if len(LNode) < 2:
            self.Perimeter = 0.0
            return

        Perimeter = 0.0
        n = len(LNode)
        for i in range(n):
            Perimeter += LNode[i].Distance2(LNode[(i + 1) % n])
        self.Perimeter = Perimeter

    @property
    def UpdateArea(self):
        """Calculate the area of the surface based on its spatial dimension."""
        if self.SpaceDim <= 1 or len(self.LNode) < 3:
            self.Area = 0.0
        elif self.SpaceDim == 2:
            self.Area = self.CalculateArea3d()
        elif self.SpaceDim == 3:
            self.Area = self.CalculateArea3d()
        else:
            self.Area = 0.0  # Default to zero if dimension is not recognized

    @property
    def CalculateArea2d(self):
        """Calculate the area of a planar polygon in 3D."""
        Coords = np.array([[node.getx, node.gety, node.getz] for node in self.getNodes])

        if len(Coords) < 3:
            print("Error: A polygon must have at least three vertices.")
            self.Area = 0.0
            return False

        # Calculate the normal vector of the plane
        Vec1 = Coords[1] - Coords[0]
        Vec2 = Coords[2] - Coords[0]
        Normal = np.cross(Vec1, Vec2)
        NormalLength = np.linalg.norm(Normal)
        if NormalLength == 0:
            raise print("The given vertices do not form a valid polygon (degenerate).")
        NormalUnit = Normal / NormalLength

        # Initialize the area vector
        AreaVector = np.zeros(3)

        # Loop over the edges of the polygon
        for i in range(len(Coords)):
            VCurrent = Coords[i]
            VNext = Coords[(i + 1) % len(Coords)]  # Wrap around to the first vertex
            CrossProduct = np.cross(VCurrent, VNext)
            AreaVector += CrossProduct

        # The area is half the magnitude of the projection of the area vector onto the Normal vector
        Area = 0.5 * np.abs(np.dot(NormalUnit, AreaVector))

        # Store the computed area
        self.Area = Area

    @property
    def CalculateArea3d(self):
        """Calculate the area of a generic surface in 3D space using Delaunay triangulation."""
        # Extract the 3D coordinates from the nodes
        Points = np.array([[node.getx, node.gety, node.getz] for node in self.getNodes])

        if len(Points) < 3:
            print("Error: A polygon must have at least three vertices.")
            self.Area = 0.0
            return

        # Perform Delaunay triangulation on the Points
        delaunay = Delaunay(Points)
        TotalArea = 0.0

        # Loop through each simplex (triangle) in the triangulation
        for Simplex in delaunay.simplices:
            # Get the vertices of the triangle
            p0, p1, p2 = Points[Simplex]
            # Calculate the vectors for two sides of the triangle
            Vec1 = p1 - p0
            Vec2 = p2 - p0
            # Calculate the cross product of the vectors
            CrossProd = np.cross(Vec1, Vec2)
            # The area of the triangle is half the magnitude of the cross product
            TriangleArea = 0.5 * np.linalg.norm(CrossProd)
            TotalArea += TriangleArea

        self.Area = TotalArea


class Surface2D(Surface):
    def __init__(self, LNode, Axis, Name=None):
        super().__init__(LNode, Name)
        self.Axis = Axis

    @property
    def getAxis(self):
        return self.Axis

    @getAxis.setter
    def getAxis(self, Axis):
        self.Axis = Axis

    def PLT2DSurface(self, paramPLT):
        xFill = []
        yFill = []
        zFill = []
        for node in self.getNodes:
            xFill.append(node.getx)
            yFill.append(node.gety)
            zFill.append(node.getz)

        if self.getAxis[0] == 1:
            Absc = xFill
        elif self.getAxis[0] == 2:
            Absc = yFill
        else:
            Absc = zFill

        if self.getAxis[1] == 1:
            Ordo = xFill
        elif self.getAxis[1] == 2:
            Ordo = yFill
        else:
            Ordo = zFill
        if paramPLT.getHatch == '':
            plt.fill(Absc, Ordo,
                     color=paramPLT.getColour,
                     zorder=0, label=paramPLT.getLegends)
        else:
            plt.fill(Absc, Ordo,
                     facecolor=paramPLT.getColour, edgecolor='black',
                     hatch=paramPLT.getHatch, zorder=0, label=paramPLT.getLegends)



"""
Volume
"""
"""
Should allow to define from trim body compute intersection, Extrusion from surface
"""
class Volume:
    def __init__(self, LSurface, Name=None):
        self.LSurface = LSurface
        self.SpaceDim = None
        self.Area = None
        self.Volume = None
        self.Name = Name
        """
        self.UpdateSpaceDim
        self.UpdatePerimeter
        self.UpdateArea
        """


