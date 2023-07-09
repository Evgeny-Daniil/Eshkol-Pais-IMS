import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class Product:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def find_product_by_id(self, id):
        for product in self.products:
            if product.id == id:
                return product
        return None

    def find_product_by_name(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

    def display_inventory(self):
        return self.products


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eshkol Pais IMS")

        self.inventory = Inventory()
        self.db_connection = sqlite3.connect("inventory.db")
        self.create_table()

        self.create_widgets()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS products (id TEXT, name TEXT, quantity INTEGER)")

    def add_product(self):
        top = tk.Toplevel(self)
        top.title("Add Product")

        id_label = tk.Label(top, text="ID:")
        id_label.grid(row=0, column=0)
        id_entry = tk.Entry(top)
        id_entry.grid(row=0, column=1)

        name_label = tk.Label(top, text="Name:")
        name_label.grid(row=1, column=0)
        name_entry = tk.Entry(top)
        name_entry.grid(row=1, column=1)

        quantity_label = tk.Label(top, text="Quantity:")
        quantity_label.grid(row=2, column=0)
        quantity_entry = tk.Entry(top)
        quantity_entry.grid(row=2, column=1)

        add_button = tk.Button(top, text="Add", command=lambda: self.add_product_to_inventory(top, id_entry.get(), name_entry.get(), quantity_entry.get()))
        add_button.grid(row=3, columnspan=2, pady=5)

    def add_product_to_inventory(self, top, id, name, quantity):
        if id and name and quantity:
            product = Product(id, name, quantity)
            self.inventory.add_product(product)
            self.insert_product_to_database(id, name, quantity)
            messagebox.showinfo("Success", "Product added to inventory.")
            top.destroy()
        else:
            messagebox.showerror("Error", "Please provide all the details.")

    def insert_product_to_database(self, id, name, quantity):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO products VALUES (?, ?, ?)", (id, name, quantity))
        self.db_connection.commit()

    def remove_product(self):
        top = tk.Toplevel(self)
        top.title("Remove Product")

        id_label = tk.Label(top, text="ID:")
        id_label.grid(row=0, column=0)
        id_entry = tk.Entry(top)
        id_entry.grid(row=0, column=1)

        remove_button = tk.Button(top, text="Remove", command=lambda: self.remove_product_from_inventory(top, id_entry.get()))
        remove_button.grid(row=1, columnspan=2, pady=5)

    def remove_product_from_inventory(self, top, id):
        product = self.inventory.find_product_by_id(id)
        if product:
            self.inventory.remove_product(product)
            self.delete_product_from_database(id)
            messagebox.showinfo("Success", "Product removed from inventory.")
            top.destroy()
        else:
            messagebox.showerror("Error", "Product not found in inventory.")

    def delete_product_from_database(self, id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (id,))
        self.db_connection.commit()

    def find_product_by_id(self):
        top = tk.Toplevel(self)
        top.title("Find Product by ID")

        id_label = tk.Label(top, text="ID:")
        id_label.grid(row=0, column=0)
        id_entry = tk.Entry(top)
        id_entry.grid(row=0, column=1)

        find_button = tk.Button(top, text="Find", command=lambda: self.display_product_info(top, self.inventory.find_product_by_id(id_entry.get())))
        find_button.grid(row=1, columnspan=2, pady=5)

    def find_product_by_name(self):
        top = tk.Toplevel(self)
        top.title("Find Product by Name")

        name_label = tk.Label(top, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(top)
        name_entry.grid(row=0, column=1)

        find_button = tk.Button(top, text="Find", command=lambda: self.display_product_info(top, self.inventory.find_product_by_name(name_entry.get())))
        find_button.grid(row=1, columnspan=2, pady=5)

    def display_product_info(self, top, product):
        if product:
            messagebox.showinfo("Product Details", f"ID: {product.id}\nName: {product.name}\nQuantity: {product.quantity}")
        else:
            messagebox.showerror("Error", "Product not found in inventory.")
        top.destroy()

    def display_inventory(self):
        self.treeview.delete(*self.treeview.get_children())
        inventory = self.inventory.display_inventory()
        for product in inventory:
            self.treeview.insert("", "end", values=(product.id, product.name, product.quantity))

    def load_inventory_from_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        for row in rows:
            product = Product(row[0], row[1], row[2])
            self.inventory.add_product(product)

    def create_widgets(self):
        self.label = tk.Label(self, text="Eshkol Pais Inventory Management System")
        self.label.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Product", command=self.add_product)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self, text="Remove Product", command=self.remove_product)
        self.remove_button.pack(pady=5)

        self.find_id_button = tk.Button(self, text="Find Product by ID", command=self.find_product_by_id)
        self.find_id_button.pack(pady=5)

        self.find_name_button = tk.Button(self, text="Find Product by Name", command=self.find_product_by_name)
        self.find_name_button.pack(pady=5)

        self.display_button = tk.Button(self, text="Display Inventory", command=self.display_inventory)
        self.display_button.pack(pady=5)

        self.treeview = ttk.Treeview(self, columns=("ID", "Name", "Quantity"), show="headings")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Quantity", text="Quantity")
        self.treeview.pack(pady=10)

        self.load_inventory_from_database()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
