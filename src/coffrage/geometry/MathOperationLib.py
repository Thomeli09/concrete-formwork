# -*- coding: utf-8 -*-
"""
Created on Tuesday Sept  30 11:20:09 2025

@author: Thommes Eliott
"""

# Library for mathematical operations on data 


# Other Lib
import numpy as np
import pandas as pd
from scipy.signal import medfilt, savgol_filter, butter, filtfilt, bessel, wiener
from scipy import integrate
from scipy.interpolate import CubicSpline, CubicHermiteSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline, make_splrep
from pykalman import KalmanFilter


# Custom Lib
from DataManagementLib import LenData


"""
DataTreatment

# Improvement to be done:
- Add differents data treatment methods
- Add differents links with DataLag class
"""
class DataTreatment:
    def __init__(self):
        pass
        # Data

    def DTMovingAverage(self, Data, FWindow=5):
        """
        Applys a moving average filter to the data.
        From scipy library.
        
        Args:
            Data (array): Input data array.
            FWindow (int): Size of the moving average filter window.

        Returns:
            Data (array): Filtered data array.
        """
        return np.convolve(Data, np.ones(FWindow)/FWindow, mode='same')

    def DTMedianFilter(self, Data, FWindow=5):
        """
        Applys a median filter to the data.
        From scipy library.
        
        Args:
            Data (array): Input data array.
            FWindow (int): Size of the median filter window. Must be an odd integer.
        Returns:
            Data (array): Filtered data array.
        """
        return medfilt(Data, kernel_size=FWindow)

    def DTSavitzkyGolay(self, Data, FWindow=5, PolyOrder=2):
        """
        Applys a Savitzky-Golay filter to the data.
        From scipy library.

        Args:
            Data (array): Input data array.
            FWindow (int): Size of the filter window. Must be an odd integer.
            PolyOrder (int): Order of the polynomial used to fit the samples. Must be less than FWindow.

        Returns:
            Data (array): Filtered data array.
        """
        return savgol_filter(Data, window_length=FWindow, polyorder=PolyOrder)

    def DTButterworth(self, Data, FSample=1.0, FCut=0.1, Order=4, BType='low'):
        """
        Applys a Butterworth filter to the data.
        From scipy library.
        Args:
            Data (array): Input data array.
            FSample (float): Sampling frequency of the data.
            FCut (float): Cutoff frequency of the filter.
            Order (int): Order of the filter.
            BType (str): Type of the filter. Can be 'low', 'high', 'bandpass' or 'bandstop'.
        Returns:
            Data (array): Filtered data array.
        """
        Nyquist = 0.5 * FSample
        NormalCutoff = FCut / Nyquist
        BButter, AButter = butter(N=Order, Wn=NormalCutoff, btype=BType, analog=False)
        return filtfilt(BButter, AButter, Data)

    def DTBessel(self, Data, FSample=1.0, FCut=0.1, Order=4, BType='low'):
        """
        Applys a Bessel filter to the data.
        From scipy library.
        Args:
            Data (array): Input data array.
            FSample (float): Sampling frequency of the data.
            FCut (float): Cutoff frequency of the filter.
            Order (int): Order of the filter.
            BType (str): Type of the filter. Can be 'low', 'high', 'bandpass' or 'bandstop'.

        Returns:
            Data (array): Filtered data array.
        """
        Nyquist = 0.5 * FSample
        NormalCutoff = FCut / Nyquist
        BBessel, ABessel = bessel(N=Order, Wn=NormalCutoff, btype=BType, analog=False)
        return filtfilt(BBessel, ABessel, Data)

    def DTWiener(self, Data, MySize=5, Noise=None):
        """
        Applys a Wiener filter to the data.
        From scipy library.

        Args:
            Data (array): Input data array.
            MySize (int): Size of the Wiener filter window.
            Noise (float): Estimated noise power. If None, it is estimated from the data.

        Returns:
            Data (array): Filtered data array.
        """
        return wiener(Data, mysize=MySize, noise=Noise)

    def DTKalman(self, Data, TransitionMatrix=1, ObservationMatrix=1, InitialStateMean=0, 
                 InitialStateCovariance=1, ObservationCovariance=1, TransitionCovariance=0.01):
        """
        Applys a Kalman filter to the data.
        From pykalman library.

        Args:
            Data (array): Input data array.
            TransitionMatrix (float or array): State transition matrix.
            ObservationMatrix (float or array): Observation matrix.
            InitialStateMean (float or array): Initial state mean.
            InitialStateCovariance (float or array): Initial state covariance.
            ObservationCovariance (float or array): Observation covariance.
            TransitionCovariance (float or array): Transition covariance.

        Returns:
            Data (array): Filtered data array.
        """
        kf = KalmanFilter(transition_matrices=TransitionMatrix,
                          observation_matrices=ObservationMatrix,
                          initial_state_mean=InitialStateMean,
                          initial_state_covariance=InitialStateCovariance,
                          observation_covariance=ObservationCovariance,
                          transition_covariance=TransitionCovariance)
        StateMeans, _ = kf.filter(Data)
        return StateMeans.flatten()

# Math functions
def CMPTDerivativeFirst(DataVal, DataAbs=None):
    """
    Computes the numerical derivative of the data.
    
    Args:
        DataVal (array): Input data array.
        DataAbs (array): Optional array of time or x-values corresponding to DataVal.
        Derivative (array): Numerical derivative of the data.
    """
    DataVal = np.asarray(DataVal)
    if DataAbs is None:
        # Assume uniform spacing
        Derivative = np.gradient(DataVal)
    else:
        DataAbs = np.asarray(DataAbs)
        Derivative = np.gradient(DataVal, DataAbs)
    return Derivative

def CMPTIntegralTrap(VectDerivative, DataAbs=None, FInitialVal=0, FDx=1.0):
    """
    Computes the numerical integral of the data using the trapezoidal rule.
    
    Args:
        VectDerivative (array): Numerical derivative of the data.
        DataAbs (array): Optional array of time or x-values corresponding to DataVal.
        FInitialVal (float): Optional initial value for the integral.
        FDx (float): Optional spacing between data points if DataAbs is not provided.
        
    Returns:
        Integral (array): Numerical integral of the data.
    """
    Derivative = np.asarray(VectDerivative, dtype=float)

    if DataAbs is None:
        # Assume uniform spacing
        Integral = integrate.cumulative_trapezoid(y=Derivative, dx=FDx, initial=FInitialVal)
    else:
        DataAbs = np.asarray(DataAbs, dtype=float)
        # Check if DataAbs is the same length as Derivative
        if LenData(DataAbs) != LenData(Derivative):
            print("Error: DataAbs and Derivative must have the same length.")
            return None

        # Trapezoidal integration
        Integral = integrate.cumulative_trapezoid(y=Derivative, x=DataAbs, initial=FInitialVal)
    return Integral

def CMPTInterpolationLinear(XPointData, YPointData, XNew, ValLeft=0, ValRight=0):
    """
    Performs linear interpolation on the given data.
    
    Args:
        XPointData (array): Known x-values.
        YPointData (array): Known y-values.
        XNew (array): New x-values to interpolate.
        ValLeft (float): Value to return for x-values less than the minimum of XPointData.
        ValRight (float): Value to return for x-values greater than the maximum of XPointData.
        
    Returns:
        YNew (array): Interpolated y-values corresponding to XNew.
    """
    XPointData = np.asarray(XPointData)
    YPointData = np.asarray(YPointData)
    XNew = np.asarray(XNew)

    if LenData(XPointData) != LenData(YPointData):
        print("Error: XPointData and YPointData must have the same length.")
        return None
    
    YNew = np.interp(x=XNew, xp=XPointData, fp=YPointData, left=ValLeft, right=ValRight)
    return YNew

def CMPTInterpolationSpline(XPointData, YPointData, XNew, Method='CubicSpline', ValLeft=0, ValRight=0, Derivatives=None):
    """
    Performs spline interpolation on the given data using various methods.
    
    Args:
        XPointData (array): Known x-values.
        YPointData (array): Known y-values.
        XNew (array): New x-values to interpolate.
        Method (str): Interpolation method. Options are 'CubicSpline', 'Pchip', 'Akima', 'BSpline'.
        ValLeft (float): Value to return for x-values less than the minimum of XPointData.
        ValRight (float): Value to return for x-values greater than the maximum of XPointData.
        Derivatives (array): Optional derivatives for 'CubicHermite' method.
        
    Returns:
        YNew (array): Interpolated y-values corresponding to XNew.
    """
    
    XPointData = np.asarray(XPointData)
    YPointData = np.asarray(YPointData)
    XNew = np.asarray(XNew)

    if LenData(XPointData) != LenData(YPointData):
        print("Error: XPointData and YPointData must have the same length.")
        return None

    if Method == 'CubicSpline' or Method == 0:
        """ Interpolate data with a piecewise cubic polynomial, C2 continuous. """
        SplineFunc = CubicSpline(x=XPointData, y=YPointData, bc_type='natural', extrapolate=False)

    elif Method == 'CubicHermite' or Method == 1:
        """ Interpolate data with a piecewise cubic Hermite interpolating polynomial, C1 continuous. """
        if Derivatives is None:
            Derivatives = CMPTDerivativeFirst(YPointData, XPointData)
            print("Warning: Derivatives not provided. Computed using first numerical derivative.")
        SplineFunc = CubicHermiteSpline(x=XPointData, y=YPointData, dydx=Derivatives, extrapolate=False)

    elif Method == 'Pchip' or Method == 2:
        """ Interpolate data with a piecewise cubic Hermite interpolating polynomial, C1 continuous. 
        Preserves monotonicity in the interpolation data and does not overshoot if the data is not smooth. """
        SplineFunc = PchipInterpolator(x=XPointData, y=YPointData, extrapolate=False)

    elif Method == 'Akima' or Method == 3:
        """ Interpolate data with an Akima1DInterpolator, C1 continuous. 
        Leads to visually pleasing results for non-smooth data. """
        SplineFunc = Akima1DInterpolator(x=XPointData, y=YPointData, method='akima', extrapolate=False)

    elif Method == 'BSpline' or Method == 4:
        """ Interpolate data with a B-Spline representation """
        SplineFunc = make_interp_spline(XPointData, YPointData)

    elif Method == 'BSplineParametric' or Method == 5:
        """ Interpolate data with a B-Spline representation depending on parameters """
        SplineFunc = make_splrep(XPointData, YPointData, s=0.01)

    else:
        print("Error: Unknown interpolation method.")
        return None

    YNew = SplineFunc(XNew)

    # Handle out-of-bounds values
    YNew[XNew < np.min(XPointData)] = ValLeft
    YNew[XNew > np.max(XPointData)] = ValRight
    return YNew