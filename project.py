from abc import ABC, abstractmethod
from multipledispatch import dispatch


class Person(ABC):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    @abstractmethod
    def show_details(self):
        pass


class Pilot:
    def __init__(self, pilot_id, name, license_number, experience_years):
        self.pilot_id = pilot_id
        self.name = name
        self.license_number = license_number
        self.experience_years = experience_years

    def display_info(self):
        print(f"Name       : {self.name}")
        print(f"Experience : {self.experience_years} years")


class Hotel:
    def __init__(self, name, location, room_number, price_per_night):
        self.name = name
        self.location = location
        self.room_number = room_number
        self.price_per_night = price_per_night

    def display_info(self):
        print(f"Name            : {self.name}")
        print(f"Location        : {self.location}")
        print(f"Room Number     : {self.room_number}")
        print(f"Price per Night : ${self.price_per_night}")


class HotelProxy:
    def __init__(self, name, location, room_number, price_per_night):
        self.hotel = Hotel(name, location, room_number, price_per_night)

    def display_info(self):
        self.hotel.display_info()

    def __getattr__(self, name):
        return getattr(self.hotel, name)

    def __setattr__(self, name, value):
        if name != 'hotel':
            setattr(self.hotel, name, value)
        else:
            super().__setattr__(name, value)


class HotelProtectionProxy:
    def __init__(self, hotel, user_role):
        self.hotel = hotel
        self.user_role = user_role

    def display_info(self):
        print(f"Name     : {self.hotel.name}")
        print(f"Location : {self.hotel.location}")
        if self.user_role == "admin":
            print(f"Room Number     : {self.hotel.room_number}")
            print(f"Price per Night : ${self.hotel.price_per_night}")
        else:
            print("Access to full hotel details denied.")


class Traveling:
    def __init__(self, from_location, to_location, price, hour, class_type):
        self.from_location = from_location
        self.to_location = to_location
        self.price = price
        self.hour = hour
        self.class_type = class_type

    def display_info(self):
        print(f"From   : {self.from_location}")
        print(f"To     : {self.to_location}")
        print(f"Price  : ${self.price}")
        print(f"Time   : {self.hour} hour(s)")
        print(f"Class  : {self.class_type}")


class HotelManager:
    instance = None  

    @staticmethod
    def add_instance():
        if HotelManager.instance is None:
            HotelManager.instance = HotelManager()
        return HotelManager.instance  

    def __init__(self):
        self.hotels = []  

    def add_hotel(self, hotel):
        try:
            if not isinstance(hotel, (Hotel, HotelProxy)):  
                raise TypeError("Expected a Hotel or HotelProxy object")
            self.hotels.append(hotel)
        except TypeError as e:
            print(f"Error: {e}")


class Passenger(Person):
    def __init__(self, name, ID, gender, date_of_birth, nationality, number):
        super().__init__(name)
        self.__ID = ID
        self.trip = None
        self.return_trip = None
        self.hotel = None
        self.pilot = None
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.number = number

    def assign_pilot(self, pilot):
        try:
            if not isinstance(pilot, Pilot):  
                raise ValueError("Assigned pilot must be a valid Pilot object")
            self.pilot = pilot
        except ValueError as e:
            print(f"Error: {e}")

    def assign_to_hotel(self, hotel):
        try:
            if not isinstance(hotel, (Hotel, HotelProxy)):  # Allow both Hotel and HotelProxy
                raise ValueError("Assigned hotel must be a valid Hotel object or HotelProxy")
            self.hotel = hotel
        except ValueError as e:
            print(f"Error: {e}")

    @dispatch(object)
    def assign_to_trip(self, trip):
        try:
            if not isinstance(trip, Traveling):  
                raise ValueError("Assigned trip must be a valid Traveling object")
            self.trip = trip
        except ValueError as e:
            print(f"Error: {e}")

    @dispatch(object, object)
    def assign_to_trip(self, trip, return_trip):
        try:
            if not isinstance(trip, Traveling) or not isinstance(return_trip, Traveling):  
                raise ValueError("Assigned trips must be valid Traveling objects")
            self.trip = trip
            self.return_trip = return_trip
        except ValueError as e:
            print(f"Error: {e}")

    def get_ID(self):
        return self.__ID

    def set_ID(self, ID):
        self.__ID = ID

    def show_details(self):
        try:
            print("\n===== Passenger Details =====")
            print(f"Name        : {self.get_name()}")
            print(f"ID          : {self.get_ID()}")
            print(f"Gender      : {self.gender}")
            print(f"DOB         : {self.date_of_birth}")
            print(f"Phone       : {self.number}")
            print(f"Nationality : {self.nationality}")

            if self.trip and not self.return_trip:
                print("\n>> Trip (One Way):")
                self.trip.display_info()
            elif self.trip and self.return_trip:
                print("\n>> Trip (Forward):")
                self.trip.display_info()
                print("\n>> Trip (Return):")
                self.return_trip.display_info()
            else:
                print("\n>> No trip assigned.")

            if self.pilot:
                print("\n>> Pilot Information:")
                print(f"Name       : {self.pilot.name}")
                print(f"Experience : {self.pilot.experience_years} years")
            else:
                print("\n>> No pilot assigned.")

            if self.hotel:
                print("\n>> Hotel Information:")
                self.hotel.display_info()
            else:
                print("\n>> No hotel assigned.")
            print("=============================\n")
        except Exception as e:
            print(f"Error showing details: {e}")


passenger1 = Passenger("Ali Hassan", "EG123", "Male", "1990-05-10", "Egyptian", "+20123456789")
pilot1 = Pilot("P001", "Captain Youssef", "LIC98765", 15)
trip1 = Traveling("Cairo", "Dubai", 350.0, 3, "Business")
trip2 = Traveling("Dubai", "Cairo", 330.0, 3, "Business")
hotel_proxy = HotelProxy("Lazy Inn", "Alexandria", 303, 100.0)

passenger1.assign_pilot(pilot1)
passenger1.assign_to_trip(trip1, trip2)
passenger1.assign_to_hotel(hotel_proxy)

manager = HotelManager()
h1 = Hotel("Hilton", "Cairo", 101, 200.0)
h2 = Hotel("Conrad", "Dubai", 202, 300.0)
manager.add_hotel(h1)
manager.add_hotel(h2)

passenger1.show_details()
