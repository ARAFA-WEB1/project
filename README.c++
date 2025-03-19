#import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re
from cryptography.fernet import Fernet

# Generate a key for encryption (store this securely in a real application)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Database Manager
class DatabaseManager:
    def __init__(self, db_name="airline_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                password TEXT,
                                role TEXT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS flights (
                                flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                flight_number TEXT,
                                airline TEXT,
                                origin TEXT,
                                destination TEXT,
                                departure_time TEXT,
                                arrival_time TEXT,
                                price REAL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_name TEXT,
                                user_age INTEGER,
                                flight_id INTEGER,
                                seat TEXT,
                                payment_status TEXT,
                                card_number TEXT,
                                FOREIGN KEY(flight_id) REFERENCES flights(flight_id))''')
        self.conn.commit()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


# Password Validator
class PasswordValidator:
    @staticmethod
    def validate(password):
        if len(password) >= 12 and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[0-9]", password) and re.search(r"[!@#$%^&*()]", password):
            return "strong"
        elif len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"[0-9]", password):
            return "medium"
        else:
            return "weak"


# Username Validator
class UsernameValidator:
    @staticmethod
    def validate(username):
        pattern = r"^(admin|user)_\d{4}$"
        return bool(re.match(pattern, username))


# Base User Class
class User:
    def __init__(self, username, password, role):
        self.username = username
        self._password = self._hash_password(password)
        self.role = role

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._password == self._hash_password(password)


# Admin Class (Inherits from User)
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="admin")

    def add_flight(self, db, flight):
        query = '''INSERT INTO flights (flight_number, airline, origin, destination, departure_time, arrival_time, price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        db.execute_query(query, flight)

    def edit_flight(self, db, flight_id, flight):
        query = '''UPDATE flights SET flight_number = ?, airline = ?, origin = ?, destination = ?, departure_time = ?, arrival_time = ?, price = ?
                   WHERE flight_id = ?'''
        db.execute_query(query, (*flight, flight_id))

    def delete_flight(self, db, flight_id):
        query = "DELETE FROM flights WHERE flight_id = ?"
        db.execute_query(query, (flight_id,))

    def view_reservations(self, db):
        query = "SELECT * FROM reservations"
        return db.fetch_all(query)


# Passenger Class (Inherits from User)
class Passenger(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="passenger")

    def book_ticket(self, db, reservation):
        query = '''INSERT INTO reservations (user_name, user_age, flight_id, seat, payment_status, card_number)
                   VALUES (?, ?, ?, ?, ?, ?)'''
        db.execute_query(query, reservation)

    def view_flights(self, db, origin, destination):
        query = "SELECT * FROM flights WHERE origin = ? AND destination = ?"
        return db.fetch_all(query, (origin, destination))


# Flight Class
class Flight:
    def __init__(self, flight_number, airline, origin, destination, departure_time, arrival_time, price):
        self.flight_number = flight_number
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price


# Reservation Class
class Reservation:
    def __init__(self, user_name, user_age, flight_id, seat, payment_status, card_number):
        self.user_name = user_name
        self.user_age = user_age
        self.flight_id = flight_id
        self.seat = seat
        self.payment_status = payment_status
        self.card_number = cipher_suite.encrypt(card_number.encode()).decode()  # Encrypt card number


# GUI Application
class AirlineSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Reservation System")
        self.db = DatabaseManager()
        self.current_user = None
        self.show_login_screen()

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
        tk.Label(self.root, text="Username (format: admin_1234 or user_1234):").grid(row=0, column=0)
        self.signup_username_entry = tk.Entry(self.root)
        self.signup_username_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.signup_password_entry = tk.Entry(self.root, show="*")
        self.signup_password_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Sign Up", command=self.sign_up).grid(row=2, column=0)
        tk.Button(self.root, text="Back", command=self.show_login_screen).grid(row=2, column=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_data = self.db.fetch_one("SELECT * FROM users WHERE username = ?", (username,))
        if user_data and User(user_data[1], user_data[2], user_data[3]).verify_password(password):
            self.current_user = Admin(username, password) if user_data[3] == "admin" else Passenger(username, password)
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def sign_up(self):
        username = self.signup_username_entry.get()
        if not UsernameValidator.validate(username):
            messagebox.showerror("Error", "Invalid username format.")
            return

        password = self.signup_password_entry.get()
        strength = PasswordValidator.validate(password)
        messagebox.showinfo("Password Strength", f"Password strength: {strength}")

        role = "admin" if username.startswith("admin") else "passenger"
        user = Admin(username, password) if role == "admin" else Passenger(username, password)

        try:
            self.db.execute_query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                 (user.username, user._password, user.role))
            messagebox.showinfo("Success", "Sign-up successful!")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def show_dashboard(self):
        self.clear_screen()
        if self.current_user.role == "admin":
            self.show_admin_dashboard()
        else:
            self.show_passenger_dashboard()

    def show_admin_dashboard(self):
        tk.Button(self.root, text="Add Flight", command=self.show_add_flight_screen).grid(row=0, column=0)
        tk.Button(self.root, text="View Reservations", command=self.view_reservations).grid(row=0, column=1)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).grid(row=0, column=2)

    def show_passenger_dashboard(self):
        tk.Button(self.root, text="Search Flights", command=self.show_search_flights_screen).grid(row=0, column=0)
        tk.Button(self.root, text="Book Ticket", command=self.show_book_ticket_screen).grid(row=0, column=1)
        tk.Button(self.root, text="Logout", command=self.show_login_screen).grid(row=0, column=2)

    def show_add_flight_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Flight Number:").grid(row=0, column=0)
        self.flight_number_entry = tk.Entry(self.root)
        self.flight_number_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Airline:").grid(row=1, column=0)
        self.airline_entry = tk.Entry(self.root)
        self.airline_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Origin:").grid(row=2, column=0)
        self.origin_entry = tk.Entry(self.root)
        self.origin_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Destination:").grid(row=3, column=0)
        self.destination_entry = tk.Entry(self.root)
        self.destination_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Departure Time (YYYY-MM-DD HH:MM):").grid(row=4, column=0)
        self.departure_time_entry = tk.Entry(self.root)
        self.departure_time_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Arrival Time (YYYY-MM-DD HH:MM):").grid(row=5, column=0)
        self.arrival_time_entry = tk.Entry(self.root)
        self.arrival_time_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Price:").grid(row=6, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=6, column=1)

        tk.Button(self.root, text="Add Flight", command=self.add_flight).grid(row=7, column=0)
        tk.Button(self.root, text="Back", command=self.show_dashboard).grid(row=7, column=1)

    def add_flight(self):
        flight = (
            self.flight_number_entry.get(),
            self.airline_entry.get(),
            self.origin_entry.get(),
            self.destination_entry.get(),
            self.departure_time_entry.get(),
            self.arrival_time_entry.get(),
            float(self.price_entry.get())
        )
        self.current_user.add_flight(self.db, flight)
        messagebox.showinfo("Success", "Flight added successfully!")
        self.show_dashboard()

    def view_reservations(self):
        reservations = self.current_user.view_reservations(self.db)
        self.clear_screen()
        for i, res in enumerate(reservations):
            tk.Label(self.root, text=f"Ticket ID: {res[0]} | Name: {res[1]} | Age: {res[2]} | Flight ID: {res[3]} | Seat: {res[4]} | Payment: {res[5]}").grid(row=i, column=0)
        tk.Button(self.root, text="Back", command=self.show_dashboard).grid(row=len(reservations), column=0)

    def show_search_flights_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Departure City:").grid(row=0, column=0)
        self.origin_search_entry = tk.Entry(self.root)
        self.origin_search_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Destination City:").grid(row=1, column=0)
        self.destination_search_entry = tk.Entry(self.root)
        self.destination_search_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Search", command=self.search_flights).grid(row=2, column=0)
        tk.Button(self.root, text="Back", command=self.show_dashboard).grid(row=2, column=1)

    def search_flights(self):
        origin = self.origin_search_entry.get()
        destination = self.destination_search_entry.get()
        flights = self.current_user.view_flights(self.db, origin, destination)
        self.clear_screen()
        for i, flight in enumerate(flights):
            tk.Label(self.root, text=f"ID: {flight[0]} | {flight[1]} | {flight[2]} | {flight[3]} -> {flight[4]} | {flight[5]} | {flight[6]} | Price: {flight[7]} EGP").grid(row=i, column=0)
        tk.Button(self.root, text="Back", command=self.show_dashboard).grid(row=len(flights), column=0)

    def show_book_ticket_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Flight ID:").grid(row=0, column=0)
        self.flight_id_entry = tk.Entry(self.root)
        self.flight_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Full Name:").grid(row=1, column=0)
        self.user_name_entry = tk.Entry(self.root)
        self.user_name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Age:").grid(row=2, column=0)
        self.user_age_entry = tk.Entry(self.root)
        self.user_age_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Seat:").grid(row=3, column=0)
        self.seat_entry = tk.Entry(self.root)
        self.seat_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Card Number:").grid(row=4, column=0)
        self.card_number_entry = tk.Entry(self.root)
        self.card_number_entry.grid(row=4, column=1)

        tk.Button(self.root, text="Book", command=self.book_ticket).grid(row=5, column=0)
        tk.Button(self.root, text="Back", command=self.show_dashboard).grid(row=5, column=1)

    def book_ticket(self):
        flight_id = int(self.flight_id_entry.get())
        reservation = (
            self.user_name_entry.get(),
            int(self.user_age_entry.get()),
            flight_id,
            self.seat_entry.get(),
            "Paid",
            self.card_number_entry.get()
        )
        self.current_user.book_ticket(self.db, reservation)
        messagebox.showinfo("Success", "Ticket booked successfully!")
        self.show_dashboard()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = AirlineSystemApp(root)
    root.mainloop() project
