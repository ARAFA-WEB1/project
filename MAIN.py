from abc import ABC, abstractmethod
from multipledispatch import dispatch

class Person(ABC):
    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def set_name(self, name):
        pass

    @abstractmethod
    def show_details(self):
        pass

class Payment:
    def __init__(self):
        self.amount = 0
        self.method = ""
        self.details = ""

    @dispatch(float)
    def pay(self, amount):
        self.amount = amount
        self.method = "Cash"
        self.details = "Paid in cash"
       

    @dispatch(float, str)
    def pay(self, amount, card_number):
        self.amount = amount
        self.method = "Credit Card"
        self.details = f"Card ending with {card_number[-4:]}"
        

    @dispatch(float, str, str)
    def pay(self, amount, wallet_type, phone_number):
        self.amount = amount
        self.method = wallet_type
        self.details = f"Wallet Phone: {phone_number}"
        

    def show_payment_info(self):
        print(f"Payment Method: {self.method}")
        print(f"Amount Paid: ${self.amount}")
        print(f"Details: {self.details}")


class Passenger(Person):
    def __init__(self, name, ID, gender, date_of_birth, nationality, number):
        super().__init__(name)
        self.__ID = ID
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.number = number 
        self.trip = None
        self.hotel = None
        self.pilot = None
        self.payment = Payment()

    def get_name(self):
        return self._Person__name

    def set_name(self, name):
        self._Person__name = name

    def get_ID(self):
        return self.__ID

    def set_ID(self, ID):
        self.__ID = ID

    def show_details(self):
        print(f"\nPassenger Name: {self.get_name()} , ID: {self.get_ID()} , Gender: {self.gender} , DOB: {self.date_of_birth} , Phone: {self.number} , Nationality: {self.nationality}")
        
        if self.pilot:
            print(f"Pilot: {self.pilot.name}")
        else:
            print("No pilot assigned.")

        if self.trip:
            print("\nTrip Info:")
            self.trip.display_info()
        else:
            print("\nNo trip assigned.")

        if self.hotel:
            print("\nHotel Info:")
            self.hotel.display_info()
        else:
            print("\nNo hotel assigned.")

        print("\nPayment Info:")
        self.payment.show_payment_info()

    def assign_to_trip(self, trip):
        self.trip = trip

    def assign_to_hotel(self, hotel):
        self.hotel = hotel

    def assign_pilot(self, pilot):
        self.pilot = pilot

    def make_payment_cash(self, amount):
        self.payment.pay(float(amount))

    def make_payment_card(self, amount, card):
        self.payment.pay(float(amount), card)

    def make_payment_wallet(self, amount, wallet, phone):
        self.payment.pay(float(amount), wallet, phone)

class Pilot:
    def __init__(self, pilot_id, name, license_number, experience_years):
        self.pilot_id = pilot_id
        self.name = name
        self.license_number = license_number
        self.experience_years = experience_years

    def display_info(self):
        print("\nPilot Information:")
        print(f"ID: {self.pilot_id}")
        print(f"Name: {self.name}")
        print(f"License Number: {self.license_number}")
        print(f"Years of Experience: {self.experience_years}")

class Hotel:
    def __init__(self, name, location, room_number, price_per_night):
        self.name = name
        self.location = location
        self.room_number = room_number
        self.price_per_night = price_per_night

    def display_info(self):
        print(f"Hotel Name: {self.name}")
        print(f"Location: {self.location}")
        print(f"Room Number: {self.room_number}")
        print(f"Price per Night: ${self.price_per_night}")

class Traveling:
    def __init__(self, from_location, to_location, price, hour, class_type):
        self.from_location = from_location
        self.to_location = to_location
        self.price = price
        self.hour = hour
        self.class_type = class_type

    def display_info(self):
        print(f"From: {self.from_location}")
        print(f"To: {self.to_location}")
        print(f"Price: ${self.price}")
        print(f"Time: {self.hour} hour(s)")
        print(f"Class: {self.class_type}")

trip1 = Traveling("Cairo", "Paris", 500, 4, "Business")
pilot1 = Pilot("P001", "Captain Youssef", "LIC98765", 15)
hotel1 = Hotel("Grand Paris", "Downtown", 204, 120)

passenger1 = Passenger("Ali", "EG123", "Male", "1990-01-01", "Egyptian", "0123456789")

passenger1.assign_to_trip(trip1)
passenger1.assign_to_hotel(hotel1)
passenger1.assign_pilot(pilot1)

#passenger1.make_payment_cash(200)        
#passenger1.make_payment_card(300, "1234567812345678")  
passenger1.make_payment_wallet(500 , "Vodafone Cash", "01098765432")  

passenger1.show_details()
 