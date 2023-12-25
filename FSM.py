import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges for the FSM
G.add_edges_from([
    ('Initialization (S0)', 'Color Selection (S1)', {'label': 'unassigned'}),
    ('Color Selection (S1)', 'Communication (S2)', {'label': 'assigned'}),
    ('Communication (S2)', 'Color Selection (S1)', {'label': 'notify neighbors'}),
    ('Color Selection (S1)', 'Termination (S3)', {'label': 'all nodes assigned colors'}),
])

# Set node attributes for label and shape
node_attributes = {
    'Initialization (S0)': {'shape': 'box'},
    'Color Selection (S1)': {'shape': 'box'},
    'Communication (S2)': {'shape': 'box'},
    'Termination (S3)': {'shape': 'box'},
}

nx.set_node_attributes(G, node_attributes)

# Set edge labels
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}

# Draw the FSM
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold', arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title('Finite State Machine (FSM) for Algorithm')
plt.show()
