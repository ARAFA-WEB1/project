import customtkinter as ctk
from tkinter import messagebox

# Mock Data and Proxy Logic
from functools import partial

class Hotel:
    def __init__(self, name, location, room_number, price_per_night):
        self.name = name
        self.location = location
        self.room_number = room_number
        self.price_per_night = price_per_night

class HotelProtectionProxy:
    def __init__(self, hotel, user_role):
        self.hotel = hotel
        self.user_role = user_role

    def display_info(self):
        info = f"Name     : {self.hotel.name}\nLocation : {self.hotel.location}\n"
        if self.user_role == "admin":
            info += f"Room Number     : {self.hotel.room_number}\nPrice per Night : ${self.hotel.price_per_night}"
        else:
            info += "Access to full hotel details denied."
        return info

hotels = [
    Hotel("Hilton", "Cairo", 101, 200.0),
    Hotel("Conrad", "Dubai", 202, 300.0),
    Hotel("Lazy Inn", "Alexandria", 303, 100.0)
]

def suggest_destination(preference):
    beach_keywords = ["beach", "relax", "coast", "sea"]
    adventure_keywords = ["hike", "mountain", "explore"]

    if any(word in preference.lower() for word in beach_keywords):
        return ["Alexandria", "Sharm El-Sheikh"]
    elif any(word in preference.lower() for word in adventure_keywords):
        return ["Aswan", "Luxor"]
    else:
        return ["Cairo", "Giza"]

def dynamic_price(base_price, days_before_flight, demand_level):
    if days_before_flight < 3:
        base_price *= 1.5
    if demand_level == "high":
        base_price *= 1.2
    elif demand_level == "low":
        base_price *= 0.9
    return round(base_price, 2)

def chatbot_response(user_input):
    if "book" in user_input.lower():
        return "Sure! Let me help you book a flight. Where to?"
    elif "cancel" in user_input.lower():
        return "Please provide your booking ID to cancel."
    elif "price" in user_input.lower():
        return "Prices vary by destination and date. Do you have a location in mind?"
    else:
        return "I'm here to assist with booking, cancellation, and inquiries."

class TravelApp:
    def __init__(self):
        self.user_role = None
        self.root = ctk.CTk()
        self.root.geometry("600x600")
        self.root.title("Travel Management System")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.login_screen()
        self.root.mainloop()

    def login_screen(self):
        self.clear()
        ctk.CTkLabel(self.root, text="Login", font=("Arial", 24)).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.role_option = ctk.CTkOptionMenu(self.root, values=["user", "admin"])
        self.role_option.set("user")
        self.role_option.pack(pady=10)

        login_btn = ctk.CTkButton(self.root, text="Login", command=self.set_role)
        login_btn.pack(pady=20)

    def set_role(self):
        self.user_role = self.role_option.get()
        self.main_menu()

    def main_menu(self):
        self.clear()
        ctk.CTkLabel(self.root, text=f"Welcome, {self.user_role.capitalize()}", font=("Arial", 20)).pack(pady=20)
        
        ctk.CTkButton(self.root, text="Search Hotels", command=self.search_hotels).pack(pady=10)
        ctk.CTkButton(self.root, text="Chatbot", command=self.chatbot_interface).pack(pady=10)
        ctk.CTkButton(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    def search_hotels(self):
        self.clear()
        ctk.CTkLabel(self.root, text="Hotel Search", font=("Arial", 20)).pack(pady=10)

        self.search_entry = ctk.CTkEntry(self.root, placeholder_text="Enter location")
        self.search_entry.pack(pady=5)

        self.max_price_entry = ctk.CTkEntry(self.root, placeholder_text="Max Price")
        self.max_price_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Search", command=self.filter_hotels).pack(pady=10)
        self.result_frame = ctk.CTkFrame(self.root)
        self.result_frame.pack(fill="both", expand=True)

    def filter_hotels(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        location = self.search_entry.get().lower()
        try:
            max_price = float(self.max_price_entry.get())
        except:
            max_price = float('inf')

        filtered = [h for h in hotels if location in h.location.lower() and h.price_per_night <= max_price]

        if not filtered:
            ctk.CTkLabel(self.result_frame, text="No hotels found.").pack(pady=10)
            return

        for hotel in filtered:
            proxy = HotelProtectionProxy(hotel, self.user_role)
            ctk.CTkLabel(self.result_frame, text=proxy.display_info(), justify="left").pack(pady=5, anchor="w")

    def chatbot_interface(self):
        self.clear()
        ctk.CTkLabel(self.root, text="Travel Assistant Chatbot", font=("Arial", 20)).pack(pady=10)

        self.chat_entry = ctk.CTkEntry(self.root, placeholder_text="Type your message")
        self.chat_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Send", command=self.respond_to_chat).pack(pady=5)
        self.chat_response = ctk.CTkTextbox(self.root, height=200)
        self.chat_response.pack(pady=10, fill="both", expand=True)

    def respond_to_chat(self):
        user_input = self.chat_entry.get()
        response = chatbot_response(user_input)
        if "vacation" in user_input.lower():
            suggestions = suggest_destination(user_input)
            response += f"\nSuggested destinations: {', '.join(suggestions)}"
        self.chat_response.insert("end", f"You: {user_input}\nBot: {response}\n\n")
        self.chat_entry.delete(0, "end")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    TravelApp()
      
