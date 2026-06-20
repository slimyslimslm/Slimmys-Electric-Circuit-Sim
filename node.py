import pygame 
from circuit_component import *

class Node:
    def __init__(self, end_components=[], internal_wires=[]):
        self.end_components = end_components
        self.internal_wires = internal_wires 
    
    def add_wire(self, wire):
        """Adds circuit components that are only wires"""
        self.internal_wires.append(wire)
    
    def add_component(self, component):
        """Adds circuit components that are not wires"""
        self.end_components.append(component)