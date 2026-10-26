#-*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:21:57 2025

@author: Thommes Eliott
"""

# Mesh object library
"""
Improovements :
- Utiliser des libraries spécialisées pour la gestion des maillages (e.g. meshio, pygmsh, etc.) pour etre plus efficace.

"""

# Other Lib
import numpy as np

# Custom Lib

class Mesh:
    def __init__(self):
        # Metadata
        self.Name = None # Name of the mesh [-]
        self.ID = None # ID of the mesh [-]

        # Nodes
        self.Nodes = None # Vector of the nodes of the mesh [mm]
        
        # Elements
        self.Elements = None # Vector of the elements of the mesh [mm]





class Element:
    def __init__(self):
        # Metadata
        self.Name = None # Name of the element [-]
        self.ElementType = None # Type of the element (e.g. triangle, quadrilateral, etc.) [-]


        # Nodes
        self.Nodes = None # Vector of the nodes of the element [mm]

    # CMPT Integration
        


class Node:
    def __init__(self, X=None, Y=None, Z=None, ID=None):
        # Coordinates
        self.X = X # X coordinate of the node [mm]
        self.Y = Y # Y coordinate of the node [mm] 
        self.Z = Z # Z coordinate of the node [mm]
        self.ID = ID # ID of the node [-]