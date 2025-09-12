#!/usr/bin/env python3
import requests
import json
import sys


class FlightBookingClient:
    def __init__(self, server_url="http://localhost:50000"):  # Changed to port 50000
        self.server_url = server_url

    def search_flights(self, source: str, destination: str):
        """Search for flights"""
        try:
            response = requests.get(f"{self.server_url}/flights/search",
                                    params={"source": source, "destination": destination})
            data = response.json()

            print(f"\nSearching flights from {source} to {destination}...")
            if data["status"] == "success":
                if data["flights"]:
                    print(f"Found {len(data['flights'])} flight(s):\n")
                    for flight in data["flights"]:
                        print(f"Flight {flight['id']} - {flight['airline']}")
                        print(f"Departure: {flight['departure']}")
                        print(f"Arrival: {flight['arrival']}")
                        print(f"Price: ${flight['price']}")
                        print(f"Seats Available: {flight['seats_available']}\n")
                else:
                    print(data["message"])
            else:
                print(f"Error: {data['message']}")
        except Exception as e:
            print(f"Error searching flights: {e}")

    def book_flight(self, flight_id: str, passenger_name: str, passenger_email: str):
        """Book a flight"""
        try:
            data = {
                "flight_id": flight_id,
                "passenger_name": passenger_name,
                "passenger_email": passenger_email
            }
            response = requests.post(f"{self.server_url}/flights/book", json=data)
            result = response.json()

            print(f"\nBooking flight {flight_id}...")
            if result["status"] == "success":
                booking = result["booking"]
                print(f"{result['message']}")
                print(f"Booking ID: {booking['booking_id']}")
                print(f"Passenger: {booking['passenger_name']}")
                print(f"Status: {booking['status']}")
            else:
                print(f"Error: {result['message']}")
        except Exception as e:
            print(f"Error booking flight: {e}")

    def check_booking(self, booking_id: str):
        """Check booking status"""
        try:
            response = requests.get(f"{self.server_url}/bookings/{booking_id}")
            result = response.json()

            print(f"\nChecking booking {booking_id}...")
            if result["status"] == "success":
                booking = result["booking"]
                print("Booking Details:")
                print(f"Booking ID: {booking['booking_id']}")
                print(f"Passenger: {booking['passenger_name']}")
                print(f"Email: {booking['passenger_email']}")
                print(f"Flight: {booking['flight_id']}")
                print(f"Status: {booking['status']}")
                print(f"Booking Date: {booking['booking_date']}")

                if "flight_details" in result:
                    flight = result["flight_details"]
                    print(f"Departure: {flight['departure']}")
                    print(f"Arrival: {flight['arrival']}")
            else:
                print(f"Error: {result['message']}")
        except Exception as e:
            print(f"Error checking booking: {e}")

    def list_flights(self):
        """List all available flights"""
        try:
            response = requests.get(f"{self.server_url}/flights")
            result = response.json()

            print("\nAll Available Flights:")
            if result["status"] == "success":
                for flight in result["flights"]:
                    print(f"Flight {flight['id']} - {flight['airline']}")
                    print(f"Route: {flight['source']} → {flight['destination']}")
                    print(f"Departure: {flight['departure']}")
                    print(f"Arrival: {flight['arrival']}")
                    print(f"Price: ${flight['price']}")
                    print(f"Seats Available: {flight['seats_available']}\n")
        except Exception as e:
            print(f"Error listing flights: {e}")

    def run_demo(self):
        """Run automated demonstration"""
        print("\nSTUDENT PROJECT: Flight Booking System")
        print("Demonstrating Server-Client Architecture")
        print("\n" + "=" * 60)

        print("\nDEMO 1: Searching for flights from New York to Los Angeles")
        self.search_flights("New York", "Los Angeles")

        print("\nDEMO 2: Booking a flight")
        self.book_flight("FL001", "John Student", "john@student.edu")

        print("\nDEMO 3: Checking booking status")
        self.check_booking("BK1000")

        print("\nDEMO 4: Listing all available flights")
        self.list_flights()

        print("\nDemo completed successfully!")
        print("\nWhy Server-Client Architecture?")
        print("   • Server handles all flight data and booking logic")
        print("   • Client provides user interface")
        print("   • Multiple clients can connect to same server")
        print("   • Easy to scale and maintain")

    def interactive_menu(self):
        """Interactive menu for the client"""
        print("\n" + "=" * 50)
        print("�� WELCOME TO FLIGHT BOOKING SYSTEM 🛫")
        print("=" * 50)

        while True:
            print("\n*****MENU:*****")
            print("1. Search Flights")
            print("2. Book a Flight")
            print("3. Check Booking Status")
            print("4. List All Flights")
            print("5. Exit")

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                source = input("Enter source city: ").strip()
                destination = input("Enter destination city: ").strip()
                self.search_flights(source, destination)

            elif choice == "2":
                flight_id = input("Enter flight ID (e.g., FL001): ").strip()
                passenger_name = input("Enter passenger name: ").strip()
                passenger_email = input("Enter passenger email: ").strip()
                self.book_flight(flight_id, passenger_name, passenger_email)

            elif choice == "3":
                booking_id = input("Enter booking ID (e.g., BK1000): ").strip()
                self.check_booking(booking_id)

            elif choice == "4":
                self.list_flights()

            elif choice == "5":
                print("\nThank you for using Flight Booking System!")
                break

            else:
                print("Invalid choice. Please try again.")


def main():
    """Main function - checks command line arguments"""
    client = FlightBookingClient()

    try:
        # Check if user wants demo mode
        if len(sys.argv) > 1 and sys.argv[1] == "--demo":
            client.run_demo()
        else:
            client.interactive_menu()

    except KeyboardInterrupt:
        print("\n Goodbye!")
    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    main()