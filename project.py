import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


class DatabaseManager:
    def __init__(self, db_name="airline_reservation.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_number TEXT,
                origin TEXT,
                destination TEXT,
                departure_time TEXT,
                price REAL
            )
        ''')
        self.conn.commit()

    def insert_default_admin(self):
        admin_password = hashlib.sha256("123".encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("mohamed",))
        if not self.cursor.fetchone():
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("mohamed", admin_password, "admin")
            )
            self.conn.commit()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


class AirlineSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Reservation System")
        self.db = DatabaseManager()
        self.db.insert_default_admin()
        self.current_user = None
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0)
        tk.Button(self.root, text="Sign Up", command=self.show_signup_screen).grid(row=2, column=1)

    def show_signup_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.signup_username_entry = tk.Entry(self.root)
        self.signup_username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.signup_password_entry = tk.Entry(self.root, show="*")
        self.signup_password_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Role (admin/passenger):").grid(row=2, column=0)
        self.role_entry = tk.Entry(self.root)
        self.role_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Sign Up", command=self.sign_up).grid(row=3, column=0)
        tk.Button(self.root, text="Back", command=self.show_login_screen).grid(row=3, column=1)

    def sign_up(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        role = self.role_entry.get().lower()

        if role not in ["admin", "passenger"]:
            messagebox.showerror("Error", "Invalid role. Choose 'admin' or 'passenger'.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.db.execute_query(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password, role)
            )
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user_data = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password)
        )

        if user_data:
            self.current_user = {"username": user_data[1], "role": user_data[3]}
            if self.current_user["role"] == "admin":
                self.show_admin_dashboard()
            else:
                self.show_passenger_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, Admin {self.current_user['username']}!").grid(row=0, column=0)

        tk.Button(self.root, text="Add Flight", command=self.show_add_flight_screen).grid(row=1, column=0)
        tk.Button(self.root, text="Manage Users", command=self.show_manage_users_screen).grid(row=2, column=0)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).grid(row=3, column=0)

    def show_manage_users_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Manage Users").grid(row=0, column=0, columnspan=2)

        users = self.db.fetch_all("SELECT id, username, role FROM users WHERE role != 'admin'")
        if users:
            for idx, user in enumerate(users):
                tk.Label(self.root, text=f"Username: {user[1]}, Role: {user[2]}").grid(row=idx+1, column=0)
                tk.Button(self.root, text="Delete", command=lambda u_id=user[0]: self.delete_user(u_id)).grid(row=idx+1, column=1)
        else:
            tk.Label(self.root, text="No users found.").grid(row=1, column=0)

        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).grid(row=len(users)+2, column=0)

    def delete_user(self, user_id):
        self.db.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
        messagebox.showinfo("Success", "User deleted successfully!")
        self.show_manage_users_screen()

    def show_add_flight_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Flight Number:").grid(row=0, column=0)
        self.flight_number_entry = tk.Entry(self.root)
        self.flight_number_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Origin:").grid(row=1, column=0)
        self.origin_entry = tk.Entry(self.root)
        self.origin_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Destination:").grid(row=2, column=0)
        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Departure Time:").grid(row=3, column=0)
        self.departure_time_entry = tk.Entry(self.root)
        self.departure_time_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Price:").grid(row=4, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Add Flight", command=self.add_flight).grid(row=5, column=0)
        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).grid(row=5, column=1)

    def add_flight(self):
        flight = (
            self.flight_number_entry.get(),
            self.origin_entry.get(),
            self.destination_entry.get(),
            self.departure_time_entry.get(),
            float(self.price_entry.get())
        )
        self.db.execute_query(
            "INSERT INTO flights (flight_number, origin, destination, departure_time, price) VALUES (?, ?, ?, ?, ?)",
            flight
        )
        messagebox.showinfo("Success", "Flight added successfully!")
        self.show_admin_dashboard()

    def show_passenger_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_user['username']}!").grid(row=0, column=0)
        tk.Button(self.root, text="Search Flights", command=self.show_search_flights_screen).grid(row=1, column=0)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).grid(row=2, column=0)

    def show_search_flights_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Search for Flights").grid(row=0, column=0, columnspan=2)

        tk.Label(self.root, text="Origin:").grid(row=1, column=0)
        self.search_origin_entry = tk.Entry(self.root)
        self.search_origin_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Destination:").grid(row=2, column=0)
        self.search_destination_entry = tk.Entry(self.root)
        self.search_destination_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Search", command=self.search_flights).grid(row=3, column=0)
        tk.Button(self.root, text="Back", command=self.show_passenger_dashboard).grid(row=3, column=1)

    def search_flights(self):
        origin = self.search_origin_entry.get()
        destination = self.search_destination_entry.get()

        flights = self.db.fetch_all(
            "SELECT * FROM flights WHERE origin = ? AND destination = ?", (origin, destination)
        )

        self.clear_screen()

        if flights:
            tk.Label(self.root, text="Available Flights:").grid(row=0, column=0, columnspan=2)
            for idx, flight in enumerate(flights):
                tk.Label(
                    self.root,
                    text=f"Flight: {flight[1]}, Origin: {flight[2]}, Destination: {flight[3]}, Departure: {flight[4]}, Price: {flight[5]}"
                ).grid(row=idx+1, column=0, columnspan=2)
        else:
            tk.Label(self.root, text="No flights found.").grid(row=0, column=0)

        tk.Button(self.root, text="Back", command=self.show_search_flights_screen).grid(row=len(flights)+2, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineSystemApp(root)
    root.mainloop()
