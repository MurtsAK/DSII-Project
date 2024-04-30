# graph.py

import networkx as nx

def load_graph_with_attributes(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            node1, node2 = parts[0], parts[1]
            attributes = {k: v for k, v in (attr.split('=') for attr in parts[2:])} if len(parts) > 2 else {}
            G.add_edge(node1, node2, **attributes)
    return G

def identify_clusters(G):
    clusters = list(nx.algorithms.community.greedy_modularity_communities(G))
    return clusters

def highlight_nodes(G, attribute=None, min_connections=None):
    highlighted = []
    for node, attrs in G.nodes(data=True):
        if attribute and attribute in attrs and attrs[attribute]:
            highlighted.append(node)
        elif min_connections is not None and G.degree[node] >= min_connections:
            highlighted.append(node)
    return highlighted

def visualize_graph(G, highlight_nodes=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=20, edge_color="gray", linewidths=0.1)
    if highlight_nodes:
        nx.draw_networkx_nodes(G,pos, with_labels=True, nodelist=highlight_nodes, node_color='r', node_size=50)
    plt.show()

def bfs_traversal(G, start_node):
    traversal_order = list(nx.bfs_tree(G, source=start_node))
    return traversal_order

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert_node(root, data):
    if not root:
        return TreeNode(data)
    
    if data < root.data:
        root.left = insert_node(root.left, data)
    else:
        root.right = insert_node(root.right, data)
    
    return root

def in_order_traversal(root):
    traversal = []
    if root:
        traversal = in_order_traversal(root.left)
        traversal.append(root.data)
        traversal = traversal + in_order_traversal(root.right)
    return traversal

def create_binary_search_tree(G):
    root = None
    for node in G.nodes():
        root = insert_node(root, node)
    return root

def search_node(root, target):
    while root:
        if int(root.data) == int(target):
            return True
        elif int(root.data) < int(target):
            root = root.right
        else:
            root = root.left
    return False

def detect_communities(G):
    return list(nx.algorithms.community.girvan_newman(G))

def calculate_centrality(G):
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    return degree_centrality, closeness_centrality

class SpatialHashTable:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.table = {}

    def hash(self, x, y):
        return (int(x / self.cell_size), int(y / self.cell_size))

    def insert(self, x, y, node):
        key = self.hash(x, y)
        if key not in self.table:
            self.table[key] = []
        self.table[key].append(node)

    def query(self, x, y):
        key = self.hash(x, y)
        return self.table.get(key, [])

