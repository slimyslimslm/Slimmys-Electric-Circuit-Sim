class ElectricCircuit:
    def __init__(self):
        self._adj_list = {}

    def add(self, node: int, neighbors: list[int]) -> None:
        """Adds neighbors to node. If node does not exist, node is created
            If a new neighbor is not in graph, a new node is generated"""
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
    
