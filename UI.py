# ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import load_graph_with_attributes, visualize_graph, identify_clusters, highlight_nodes, bfs_traversal, create_binary_search_tree, search_node, calculate_centrality, in_order_traversal  # Importing in_order_traversal

class SocialNetworkAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Network Analysis Tool")
        self.root.geometry("800x600")

        self.graph = None
        self.scale_factor = 1.0
        self.x = None
        self.y = None

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

        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_canvas = FigureCanvasTkAgg(plt.figure(figsize=(6, 6)), master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph_canvas.mpl_connect('button_press_event', self.on_press)
        self.graph_canvas.mpl_connect('button_release_event', self.on_release)

        self.action_label = tk.Label(self.output_frame, text="Select action:")
        self.action_label.pack(pady=5)

        self.action_var = tk.StringVar()
        self.action_dropdown = ttk.Combobox(self.output_frame, textvariable=self.action_var, values=["Identify Clusters", "Highlight Nodes", "BFS Traversal", "Create Binary Search Tree", "Search Node", "Calculate Centrality"])
        self.action_dropdown.pack()

        self.search_label = tk.Label(self.output_frame, text="Enter node to search:")
        self.search_label.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.output_frame, textvariable=self.search_var, state='disabled')  # Disabled by default
        self.search_entry.pack()

        self.run_button = tk.Button(self.output_frame, text="Run", command=self.execute_action)
        self.run_button.pack(pady=10)

        self.output_text = tk.Text(self.output_frame, height=10, width=50)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.zoom_in_button = tk.Button(self.output_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.output_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Bind the action_dropdown to a function to enable/disable the search_entry
        self.action_var.trace_add('write', self.enable_search_entry)

    def enable_search_entry(self, *args):
        # Enable the search_entry if "Search Node" is selected, disable otherwise
        if self.action_var.get() == "Search Node":
            self.search_entry.config(state='normal')
        else:
            self.search_entry.config(state='disabled')

    def open_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self.graph = load_graph_with_attributes(file_path)
                self.visualize_graph()
                messagebox.showinfo("Success", "Dataset loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset:\n{str(e)}")

    def visualize_graph(self):
        plt.clf()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=False, node_size=20, edge_color="gray", linewidths=0.1)
        self.graph_canvas.draw()

    def execute_action(self):
        self.output_text.delete(1.0, tk.END)
        
        action = self.action_var.get()
        search_value = self.search_var.get()

        if action == "Identify Clusters":
            clusters = identify_clusters(self.graph)
            self.output_text.insert(tk.END, f"Clusters: {clusters}\n")
        elif action == "Highlight Nodes":
            highlighted = highlight_nodes(self.graph, min_connections=5)
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
            self.output_text.insert(tk.END, f"Degree Centrality: {degree_centrality}\n")
            self.output_text.insert(tk.END, f"Closeness Centrality: {closeness_centrality}\n")
        else:
            messagebox.showerror("Error", "Invalid action selected.")

    def zoom_in(self):
        self.scale_factor *= 1.2
        self.graph_canvas.get_tk_widget().scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def zoom_out(self):
        self.scale_factor /= 1.2
        self.graph_canvas.get_tk_widget().scale("all", 0, 0, self.scale_factor, self.scale_factor)

    def on_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_release(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.graph_canvas.get_tk_widget().move("all", deltax, deltay)

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkAnalysisApp(root)
    root.mainloop()
