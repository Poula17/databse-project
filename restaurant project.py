import sqlite3
from tkinter import *
from tkinter import messagebox, ttk


def connect_db():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Restaurant (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            phone_number TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MenuItem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            FOREIGN KEY (menu_id) REFERENCES Menu(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone_number TEXT,
            address TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Order" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES Customer(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OrderItem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES "Order"(id),
            FOREIGN KEY (menu_item_id) REFERENCES MenuItem(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
            payment_method TEXT,
            status TEXT,
            FOREIGN KEY (order_id) REFERENCES "Order"(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Delivery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            delivery_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            delivery_person TEXT,
            FOREIGN KEY (order_id) REFERENCES "Order"(id)
        )
    """)
    conn.commit()
    return conn



def add_record(table_name, fields, entries, tree):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        placeholders = ", ".join("?" for _ in fields)
        query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
        values = [entry.get() for entry in entries]
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", f"Record added to {table_name}!")
        clear_inputs(entries)
        load_data(table_name, fields, tree)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        conn.close()



def load_data(table_name, fields, tree):
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT {', '.join(['id'] + fields)} FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load data: {e}")
    finally:
        conn.close()



def clear_inputs(entries):
    for entry in entries:
        entry.delete(0, END)



def create_tab(tab_name, table_name, fields):
    tab = Frame(tab_control)
    tab_control.add(tab, text=tab_name)

    Label(tab, text=f"Add {tab_name} Record", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    entries = []
    for idx, field in enumerate(fields):
        Label(tab, text=field.capitalize()).grid(row=idx + 1, column=0, padx=10, pady=5)
        entry = Entry(tab)
        entry.grid(row=idx + 1, column=1, padx=10, pady=5)
        entries.append(entry)

    tree = ttk.Treeview(tab, columns=["ID"] + fields, show="headings")
    tree.grid(row=len(fields) + 2, column=0, columnspan=2, padx=10, pady=10)
    for col in ["ID"] + fields:
        tree.heading(col, text=col)

    Button(tab, text="Add Record", command=lambda: add_record(table_name, fields, entries, tree)).grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)


    load_data(table_name, fields, tree)



root = Tk()
root.title("Restaurant Management System")
root.geometry("1200x800")

tab_control = ttk.Notebook(root)


create_tab("Restaurant", "Restaurant", ["name", "address", "phone_number", "email"])
create_tab("Menu", "Menu", ["restaurant_id", "name", "description"])
create_tab("MenuItem", "MenuItem", ["menu_id", "name", "description", "price"])
create_tab("Customer", "Customer", ["name", "email", "phone_number", "address"])
create_tab("Order", "Order", ["customer_id", "order_date", "status", "total_amount"])
create_tab("OrderItem", "OrderItem", ["order_id", "menu_item_id", "quantity", "price"])
create_tab("Payment", "Payment", ["order_id", "amount", "payment_method", "status"])
create_tab("Delivery", "Delivery", ["order_id", "delivery_date", "status", "delivery_person"])

tab_control.pack(expand=1, fill="both")

root.mainloop()
