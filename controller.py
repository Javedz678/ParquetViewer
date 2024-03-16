import tkinter as tk
from tkinter import filedialog, messagebox
from view import ApplicationView
from model import ParquetModel


class ApplicationController:
    def __init__(self):
        self.model = ParquetModel()
        self.view = ApplicationView(tk.Tk())
        self.setup_events()
        self.data = None

    def setup_events(self):
        self.view.open_button.config(command=self.open_file_dialog)
        self.view.query_button.config(command=self.apply_query)
        self.view.schema_button.config(command=self.show_schema)
        self.view.json_button.config(command=self.convert_to_json)

    def open_file_dialog(self):
        file_path = self.view.open_file_dialog()
        if file_path:
            self.load_parquet_file(file_path)
        else:
            self.view.disable_features()

    def load_parquet_file(self, file_path):
        try:
            self.data = self.model.read_parquet_file(file_path)
            self.view.populate_treeview(self.data)
            self.view.enable_features()
        except Exception as e:
            messagebox.showerror("Error", repr(e))

    def apply_query(self):
        query = self.view.query_entry.get()
        if query:
            try:
                filtered_data = self.model.query_data(self.data, query)
                self.view.populate_treeview(filtered_data)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            self.view.populate_treeview(self.data)

    def show_schema(self):
        if self.data is not None:  # Check if data is loaded
            schema = self.model.get_schema(self.data)
            messagebox.showinfo("Schema", schema)
        else:
            messagebox.showinfo("Info", "No data loaded.")

    def convert_to_json(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_path:
            try:
                self.model.convert_to_json(self.data, save_path)
                messagebox.showinfo("Converted to JSON", "Parquet data converted and saved to JSON successfully.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = ApplicationController()
    app.view.root.mainloop()
