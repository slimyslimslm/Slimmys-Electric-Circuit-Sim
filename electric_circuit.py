import pygame 
from node import Node 

class ElectricCircuit:
    def __init__(self, components):
        if type(components) != list:
            raise TypeError("Electric Circuit components must be a list of CircuitComponents")
        self.components = components 
        
        self.nodes = []

        self.total_resistance = 0

    def __add__(self, other):
        return ElectricCircuit(self.components + other.components)

    def __len__(self):
        return len(self.components)
    
    def is_closed(self, side, starting_component=None) -> bool:
        """Determines whether the circuit is closed or not"""
        if starting_component is not None and starting_component not in self.components:
            raise ValueError("Starting component not in self.components")
        
        elif len(self.components) == 0:
            return True 

        elif starting_component is None:
            start = self.components[0]
        
        else:
            start = starting_component 

        if side == "Right":
            stack = [c for c in start.right_components]
        else: # side == "Left":
            stack = [c for c in start.left_components]

        previous = start 
        visited = {start}

        while stack != []:
            node = stack.pop()

            # print(node.name, start.name)

            if node is start:
                return True 
            elif node in visited:
                return False 
            elif previous in node.left_components:
                stack.extend([c for c in node.right_components])
                visited.add(node)
            elif previous in node.right_components:
                stack.extend([c for c in node.left_components])
                visited.add(node)

            previous = node 

        return False 
    
    def node_of_component(self, component) -> Node | None:
        """Returns the node the component is a part of. Returns None if component is not in any nodes"""
        for node in self.nodes:
            if component in node.end_components or component in node.internal_wires:
                return node 
            
        return None 
    
    def _calculate_series_resistance(self, r1: float , r2: float) -> float:
        """Given two, resistances, calculate the equivalent resistance in series"""
        return r1 + r2

    def _calculate_parallel_resistance(self, r1: float, r2: float) -> float:
        """Given two resistances, calculate the equivalent resistance in parallel"""
        return 1 / ((1/r1) + (1/r2))
    
    def voltage2(self) -> float:
        """Attempt to calculate equivalent voltage using Kirchoff's voltage law"""
        voltage = 0 
        for component in self.components:
            if component.name == "Battery" and self.is_closed("Left", component) and self.is_closed("Right", component):
                start = component
                break
        else:
            return voltage
    
    def calculate_equivalent_voltage(self) -> float:
        """
        Calculate the equivalent voltage of the circuit
        Preconditions: Assume there are no branches and that the circuit is closed 
        """
        voltage = 0 
        for component in self.components:
            if component.name == "Battery" and self.is_closed("Left", component) and self.is_closed("Right", component):
                start = component
                voltage += component.voltage
                break
        else:
            return voltage
        
        stack = [c for c in start.right_components]
        visited = {start}
        previous = start 

        while stack != []:
            node = stack.pop()

            if node is start and previous in start.left_components:
                return voltage
            elif previous in node.left_components:
                stack.extend([c for c in node.right_components])
                if node.name == "Battery":
                    voltage += node.voltage
            else: # previous in node.right_components
                stack.extend([c for c in node.left_components])
                if node.name == "Battery":
                    voltage -= node.voltage 

            visited.add(node)
            previous = node 

    
    def calculate_equivalent_resistance(self) -> float:
        """Calculate the equivalent resistance of the circuit, and the resistance of each branch"""
        """FOR NOW, ASSUME THERE ARE NO BRANCHES"""
        """Preconditions: Assume the circuit is closed"""
        resistance = 0

        start = self.components[0]
        if start.name == "Resistor" and self.is_closed("Left", start) and self.is_closed("Right", start):
            resistance += start.resistance

        stack = []
        stack.extend([c for c in start.right_components])
        visited = {start}

        while stack != []:
            node = stack.pop()

            if node not in visited:
                if node.name == "Resistor":
                    resistance += node.resistance
                visited.add(node)
                
                for component in node.right_components + node.left_components:
                    stack.append(component)
        
        return resistance 
    
    def calculate_current(self) -> float:
        voltage = self.calculate_equivalent_voltage()
        resistance = self.calculate_equivalent_resistance()
        if resistance == 0:
            return 0
        
        return voltage / resistance 

"""
class ElectricCircuit:
    def __init__(self):
        self._adj_list = {}

    def add(self, node: int, neighbors: list[int]) -> None:
        Adds neighbors to node. If node does not exist, node is created
            If a new neighbor is not in graph, a new node is generated
        if node not in self._adj_list:
            self._adj_list[node] = neighbors
        else:
            self._adj_list[node] = self._adj_list[node].extend(neighbors)
        
        for n in neighbors:
            if n not in self._adj_list:
                self._adj_list[n] = []
    
    def __str__(self) -> str:
        str = ""
        for key, value in self._adj_list.items():
            str += (f"{key.name}: {value.name}\n")
        
        return str
"""    
