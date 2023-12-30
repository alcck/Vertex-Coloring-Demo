from mpi4py import MPI
import networkx as nx
import matplotlib.pyplot as plt

class GraphColoring:
    def __init__(self, graph, comm):
        self.graph = graph
        self.comm = comm
        self.rank = comm.Get_rank()
        self.size = comm.Get_size()
        

    def get_connected_components(self):
        components = []
        for component_nodes in nx.connected_components(self.graph):
            components.append(set(component_nodes))
        return components

    def color_connected_components(self):
        components = self.get_connected_components()
        for round_number in range(len(components)):
            if round_number % self.size == self.rank:
                for comp_idx, comp_nodes in enumerate(components):
                    if comp_idx == round_number:
                        self.color_component(comp_nodes)

    def color_component(self, component_nodes):
        # Sort nodes by rank in descending order
        sorted_nodes = sorted(component_nodes, key=lambda node: -node)

        color_map = {}

        for node in sorted_nodes:
            available_colors = set(range(len(self.graph.nodes)))
            for neighbor in self.graph.neighbors(node):
                neighbor_color = color_map.get(neighbor, None)
                if neighbor_color in available_colors:
                    available_colors.remove(neighbor_color)
            if available_colors:
                color_map[node] = min(available_colors)

        colors_list = [color_map.get(node, None) for node in self.graph.nodes]
        self.graph.graph["coloring"] = colors_list


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Given edge list
    edges = [(6, 3), (6, 2), (3, 2), (2, 4), (3, 4), (3, 0), (0, 4), (4, 5), (4, 7), (0, 7), (7, 5), (7, 1), (5, 1)]

    # Create a graph
    G = nx.Graph()
    G.add_edges_from(edges)

    coloring = GraphColoring(G, comm)
    coloring.color_connected_components()

    if rank == 0:
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color=G.graph["coloring"], with_labels=True, font_size=10, node_size=500)
        plt.title("Colored Graph")
        plt.axis("off")
        plt.show()