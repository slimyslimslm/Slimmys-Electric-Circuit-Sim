import pygame 

class ElectricCircuit:
    def __init__(self, components):
        if type(components) != list:
            raise TypeError("Electric Circuit components must be a list of CircuitComponents")
        self.components = components 

    def __add__(self, other):
        return ElectricCircuit(self.components + other.components)

    def __len__(self):
        return len(self.components)
    
    def is_closed(self, starting_component=None) -> bool:
        """Determines whether the circuit is closed or not"""
        if starting_component is not None and starting_component not in self.components:
            raise ValueError("Starting component not in self.components")
        
        elif len(self.components) == 0:
            return True 

        elif starting_component is None:
            start = self.components[0]
        
        else:
            start = starting_component 

        stack = []

        for component in start.right_components:
            stack.append(component)

        previous = start 

        while stack != []:
            node = stack.pop()

            print(node.name, start.name)

            if node is start:
                return True 
            if node in previous.left_components:
                stack.extend([c for c in node.right_components])
            elif node in previous.right_components:
                stack.extend([c for c in node.left_components])

            previous = node 

        return False 


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
