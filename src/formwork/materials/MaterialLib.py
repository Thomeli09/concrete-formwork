# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 15:43:03 2025

@author: Thommes Eliott
"""

# Material library


# Other Lib
import numpy as np
import shapely as shp

# Custom Lib
from PlotLib import ParamPLT, StartPlots, CloseAllPlots, PLTShow, DefaultParamPLT, PLTPlot

"""
Material : Default class for all the material data
"""
class Material:
    def __init__(self, Name, ID, MatType):
        # Metadata
        self.Name = Name
        self.ID = ID
        self.MatType = MatType

        # Graphics
        self.Color = None
        self.Hatch = None

        # Batch Information
        self.LBatches = []
        
        # Properties
        self.Density = 0  # [float] Density of the material [kg/m^3]
        self.BulkDensity = 0  # [float] Bulk density of the material [kg/m^3]

        # Mechanical Properties
        self.CompStrengthCK = None  # Compressive Strength Characteristic
        self.TensStrengthCK = None  # Tensile Strength Characteristic

        # Experiments
        self.LExperiments = []

    # Metadata
    @property
    def getName(self):
        return self.Name

    @getName.setter
    def getName(self, Name):
        self.Name = Name

    @property
    def getID(self):
        return self.ID

    @getID.setter
    def getID(self, ID):
        self.ID = ID

    @property
    def getMatType(self):
        return self.MatType

    @getMatType.setter
    def getMatType(self, MatType):
        self.MatType = MatType

    # Graphics
    @property
    def getColour(self):
        return self.Color

    @getColour.setter
    def getColour(self, Color):
        self.Color = Color

    # Batch Information
    @property
    def getLBatches(self):
        return self.LBatches

    @getLBatches.setter
    def getLBatches(self, Batch):
        self.LBatches.append(Batch)
        Batch.AddMaterial = self

    def AddBatch(self, Batch):
        self.LBatches.append(Batch)

    # Properties
    @property
    def getDensity(self):
        return self.Density

    @getDensity.setter
    def getDensity(self, Density):
        self.Density = Density

    @property
    def getBulkDensity(self):
        return self.BulkDensity

    @getBulkDensity.setter
    def getBulkDensity(self, BulkDensity):
        self.BulkDensity = BulkDensity

    # Mechanical Properties
    @property
    def getCompStrengthCK(self):
        return self.CompStrengthCK

    @getCompStrengthCK.setter
    def getCompStrengthCK(self, CompStrengthCK):
        self.CompStrengthCK = CompStrengthCK

    @property
    def getTensStrengthCK(self):
        return self.TensStrengthCK

    @getTensStrengthCK.setter
    def getTensStrengthCK(self, TensStrengthCK):
        self.TensStrengthCK = TensStrengthCK

    # Experiments
    @property
    def getExperiments(self):
        return self.LExperiments

    @getExperiments.setter
    def getExperiments(self, Experiment):
        self.LExperiments.append(Experiment)


class MaterialGeom(Material):
    def __init__(self, Name, ID, MatType):
        # Initialize the material
        super().__init__(Name=Name, ID=ID, MatType=MatType)

        # Parent Structure   
        self.ParentOBJ = None # Parent object to which the material belongs (e.g., RVE, aggregate, etc.)

        # Subobjects
        self.VectSubOBJ = None # Vector of the subobjects

        # Generation Data
        self.GenePropDic = {} # Dictionary of the properties used for the generation

        # Properties

        # Geometry
        self.Vertexes = None # Vector of the vertexes [mm]
        self.GeomOBJ = None # Object of the library Shapely to define the geometry
        self.SpaceResolution = None # Spatial resolution of the geometry in [mm]

        # Mesh
        self.Mesh = None # Mesh for the CMPT analysis

        # Displacements and rotations
        self.TransVector = np.array([0.0, 0.0]) # Translation vector [mm]
        self.RotAngle = 0.0 # Rotation angle
        self.BRadAngle = True # Boolean to indicate if the rotation angle is in radians or degrees

    # Parent Structure
    @property
    def getParentOBJ(self):
        return self.ParentOBJ

    @getParentOBJ.setter
    def getParentOBJ(self, ParentOBJ):
        self.ParentOBJ = ParentOBJ

    # Subobjects
    @property
    def getVectSubOBJ(self):
        """Getter for the vector of the subobjects contained"""
        return self.VectSubOBJ

    @getVectSubOBJ.setter
    def getVectSubOBJ(self, VectSubOBJ):
        """Setter for the vector of the subobjects contained"""
        if isinstance(VectSubOBJ, list):
            self.VectSubOBJ = np.asarray(VectSubOBJ, dtype=object)
        elif isinstance(VectSubOBJ, np.ndarray):
            self.VectSubOBJ = VectSubOBJ.astype(object)
        else:
            raise ValueError("Error: VectSubOBJ must be a list or a numpy array.")
    
    # Generation Data
    @property
    def getGenePropDic(self):
        """Getter for the dictionary of the properties used for the generation."""
        return self.GenePropDic

    @getGenePropDic.setter
    def getGenePropDic(self, GenePropDic):
        """Setter for the dictionary of the properties used for the generation."""
        if isinstance(GenePropDic, dict):
            self.GenePropDic = GenePropDic
        else:
            raise ValueError("Error: GenePropDic must be a dictionary.")

    # Properties
    @property
    def getMassCenterSHP(self):
        """Getter for the center of mass of the geometry."""
        return np.asarray(self.getGeomOBJ.centroid, dtype=float)

    @property
    def getAreaSHP(self):
        """Getter for the area of the geometry [mm^2]."""
        return self.getGeomOBJ.area

    @property
    def getPerimeterSHP(self):
        """Getter for the perimeter of the geometry [mm]."""
        return self.getGeomOBJ.length

    # Geometry
    @property
    def getVertexes(self):
        """Getter for the vector of the vertexes of the geometry [mm]."""
        return self.Vertexes

    @getVertexes.setter
    def getVertexes(self, Vertexes):
        """Setter for the vector of the vertexes of the geometry [mm]."""
        if isinstance(Vertexes, list):
            self.Vertexes = np.asarray(Vertexes, dtype=float)
        elif isinstance(Vertexes, np.ndarray):
            self.Vertexes = Vertexes.astype(float)
        else:
            raise ValueError("Error: Vertexes must be a list or a numpy array.")

        self.SetGeomOBJ() # Initialize the shape object

    @property
    def getClosedVertexes(self):
        """Getter for the vector of the closed vertexes of the geometry [mm]."""
        # Add the first vertex at the end of the vector of vertexes to close the shape of the aggregate
        return np.concatenate((self.getVertexes, self.getVertexes[0, 0:2].reshape(1, -1)), axis=0)

    @property
    def SetCenteredMassCenter(self):
        """Function to translate the geometry to center the mass center at the origin of the coordinate system."""
        self.getTransVector = -self.getMassCenterSHP

    @property
    def getGeomOBJ(self):
        return self.GeomOBJ

    @getGeomOBJ.setter
    def getGeomOBJ(self, GeomOBJ):
        self.GeomOBJ = GeomOBJ

    def SetGeomOBJ(self):
        """Function to initialize the geometry object based on the vertexes of the geometry."""
        if self.getVertexes is not None:
            self.GeomOBJ = shp.Polygon(self.getVertexes)
        else:
            raise ValueError("Error: Vertexes must be defined to initialize the shape object of the aggregate.")
    
    @property
    def getSpaceResolution(self):
        """Getter for the spatial resolution of the geometry in [mm]."""
        return self.SpaceResolution

    @getSpaceResolution.setter
    def getSpaceResolution(self, SpaceResolution):
        """Setter for the spatial resolution of the geometry in [mm]."""
        self.SpaceResolution = SpaceResolution

    # Mesh
    @property
    def getMesh(self):
        """Getter for the mesh for the CMPT analysis."""
        return self.Mesh

    @getMesh.setter
    def getMesh(self, Mesh):
        """Setter for the mesh for the CMPT analysis."""
        self.Mesh = Mesh

    # Displacements and rotations
    @property
    def getTransVector(self):
        """Getter for the translation vector [mm]."""
        return self.TransVector

    @getTransVector.setter
    def getTransVector(self, TransVector):
        """Setter for the translation vector [mm]."""
        if isinstance(TransVector, list):
            self.TransVector = np.asarray(TransVector, dtype=float)
        elif isinstance(TransVector, np.ndarray):
            self.TransVector = TransVector.astype(float)
        else:
            raise ValueError("Error: TransVector must be a list or a numpy array.")

        self.getVertexes = self.getCMPTTranslation
        self.getTransVector = np.array([0.0, 0.0])

    @property
    def getRotAngle(self):
        """Getter for the rotation angle in radians."""
        return self.RotAngle

    @getRotAngle.setter
    def getRotAngle(self, RotAngle):
        """Setter for the rotation angle in radians."""
        if self.BRadAngle:
            self.RotAngle = RotAngle
        else:
            self.RotAngle = np.radians(RotAngle)

        self.getVertexes = self.getCMPTRotation
        self.getRotAngle = 0.0
    
    @property
    def getBRadAngle(self):
        """Getter for the boolean to indicate if the rotation angle is in radians or degrees."""
        return self.BRadAngle

    @getBRadAngle.setter
    def getBRadAngle(self, BRadAngle):
        """Setter for the boolean to indicate if the rotation angle is in radians or degrees."""
        if isinstance(BRadAngle, bool):
            self.BRadAngle = BRadAngle
        else:
            raise ValueError("Error: BRadAngle must be a boolean.")

    # CMPT MVMNTs
    # Translation MVMNTs
    @property
    def getCMPTTranslation(self):
        """Function to translate the geometry based on the translation vector."""
        if self.getTransVector is not None:
            return CMPTTranslation(Vertexes=self.getVertexes, TransVector=self.getTransVector)
        else:
            raise ValueError("Error: TransVector must be defined to translate the geometry.")

    # Rotation MVMNTs
    @property
    def getCMPTRotation(self):
        """Function to rotate the geometry based on the rotation angle."""
        if self.getRotAngle is not None:
            return CMPTRotation(Vertexes=self.getVertexes, Angle=self.getRotAngle, BRadAngle=self.getBRadAngle)
        else:
            raise ValueError("Error: RotAngle must be defined to rotate the geometry.")

    # Combined MVMNTs
    @property
    def getCMPTMVMNT(self):
        """Function to translate and rotate the geometry based on the translation vector and rotation angle."""
        if self.getRotAngle is not None:
            RotatedVertexes = CMPTRotation(Vertexes=self.getVertexes, Angle=self.getRotAngle, BRadAngle=self.getBRadAngle)
        else:
            raise ValueError("Error: RotAngle must be defined to rotate the geometry.")

        if self.getTransVector is not None:
            TranslatedVertexes = CMPTTranslation(Vertexes=RotatedVertexes, TransVector=self.getTransVector)
        else:
            raise ValueError("Error: TransVector must be defined to translate the geometry.")

        return TranslatedVertexes

    # PLT
    def PLTGeom(self, paramPLT=None, BStart=True, BEnd=True, BDefaultParam=True):
        """
        Plot the shape of the aggregate based on the vertexes of the aggregate.

        Args:
        - paramPLT: Parameters of the plot
        - BStart: Boolean to indicate if the plot starts in a new figure
        - BEnd: Boolean to indicate if the plot ends and shows the figure

        Returns:

        """
        if paramPLT is None:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        paramPLT.getTitle = "Geometry of " + self.getMatType + " " + self.getName
        paramPLT.getXLabel = "X (mm)"
        paramPLT.getYLabel = "Y (mm)"

        if BDefaultParam:
            Temp = [paramPLT.getColour]
            paramPLT.getColour = self.getColour

        # Plot of the geometry
        VertexesMatrix = self.getClosedVertexes

        PLTPlot(XValues=VertexesMatrix[:, 0], YValues=VertexesMatrix[:, 1], 
                paramPLT=paramPLT)

        if BDefaultParam:
            paramPLT.getColour = Temp[0]

        if BEnd:
            PLTShow(paramPLT)

    def PLTMassCenter(self, paramPLT=None, BStart=True, BEnd=True, BDefaultParam=True):
        """
        Plot the center of mass based on the vertexes.

        Args:
        - paramPLT: Parameters of the plot
        - BStart: Boolean to indicate if the plot starts in a new figure
        - BEnd: Boolean to indicate if the plot ends and shows the figure
        - BDefaultParam: Boolean to indicate if the default parameters of the plot are used (e.g., marker, color, etc.)

        Returns:
           
        """
        if paramPLT is None:
            paramPLT = DefaultParamPLT()

        if BStart:
            StartPlots()

        paramPLT.getTitle = "Center of mass of " + self.getMatType + " " + self.getName
        paramPLT.getXLabel = "X (mm)"
        paramPLT.getYLabel = "Y (mm)"

        if BDefaultParam:
            Temp = [paramPLT.getMarker, paramPLT.getMarkerSize, paramPLT.getColour]
            paramPLT.getMarker = 3
            paramPLT.getMarkerSize = 10
            paramPLT.getColour = "red"

        # Plot of the center of mass
        MassCenter = self.getMassCenter

        PLTPlot(XValues=MassCenter[0], YValues=MassCenter[1], 
                paramPLT=paramPLT)

        if BDefaultParam:
            paramPLT.getMarker, paramPLT.getMarkerSize, paramPLT.getColour = Temp

        if BEnd:
            PLTShow(paramPLT)

# CMPT Mouvements
# Translation of vertexes
def CMPTTranslation(Vertexes, TransVector):
    """
    Function to translate the vertexes
    Args:
    - TransVector: Translation vector of vertexes [mm].

    Returns:
    """
    if isinstance(TransVector, (list, np.ndarray)):
        TransVector = np.asarray(TransVector, dtype=float)
    else:
        raise ValueError("Error: TransVector must be a list or a numpy array.")

    # Translate the vertexes
    TranslatedVertexes = Vertexes + TransVector # Translate the vertexes using the translation vector
    return TranslatedVertexes

# Rotation of the material
def CMPTRotation(Vertexes, Angle, BRadAngle=True):
    """
    Function to rotate the vertexes
    Args:
    - Angle: Angle of rotation.
    - BRadAngle: Boolean to indicate if the angle of rotation is in radians (True) or degrees (False).

    Returns:
    """
    if isinstance(Angle, (float)):
        if BRadAngle:
            Theta = Angle # Angle of rotation in radians
        else:
            Theta = np.radians(Angle) # Convert the angle of rotation from degrees to radians
    else:
        raise ValueError("Error: Angle must be a number (float) or None.")

    # Define the rotation matrix
    RotationMatrix = np.array([[np.cos(Theta), -np.sin(Theta)], [np.sin(Theta), np.cos(Theta)]]) # Rotation matrix
    # Rotate the vertexes
    RotatedVertexes = np.dot(Vertexes, RotationMatrix.T) # Rotate the vertexes using the rotation matrix
    return RotatedVertexes