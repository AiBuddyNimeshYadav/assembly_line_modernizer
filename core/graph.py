import networkx as nx

class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_dependency(self, file_node, dependency_node):
        self.graph.add_edge(file_node, dependency_node)
        
    def get_execution_order(self):
        # Topological sort to determine what to build first
        return list(nx.topological_sort(self.graph))
