
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import load_graph_with_attributes, visualize_graph, identify_clusters, highlight_nodes, bfs_traversal, create_binary_search_tree, search_node, calculate_centrality, in_order_traversal

class SocialNetworkAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Network Analysis Tool")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2B2B2B')

        self.graph = None
        self.scale_factor = 1.0
        self.current_scale = 1.0

        self.build_menu()
        self.build_main_frame()

    def build_menu(self):
        menubar = tk.Menu(self.root, bg="#333333", fg="#FFFFFF", font=('Helvetica', 10))
        filemenu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="#FFFFFF")
        filemenu.add_command(label="Open Dataset", command=self.open_dataset)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def build_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg='#2B2B2B')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = tk.Frame(self.main_frame, bg='#2B2B2B')
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_frame = tk.Frame(self.main_frame, bg='#800080', padx=10, pady=10)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.graph_canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 8)), master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.action_label = tk.Label(self.output_frame, text="Select action:", bg='#3C3F41', fg='white', font=('Helvetica', 12, 'bold'))
        self.action_label.pack(pady=5)

        self.action_var = tk.StringVar()
        self.action_dropdown = ttk.Combobox(self.output_frame, textvariable=self.action_var, values=["Identify Clusters", "Highlight Nodes", "BFS Traversal", "Create Binary Search Tree", "Search Node", "Calculate Centrality"], state="readonly")
        self.action_dropdown.pack()

        self.search_label = tk.Label(self.output_frame, text="Enter node to search:", bg='#3C3F41', fg='white', font=('Helvetica', 12, 'bold'))
        self.search_label.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.output_frame, textvariable=self.search_var, state='disabled', font=('Helvetica', 10))
        self.search_entry.pack()

        self.run_button = tk.Button(self.output_frame, text="Run", command=self.execute_action, bg="#4B6EAF", fg="white", font=('Helvetica', 12, 'bold'))
        self.run_button.pack(pady=10)

        self.output_text = tk.Text(self.output_frame, height=10, width=50, bg="#333333", fg="white")
        self.output_text.pack(fill=tk.BOTH, expand=True)

        zoom_frame = tk.Frame(self.output_frame, bg='#3C3F41')
        zoom_frame.pack(fill=tk.X, expand=False)

        self.zoom_in_button = tk.Button(zoom_frame, text="Zoom In", command=self.zoom_in, bg="#4B6EAF", fg="white", font=('Helvetica', 10, 'bold'))
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", command=self.zoom_out, bg="#4B6EAF", fg="white", font=('Helvetica', 10, 'bold'))
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Bind the action_dropdown to a function to enable/disable the search_entry
        self.action_var.trace_add('write', self.enable_search_entry)

    def enable_search_entry(self, *args):
        if self.action_var.get() == "Search Node":
            self.search_entry.config(state='normal')
        else:
            self.search_entry.config(state='disabled')

    def open_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self.graph = load_graph_with_attributes(file_path)
                global highlighted_nodes
                highlighted_nodes = None
                self.visualize_graph()
                messagebox.showinfo("Success", "Dataset loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset:\n{str(e)}")

    def get_unique_colors(self, num_colors):
        colors = plt.cm.tab10.colors
        if num_colors > len(colors):
            extended_colors = plt.cm.get_cmap('tab20', num_colors)
            colors = [extended_colors(i) for i in range(num_colors)]
        return colors

    def visualize_graph(self, cluster_colors=None):
        plt.clf()
        pos = nx.spring_layout(self.graph)
        if cluster_colors:
            for node, color in cluster_colors.items():
                nx.draw(self.graph, pos, nodelist=[node], node_color=color, edge_color='black', node_size=50, width=1)
        else:
            if highlighted_nodes:
                nx.draw(self.graph, pos, nodelist=highlighted_nodes, node_color='red', node_size=50)
            else:
                nx.draw(self.graph, pos, with_labels=False, node_color='blue', edge_color='black', node_size=50, width=1)
        self.graph_canvas.draw()

    def execute_action(self):
        global highlighted_nodes
        self.output_text.delete(1.0, tk.END)

        action = self.action_var.get()
        search_value = self.search_var.get()

        if action == "Identify Clusters":
            clusters = identify_clusters(self.graph)
            colors = self.get_unique_colors(len(clusters))
            cluster_colors = {}
            for idx, cluster in enumerate(clusters):
                for node in cluster:
                    cluster_colors[node] = colors[idx]
            highlighted_nodes = cluster_colors
            self.visualize_graph(cluster_colors=cluster_colors)
            self.output_text.insert(tk.END, f"Clusters: {clusters}\n")
        elif action == "Highlight Nodes":
            highlighted = highlight_nodes(self.graph, min_connections=50)
            highlighted_nodes = highlighted
            self.visualize_graph()
            self.output_text.insert(tk.END, f"Highlighted nodes: {highlighted}\n")
        elif action == "BFS Traversal":
            start_node = list(self.graph.nodes())[0]
            bfs_order = bfs_traversal(self.graph, start_node)
            self.output_text.insert(tk.END, f"BFS traversal order: {bfs_order}\n")
        elif action == "Create Binary Search Tree":
            bst_root = create_binary_search_tree(self.graph)
            bst_traversal = in_order_traversal(bst_root)
            self.output_text.insert(tk.END, f"Binary search tree traversal: {bst_traversal}\n")
        elif action == "Search Node":
            if search_value:
                result = search_node(create_binary_search_tree(self.graph), int(search_value))
                self.output_text.insert(tk.END, f"Node {search_value} found: {result}\n")
            else:
                messagebox.showwarning("Warning", "Please enter a node value to search.")
        elif action == "Calculate Centrality":
            degree_centrality, closeness_centrality = calculate_centrality(self.graph)
            self.output_text.insert(tk.END, f"Closeness Centrality: {closeness_centrality}\n")
        else:
            messagebox.showerror("Error", "Invalid action selected.")
        
    def zoom_in(self):
        # Increase the scale factor for zooming in
            self.current_scale *= 1.2
            self.rescale_graph()

    def zoom_out(self):
    # Decrease the scale factor for zooming out, with a minimum limit
            if self.current_scale > 1:
             self.current_scale /= 1.2
             self.rescale_graph()

    def rescale_graph(self):
    # Apply the current scale to the graph canvas
        fig = self.graph_canvas.figure
        fig.set_size_inches(8 * self.current_scale, 8 * self.current_scale)
        self.graph_canvas.draw()

    def on_press(self, event):
    # Store the mouse click position for panning
        self.x = event.x
        self.y = event.y

    def on_release(self, event):
    # Calculate the distance moved and pan the graph accordingly
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.graph_canvas.get_tk_widget().scan_dragto(deltax, deltay, gain=1)
        
if __name__ == "__main__":
    
    root = tk.Tk()
    app = SocialNetworkAnalysisApp(root)
    root.mainloop()