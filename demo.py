import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpi4py import MPI

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ranked Vertex Coloring Algorithm")
        self.canvas = None

        self.G = nx.Graph()
        self.G.add_edges_from([(6, 3), (6, 2), (3, 2), (2, 4), (3, 4), (3, 0), (0, 4), (4, 5), (4, 7), (0, 7), (7, 5), (7, 1), (5, 1)])

        # Initialize colors for nodes
        self.color_map = [None] * 8
        self.step = 0

        # Initialize MPI
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

        self.update_graph()

    def update_graph(self):
        if self.step < 8:
            # Update color for the next node
            self.color_map[self.step] = self.get_available_color(self.step)
            self.step += 1

            # Broadcast color_map to all nodes
            self.color_map = self.comm.bcast(self.color_map, root=0)

            # Draw the updated graph
            plt.clf()
            pos = nx.spring_layout(self.G, seed=42)
            nx.draw(self.G, pos, node_color=self.color_map, with_labels=True, font_size=10, node_size=500)
            plt.title(f"Step {self.step}")
            plt.axis("off")

            # Display the graph in Tkinter window
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

            # Schedule the next update
            self.root.after(1000, self.update_graph)
        else:
            plt.close()  # Close the plot when all steps are done

    def get_available_color(self, vertex):
        # Find the lowest available color for the given vertex
        used_colors = set(self.color_map[neighbor] for neighbor in self.G.neighbors(vertex))
        for color in range(len(self.G)):
            if color not in used_colors:
                return color
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
