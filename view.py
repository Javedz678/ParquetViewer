import tkinter as tk
from tkinter import ttk, filedialog


class ApplicationView:
    def __init__(self, root):
        self.root = root
        self.root.title("Javed's Parquet Viewer")
        self.root.state('zoomed')
        self.create_widgets()

    def create_widgets(self):
        self.open_button = ttk.Button(self.root, text="Open Parquet File", command=self.open_file_dialog)
        self.open_button.pack(pady=10)

        self.query_frame = ttk.Frame(self.root)
        self.query_frame.pack(fill=tk.X, padx=10, pady=10)

        self.query_label = ttk.Label(self.query_frame, text="Enter query:")
        self.query_label.pack(side=tk.TOP)

        self.query_entry = ttk.Entry(self.query_frame, width=50, state="disabled")
        self.query_entry.pack(side=tk.TOP, padx=(5, 0))

        self.query_button = ttk.Button(self.query_frame, text="Apply Query", command=self.apply_query, state="disabled")
        self.query_button.pack(side=tk.TOP, padx=(5, 0))

        self.schema_button = ttk.Button(self.root, text="Show Schema", command=self.show_schema, state="disabled")
        self.schema_button.pack(side=tk.TOP, padx=10, pady=10)

        self.json_button = ttk.Button(self.root, text="Convert full file to JSON", command=self.convert_to_json,
                                      state="disabled")
        self.json_button.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.treeview = ttk.Treeview(self.frame)
        self.x_scrollbar = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.treeview.xview)
        self.y_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select Parquet File", filetypes=[("Parquet Files", "*.parquet")])
        if file_path:
            return file_path

    def populate_treeview(self, data):
        if data is None:
            return

        self.treeview.delete(*self.treeview.get_children())

        self.treeview["columns"] = list(data.columns)
        self.treeview["show"] = "headings"
        for col_index, col_name in enumerate(data.columns):
            self.treeview.heading(col_name, text=col_name)
            self.treeview.column(col_name, width=100)  # Initial width

        for row in data.itertuples(index=False, name=None):
            self.treeview.insert("", "end", values=row)

        for col_index, col_name in enumerate(data.columns):
            max_width = max(data[col_name].astype(str).apply(lambda x: len(str(x))).max(), len(col_name))
            self.treeview.column(col_name, width=max_width * 10)

        total_width = sum(self.treeview.column(col, "width") for col in self.treeview["columns"])
        self.root.geometry(f"{total_width + 200}x800")

    def enable_features(self):
        self.schema_button.config(state="normal")
        self.query_button.config(state="normal")
        self.json_button.config(state="normal")
        self.query_entry.config(state="normal")

    def disable_features(self):
        self.schema_button.config(state="disabled")
        self.query_button.config(state="disabled")
        self.json_button.config(state="disabled")
        self.query_entry.config(state="disabled")

    def apply_query(self):
        pass

    def show_schema(self):
        pass

    def convert_to_json(self):
        pass
