class Graph:
    """
    Implementation of a directed graph using an adjacent list
    
    Instance Attributes:
        - _adj_list: the adjacent list represented with a Python dictionary
    """

    _adj_list: dict

    def __init__(self, adj_list=None) -> None:
        "Intializes a new graph with an empty adj list or a provided one"
        if adj_list is None:
            self._adj_list = {}
        else:
            self._adj_list = adj_list
    
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

    def remove(self, node: int) -> None:
        """Removes the node passed in, or does nothing if the node passed it is not in the graph"""
        for key in self._adj_list.keys():
            if key == node:
                self._adj_list.pop(node)
                break 
        else:
            return 
        
        for value in self._adj_list.values:
            if node in value:
                value.remove(node)
 
    def _depth(self, starting_node: int, already_visited=set()) -> list[int]:
        """
        Depth first search algorithim beginning at starting_node

        Precondition: starting_node is key in self._adj_list
        """

        order = []
        if self._adj_list == {}:
            return [], {}

        if starting_node not in already_visited:
            order.append(starting_node)
            already_visited.add(starting_node)

        for neighbor in self._adj_list[starting_node]:
            if neighbor not in already_visited:
                add_orders, add_visited = self._depth(neighbor, already_visited)
                order.extend(add_orders)
                already_visited = already_visited.union(add_visited)

        return order, already_visited
    
    def depth_first_search(self, starting_node: int) -> list[int]:
        return self._depth(starting_node)[0]
    
    def __str__(self) -> str:
        str = ""
        for key, value in self._adj_list.items():
            str += (f"{key}: {value}\n")
        
        return str
    

graph = Graph()
graph.add(1, [2])
graph.add(3, [1])

print(graph)


"""
    3: [4],
    4: [5],
    5: []
"""