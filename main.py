import tkinter as tk
from tkinter import messagebox, ttk, font as tkfont
import sqlite3

def create_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_item(item_name, quantity, price, supplier, tree):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT INTO inventory (item_name, quantity, price, supplier) VALUES (?, ?, ?, ?)', 
              (item_name, quantity, price, supplier))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Item added to inventory")
    refresh_inventory(tree)

def get_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    return items

def refresh_inventory(tree):
    for row in tree.get_children():
        tree.delete(row)
    for item in get_inventory():
        tree.insert('', 'end', values=item)

def inventory_management_system():
    app = tk.Tk()
    app.title("Inventory Management System")
    style = ttk.Style(app)
    style.theme_use('clam')  # Using a theme for better button and frame visuals

    # Define colors and styles
    style.configure('TFrame', background='#333333')
    style.configure('TLabel', background='#333333', foreground='#FFFFFF')
    style.configure('TEntry', background='#FFFFFF', foreground='#000000')
    style.configure('TButton', background='#005f73', foreground='#FFFFFF', font=('Helvetica', 12, 'bold'))
    style.map('TButton', background=[('active', '#0a9396')])

    app_font = tkfont.Font(family="Helvetica", size=12)

    # Layout Frames
    input_frame = ttk.Frame(app)
    input_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
    list_frame = ttk.Frame(app)
    list_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Input fields
    ttk.Label(input_frame, text="Item Name:", font=app_font).grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(input_frame, text="Quantity:", font=app_font).grid(row=1, column=0, padx=5, pady=5)
    ttk.Label(input_frame, text="Price:", font=app_font).grid(row=2, column=0, padx=5, pady=5)
    ttk.Label(input_frame, text="Supplier:", font=app_font).grid(row=3, column=0, padx=5, pady=5)

    item_name = ttk.Entry(input_frame, font=app_font)
    quantity = ttk.Entry(input_frame, font=app_font)
    price = ttk.Entry(input_frame, font=app_font)
    supplier = ttk.Entry(input_frame, font=app_font)

    item_name.grid(row=0, column=1, padx=5, pady=5)
    quantity.grid(row=1, column=1, padx=5, pady=5)
    price.grid(row=2, column=1, padx=5, pady=5)
    supplier.grid(row=3, column=1, padx=5, pady=5)

    # Buttons
    add_button = ttk.Button(input_frame, text="Add Item", command=lambda: insert_item(item_name.get(), quantity.get(), price.get(), supplier.get(), tree))
    add_button.grid(row=4, column=1, sticky=tk.W+tk.E, padx=5, pady=5)

    # Inventory List
    columns = ('id', 'item_name', 'quantity', 'price', 'supplier')
    tree = ttk.Treeview(list_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.title())
    tree.grid(row=0, column=0, sticky=tk.NSEW)

    refresh_inventory(tree)

    # Signature
    signature = ttk.Label(app, text="Powered by Mohammad Jowkari", font=("Helvetica", 10, "italic"), background='#333333', foreground='#ffffff')
    signature.grid(row=2, column=0, sticky=tk.S, pady=10)

    app.mainloop()

create_db()
inventory_management_system()
