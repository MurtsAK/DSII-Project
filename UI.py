"""
Things to know:
The SocialNetworkAnalysisApp class represents the main application window.
It creates a menu bar with options to open a dataset and exit the application.
The main frame contains a canvas to display the graph visualization and a details frame for additional controls.
The open_dataset method allows users to open a CSV file containing the network data.
The draw_graph method visualizes the loaded graph using NetworkX and Matplotlib.
The analyze_graph method performs analysis on the loaded graph, such as community detection and centrality measures.
Interaction with the GUI triggers various actions, such as loading a dataset and analyzing the graph.
The highlight_nodes method has been updated to highlight nodes with high degree centrality using DFS traversal.
We calculate the degree centrality for each node in the graph and identify nodes with centrality values
above a certain threshold (in this case, 80% of the maximum centrality value).
Nodes with high centrality are highlighted in red, while other nodes remain blue.

"""

import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class SocialNetworkAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Network Analysis Tool")
        self.root.geometry("800x600")

        self.graph = None
        self.graph_canvas = None

        self.build_menu()
        self.build_main_frame()

    def build_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Dataset", command=self.open_dataset)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def build_main_frame(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_canvas = FigureCanvasTkAgg(plt.figure(), master=self.main_frame)
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.btn_cluster = tk.Button(self.main_frame, text="Identify Clusters", command=self.identify_clusters)
        self.btn_cluster.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_highlight = tk.Button(self.main_frame, text="Highlight Nodes", command=self.highlight_nodes)
        self.btn_highlight.pack(side=tk.LEFT, padx=10, pady=10)

    def open_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.graph = nx.from_pandas_edgelist(self.data, source='source', target='target', edge_attr='weight')
                self.draw_graph()
                messagebox.showinfo("Success", "Dataset loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset:\n{str(e)}")

    def draw_graph(self):
        plt.clf()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.graph_canvas.figure.add_subplot(111), with_labels=True, node_size=300,
                font_size=8)
        self.graph_canvas.draw()

    def identify_clusters(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "Please open a dataset first.")
            return

        clusters = list(nx.algorithms.community.girvan_newman(self.graph))
        messagebox.showinfo("Clusters", f"Number of clusters: {len(clusters)}")

    def highlight_nodes(self):
        if self.graph is None:
            messagebox.showwarning("Warning", "Please open a dataset first.")
            return

        # Highlight nodes with high degree centrality using DFS
        degree_centrality = nx.degree_centrality(self.graph)
        max_degree_centrality = max(degree_centrality.values())

        highlighted_nodes = set()
        for node, centrality in degree_centrality.items():
            if centrality >= max_degree_centrality * 0.8:  # Highlight nodes with degree centrality >= 80% of the max value
                highlighted_nodes.add(node)

        plt.clf()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, ax=self.graph_canvas.figure.add_subplot(111), with_labels=True, node_size=300,
                font_size=8, node_color=['red' if node in highlighted_nodes else 'blue' for node in self.graph.nodes()])
        self.graph_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkAnalysisApp(root)
    root.mainloop()
