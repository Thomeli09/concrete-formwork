# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:16:36 2024

@author: Thommes Eliott
"""

# Rheology library

# Other Lib

from ElementLib import Element
# from GeometryLib import Line


# R Rheology, E Element

class RElement(Element):
    def __init__(self):
        self.data = True  # Section easy by default


class REDamper(RElement):
    def __init__(self, section):
        self.Section = section  # Section easy by default


class RESpring(RElement):
    def __init__(self, section):
        self.Section = section  # Section easy by default
