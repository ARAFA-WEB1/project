from abc import ABC, abstractmethod
from multipledispatch import dispatch
import datetime

# ---------------------- Exception Classes ----------------------
class BookingException(Exception):
    pass

class InvalidInputException(BookingException):
    pass

class PaymentFailedException(BookingException):
    pass

# ---------------------- Singleton Pattern ----------------------
class BookingSystemSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if BookingSystemSingleton._instance is None:
            BookingSystemSingleton()
        return BookingSystemSingleton._instance

    def __init__(self):
        if BookingSystemSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BookingSystemSingleton._instance = self
            self.users = {}
            self.current_user = None
            self.services = []

# ---------------------- Proxy Pattern ----------------------
class PaymentProxy:
    def __init__(self, payment_service):
        self.payment_service = payment_service

    def pay(self, card_number, expiry, cvv):
        # Basic validation before real payment
        if len(card_number) != 16 or not card_number.isdigit():
            raise PaymentFailedException("Invalid card number.")
        if int(expiry.split("/")[0]) > 12 or int(expiry.split("/")[1]) < datetime.datetime.now().year % 100:
            raise PaymentFailedException("Card expired.")
        if len(cvv) != 3:
            raise PaymentFailedException("Invalid CVV.")
        self.payment_service.process()

class RealPaymentService:
    def process(self):
        print("Payment processed successfully.")

# ---------------------- Abstract Booking Service ----------------------
class BookingService(ABC):
    @abstractmethod
    def book(self):
        pass

# ---------------------- User System ----------------------
class User:
    def __init__(self, username, password):
        if len(username) < 3 or len(password) < 6:
            raise InvalidInputException("Username or password too short.")
        self.username = username
        self.password = password
        self.bookings = []

    def add_booking(self, booking):
        self.bookings.append(booking)

# ---------------------- Flights ----------------------
class Flight(BookingService):
    def __init__(self):
        self.available_flights = [
            {"from": "Cairo", "to": "Paris", "duration": "4h", "price": 350},
            {"from": "New York", "to": "London", "duration": "7h", "price": 550},
        ]

    def book(self):
        print("Available Flights:")
        for idx, flight in enumerate(self.available_flights):
            print(f"{idx+1}. {flight['from']} -> {flight['to']} | {flight['duration']} | ${flight['price']}")
        choice = int(input("Choose a flight number: ")) - 1
        if choice not in range(len(self.available_flights)):
            raise InvalidInputException("Invalid choice.")
        date = input("Enter your travel date (YYYY-MM-DD): ")
        # Seat selection simulation
        print("Available seats: A1, A2, B1, B2")
        seat = input("Choose your seat: ")
        print("Booking flight...")
        return f"Flight: {self.available_flights[choice]} on {date} Seat: {seat}"

# ---------------------- Hotels ----------------------
class Hotel(BookingService):
    def __init__(self):
        self.hotels = [
            {"name": "Hilton Cairo", "price": 120},
            {"name": "Marriott Paris", "price": 200},
        ]

    def book(self):
        print("Available Hotels:")
        for idx, hotel in enumerate(self.hotels):
            print(f"{idx+1}. {hotel['name']} | ${hotel['price']} per night")
        choice = int(input("Choose a hotel number: ")) - 1
        nights = int(input("Enter number of nights: "))
        date = input("Check-in date (YYYY-MM-DD): ")
        return f"Hotel: {self.hotels[choice]['name']} for {nights} nights from {date}"

# ---------------------- Car Rentals ----------------------
class CarRental(BookingService):
    def book(self):
        print("Available Cars: 1. Toyota Corolla, 2. BMW 3 Series")
        car = input("Choose your car (1 or 2): ")
        duration = input("Rental duration (days): ")
        return f"Car Rental: {car}, for {duration} days"

# ---------------------- Attractions ----------------------
class Attraction(BookingService):
    def book(self):
        attractions = ["Eiffel Tower Tour", "Pyramids Tour", "London Eye"]
        for idx, attr in enumerate(attractions):
            print(f"{idx+1}. {attr}")
        choice = int(input("Choose an attraction: ")) - 1
        date = input("Date for attraction: ")
        return f"Attraction: {attractions[choice]} on {date}"

# ---------------------- Airport Taxi ----------------------
class AirportTaxi(BookingService):
    def book(self):
        pickup = input("Enter pickup location: ")
        time = input("Enter pickup time (HH:MM): ")
        return f"Taxi booked from {pickup} at {time}"

# ---------------------- Currency Selector ----------------------
def select_currency():
    currencies = ["USD", "EUR", "EGP"]
    print("Available currencies:")
    for i, c in enumerate(currencies):
        print(f"{i+1}. {c}")
    choice = int(input("Select currency: "))
    print(f"Currency set to {currencies[choice-1]}")

# ---------------------- Main Program ----------------------
def main():
    system = BookingSystemSingleton.get_instance()
    print("Welcome to Booking.com Clone")
    while True:
        action = input("1. Sign Up  2. Login  3. Exit: ")
        if action == '1':
            username = input("Username: ")
            password = input("Password: ")
            try:
                user = User(username, password)
                system.users[username] = user
                print("Sign up successful.")
            except InvalidInputException as e:
                print(e)
        elif action == '2':
            username = input("Username: ")
            password = input("Password: ")
            user = system.users.get(username)
            if user and user.password == password:
                system.current_user = user
                print("Login successful.")
                break
            else:
                print("Invalid credentials.")
        elif action == '3':
            return

    # Authenticated menu
    services = {
        '1': Flight(),
        '2': Hotel(),
        '3': CarRental(),
        '4': Attraction(),
        '5': AirportTaxi()
    }

    while True:
        print("\n--- Services ---")
        print("1. Book Flight\n2. Book Hotel\n3. Rent Car\n4. Book Attraction\n5. Book Airport Taxi\n6. Select Currency\n7. View My Bookings\n8. Exit")
        choice = input("Choose a service: ")
        if choice in services:
            try:
                details = services[choice].book()
                card = input("Enter card number (16 digits): ")
                exp = input("Expiry (MM/YY): ")
                cvv = input("CVV: ")
                proxy = PaymentProxy(RealPaymentService())
                proxy.pay(card, exp, cvv)
                system.current_user.add_booking(details)
                print("Booking successful!")
            except (InvalidInputException, PaymentFailedException) as e:
                print(f"Error: {e}")
        elif choice == '6':
            select_currency()
        elif choice == '7':
            print("Your Bookings:")
            for b in system.current_user.bookings:
                print(f"- {b}")
        elif choice == '8':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
