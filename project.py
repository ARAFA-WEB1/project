from abc import ABC, abstractmethod
from multipledispatch import dispatch
import datetime

# ---------------------- Currency Conversion ----------------------
current_currency = "USD"
currency_rates = {
    "USD": 1.0,
    "EGP": 50.0,
    "KWD": 0.31,
    "SAR": 3.75,
    "JPY": 155.0,
    "EUR": 0.93,
    "GBP": 0.80,
    "AED": 3.67,
    "CNY": 7.23
}

def convert_price(price_usd):
    return round(price_usd * currency_rates[current_currency], 2)

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
            self._users = {}
            self._current_user = None
            self.services = []

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value):
        self._users = value

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, user):
        self._current_user = user

# ---------------------- Proxy Pattern ----------------------
class PaymentProxy:
    def __init__(self, payment_service):
        self.payment_service = payment_service

    def pay(self, card_number=None, expiry=None, cvv=None):
        while True:
            try:
                if card_number is None:
                    card_number = input("Enter card number (16 digits): ")
                if len(card_number) != 16 or not card_number.isdigit():
                    raise PaymentFailedException("Invalid card number. Must be exactly 16 digits.")

                if expiry is None:
                    expiry = input("Enter expiry date (MM/YY): ")
                try:
                    month, year = map(int, expiry.split("/"))
                except ValueError:
                    raise PaymentFailedException("Expiry must be in MM/YY format using numbers.")

                current_year = datetime.datetime.now().year % 100
                if month < 1 or month > 12 or year < current_year:
                    raise PaymentFailedException("Card expired or invalid expiry date.")

                if cvv is None:
                    cvv = input("Enter CVV (3 digits): ")
                if not cvv.isdigit() or len(cvv) != 3:
                    raise PaymentFailedException("CVV must be exactly 3 digits.")

                self.payment_service.process()
                break  # Exit loop on successful payment

            except PaymentFailedException as e:
                print(f"Payment error: {e}")
                card_number, expiry, cvv = None, None, None
                retry = input("Try again? (y/n): ").lower()
                if retry != 'y':
                    raise PaymentFailedException("Payment cancelled by user.")

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
        self._username = username
        self._password = password
        self.bookings = []

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def add_booking(self, booking):
        self.bookings.append(booking)


# ---------------------- Flights ----------------------
class Flight(BookingService):
    def __init__(self):
        self.available_flights = [
            {"from": "Cairo", "to": "Paris", "duration": "4h", "price": 350},
            {"from": "New York", "to": "London", "duration": "7h", "price": 550},
            {"from": "Tokyo", "to": "Los Angeles", "duration": "11h", "price": 750},
            {"from": "Dubai", "to": "Sydney", "duration": "14h", "price": 900},
            {"from": "Paris", "to": "Rome", "duration": "2h", "price": 120},
            {"from": "London", "to": "Berlin", "duration": "1.5h", "price": 110},
            {"from": "Beijing", "to": "Bangkok", "duration": "4h", "price": 300},
            {"from": "Toronto", "to": "Vancouver", "duration": "5h", "price": 320},
            {"from": "New York", "to": "San Francisco", "duration": "6h", "price": 400},
            {"from": "Mumbai", "to": "Dubai", "duration": "3h", "price": 200},
            {"from": "Istanbul", "to": "Athens", "duration": "1.5h", "price": 150},
            {"from": "Madrid", "to": "Lisbon", "duration": "1.2h", "price": 100},
            {"from": "Seoul", "to": "Tokyo", "duration": "2.5h", "price": 250},
            {"from": "Los Angeles", "to": "Honolulu", "duration": "6h", "price": 450},
            {"from": "Chicago", "to": "Miami", "duration": "3h", "price": 280},
            {"from": "Johannesburg", "to": "Cape Town", "duration": "2h", "price": 170},
            {"from": "Singapore", "to": "Bali", "duration": "2.5h", "price": 230},
            {"from": "Amsterdam", "to": "Oslo", "duration": "2h", "price": 140},
            {"from": "Zurich", "to": "Vienna", "duration": "1.5h", "price": 160},
            {"from": "Doha", "to": "Istanbul", "duration": "4.5h", "price": 300},
        ]

    def book(self):
        print("Available Flights:")
        for idx, flight in enumerate(self.available_flights):
            print(f"{idx+1}. {flight['from']} -> {flight['to']} | {flight['duration']} | {convert_price(flight['price'])} {current_currency}")
        choice = int(input("Choose a flight number: ")) - 1
        if choice not in range(len(self.available_flights)):
            raise InvalidInputException("Invalid choice.")

        date = input("Enter your travel date (YYYY-MM-DD): ")

        # Seat selection
        if not hasattr(self, 'available_seats'):
            self.available_seats = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2"]

        if not self.available_seats:
            print("No available seats.")
            return "Booking failed: No seats left."

        print(f"Available seats: {', '.join(self.available_seats)}")
        seat = input("Choose your seat: ")

        if seat not in self.available_seats:
            print("Invalid or already booked seat.")
            return "Booking failed: Seat unavailable."

        self.available_seats.remove(seat)
        print("Booking flight...")
        return f"Flight: {self.available_flights[choice]} on {date} Seat: {seat}"

    def cancel(self, user, booking_detail):
        if booking_detail.startswith("Flight:"):
            print(f"Canceling flight booking: {booking_detail}")
            # Return seat to available seats
            seat = booking_detail.split("Seat: ")[1]
            if seat not in self.available_seats:
                self.available_seats.append(seat)
            return user.cancel_booking(booking_detail)
        return False

# ---------------------- Hotels ----------------------
class Hotel(BookingService):
    def __init__(self):
        self.hotels = [
            {"name": "Hilton Cairo", "price": 120},
            {"name": "Marriott Paris", "price": 200},
            {"name": "Sheraton New York", "price": 250},
            {"name": "Four Seasons Tokyo", "price": 300},
            {"name": "Ritz London", "price": 350},
            {"name": "Grand Hyatt Dubai", "price": 220},
            {"name": "The Oberoi Mumbai", "price": 180},
            {"name": "Peninsula Hong Kong", "price": 330},
            {"name": "Park Hyatt Sydney", "price": 310},
            {"name": "Shangri-La Singapore", "price": 290},
            {"name": "InterContinental Berlin", "price": 210},
            {"name": "Mandarin Oriental Bangkok", "price": 270},
            {"name": "The Langham Melbourne", "price": 240},
            {"name": "Sofitel Rome Villa Borghese", "price": 260},
            {"name": "JW Marriott Seoul", "price": 280},
        ]

    def book(self):
        print("Available Hotels:")
        for idx, hotel in enumerate(self.hotels):
            print(f"{idx + 1}. {hotel['name']} | {convert_price(hotel['price'])} {current_currency} per night")
        choice = int(input("Choose a hotel number: ")) - 1
        if not (0 <= choice < len(self.hotels)):
            raise InvalidInputException("Invalid hotel choice.")
        return self.hotels[choice]

    @dispatch(int)
    def book_choose(self, nights):
        hotel = self.book()
        date = input("Check-in date (YYYY-MM-DD): ")
        return f"Hotel: {hotel['name']} | Single Room | {nights} nights from {date}"

    @dispatch(int, str)
    def book_choose(self, nights, room_type):
        hotel = self.book()
        date = input("Check-in date (YYYY-MM-DD): ")
        if room_type.lower() != "double":
            raise InvalidInputException("Second argument must be 'double' for double room.")
        return f"Hotel: {hotel['name']} | Double Room | {nights} nights from {date}"


    

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
    global current_currency
    print("Available Currencies:")
    for idx, currency in enumerate(currency_rates.keys()):
        print(f"{idx+1}. {currency}")
    choice = int(input("Choose a currency number: ")) - 1
    if choice in range(len(currency_rates)):
        current_currency = list(currency_rates.keys())[choice]
        print(f"Currency selected: {current_currency}")
    else:
        print("Invalid currency choice.")

# ---------------------- Main Program ----------------------
def main():
    system = BookingSystemSingleton.get_instance()
    print("Welcome to AIRLINE Reservation System")

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
        '3': CarRental(),
        '4': Attraction(),
        '5': AirportTaxi()
    }

    booking_services = []  # To store the services each user books
    select_currency()
    while True:
       
        print("\n--- Services ---")
        print("1. Book Flight\n2. Book Hotel\n3. Rent Car\n4. Book Attraction\n5. Book Airport Taxi\n6. View My Bookings\n7. Cancel Booking\n8. Exit")
        choice = input("Choose a service: ")

        if choice in services:
            try:
                # Booking the service and adding the booking to the user's list
                details = services[choice].book()
                card = input("Enter card number (16 digits): ")
                exp = input("Expiry (MM/YY): ")
                cvv = input("CVV: ")
                proxy = PaymentProxy(RealPaymentService())
                proxy.pay(card, exp, cvv)
                system.current_user.add_booking(details)

                # Add the service type to the booking_services list to track what was booked
                booking_services.append((services[choice], details))  # Store service and details

                print("Booking successful!")
            except (InvalidInputException, PaymentFailedException) as e:
                print(f"Error: {e}")

        elif choice == '2':  # Hotel
            hotel_service = Hotel()
            services[choice] = hotel_service  # Store instance for reuse

            try:
                nights = int(input("Enter number of nights: "))
                room_type = input("Room type (single/double): ").strip().lower()

                if room_type == "single":
                    details = hotel_service.book_choose(nights)
                elif room_type == "double":
                    details = hotel_service.book_choose(nights, "double")
                else:
                    raise InvalidInputException("Invalid room type entered.")

                card = input("Enter card number (16 digits): ")
                exp = input("Expiry (MM/YY): ")
                cvv = input("CVV: ")
                proxy = PaymentProxy(RealPaymentService())
                proxy.pay(card, exp, cvv)

                system.current_user.add_booking(details)
                booking_services.append((hotel_service, details))  # Track booking
                print("Hotel booked successfully.")
            except Exception as e:
                print(f"Error: {e}")


        elif choice == '6':
            print("Your Bookings:")
            for idx, (service, booking) in enumerate(booking_services):
                print(f"{idx + 1}. {booking}")

        elif choice == '7':  # Cancel booking
            print("Your current bookings:")
            for idx, (service, booking) in enumerate(booking_services):
                print(f"{idx + 1}. {booking}")

            cancel_choice = int(input("Choose a booking to cancel (number): ")) - 1
            if 0 <= cancel_choice < len(booking_services):
                cancelled_service, cancelled_booking = booking_services.pop(cancel_choice)
                system.current_user.bookings.remove(cancelled_booking)  # Also remove from user bookings
                print(f"Booking cancelled: {cancelled_booking}")

                # Silently return seat if it's a flight
                if isinstance(cancelled_service, Flight):
                    try:
                        seat_part = cancelled_booking.split("Seat: ")[1].strip()
                        cancelled_service.available_seats.append(seat_part)
                    except IndexError:
                        pass  # Booking didn't include a seat — ignore
            else:
                print("Invalid choice.")

        elif choice == '8':
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
