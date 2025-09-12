#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = BASE_DIR / "data" / "notes"

# Sample flight data
FLIGHTS = [
    {
        "id": "FL001",
        "airline": "SkyWings",
        "source": "New York",
        "destination": "Los Angeles",
        "departure": "2024-01-15 08:00",
        "arrival": "2024-01-15 11:30",
        "price": 299.99,
        "seats_available": 45
    },
    {
        "id": "FL002",
        "airline": "CloudJet",
        "source": "New York",
        "destination": "Los Angeles",
        "departure": "2024-01-15 14:00",
        "arrival": "2024-01-15 17:30",
        "price": 349.99,
        "seats_available": 32
    },
    {
        "id": "FL003",
        "airline": "AirExpress",
        "source": "Chicago",
        "destination": "Miami",
        "departure": "2024-01-16 09:00",
        "arrival": "2024-01-16 13:00",
        "price": 199.99,
        "seats_available": 28
    }
]

# Simple in-memory storage for bookings
bookings = []
booking_counter = 1000


@app.route('/')
def home():
    """Home page with API documentation"""
    return """
    <h1>🛫 Flight Booking Server</h1>
    <h2>Available Endpoints:</h2>
    <ul>
        <li><strong>GET /flights</strong> - List all flights</li>
        <li><strong>GET /flights/search?source=New York&destination=Los Angeles</strong> - Search flights</li>
        <li><strong>POST /flights/book</strong> - Book a flight (JSON: flight_id, passenger_name, passenger_email)</li>
        <li><strong>GET /bookings/{booking_id}</strong> - Check booking status</li>
    </ul>
    <p><strong>Why Server-Client Architecture?</strong></p>
    <ul>
        <li>Server handles all flight data and booking logic</li>
        <li>Client provides user interface</li>
        <li>Multiple clients can connect to same server</li>
        <li>Easy to scale and maintain</li>
    </ul>
    """


@app.route('/flights', methods=['GET'])
def list_flights():
    """List all available flights"""
    return jsonify({
        "status": "success",
        "flights": FLIGHTS,
        "count": len(FLIGHTS)
    })


@app.route('/flights/search', methods=['GET'])
def search_flights():
    """Search for flights between two cities"""
    source = request.args.get('source', '').strip()
    destination = request.args.get('destination', '').strip()

    if not source or not destination:
        return jsonify({
            "status": "error",
            "message": "Please provide both source and destination parameters"
        }), 400

    matching_flights = []
    for flight in FLIGHTS:
        if (flight["source"].lower() == source.lower() and
                flight["destination"].lower() == destination.lower()):
            matching_flights.append(flight)

    if not matching_flights:
        return jsonify({
            "status": "success",
            "message": f"No flights found from {source} to {destination}",
            "flights": []
        })

    return jsonify({
        "status": "success",
        "message": f"Found {len(matching_flights)} flight(s) from {source} to {destination}",
        "flights": matching_flights
    })


@app.route('/flights/book', methods=['POST'])
def book_flight():
    """Book a flight for a passenger"""
    global booking_counter

    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Please provide JSON data"
        }), 400

    flight_id = data.get('flight_id', '').strip()
    passenger_name = data.get('passenger_name', '').strip()
    passenger_email = data.get('passenger_email', '').strip()

    if not all([flight_id, passenger_name, passenger_email]):
        return jsonify({
            "status": "error",
            "message": "Please provide flight_id, passenger_name, and passenger_email"
        }), 400

    # Find the flight
    flight = None
    for f in FLIGHTS:
        if f["id"] == flight_id:
            flight = f
            break

    if not flight:
        return jsonify({
            "status": "error",
            "message": f"Flight {flight_id} not found"
        }), 404

    if flight["seats_available"] <= 0:
        return jsonify({
            "status": "error",
            "message": f"Sorry, no seats available on flight {flight_id}"
        }), 400

    # Create booking
    booking = {
        "booking_id": f"BK{booking_counter}",
        "flight_id": flight_id,
        "passenger_name": passenger_name,
        "passenger_email": passenger_email,
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "confirmed"
    }

    bookings.append(booking)
    flight["seats_available"] -= 1
    booking_counter += 1

    return jsonify({
        "status": "success",
        "message": "Booking confirmed!",
        "booking": booking
    })


@app.route('/bookings/<booking_id>', methods=['GET'])
def get_booking_status(booking_id):
    """Get booking status by booking ID"""
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            flight = next((f for f in FLIGHTS if f["id"] == booking["flight_id"]), None)
            result = {
                "status": "success",
                "booking": booking
            }
            if flight:
                result["flight_details"] = flight
            return jsonify(result)

    return jsonify({
        "status": "error",
        "message": f"Booking {booking_id} not found"
    }), 404


@app.route('/bookings', methods=['GET'])
def list_bookings():
    """List all bookings (for demo purposes)"""
    return jsonify({
        "status": "success",
        "bookings": bookings,
        "count": len(bookings)
    })


if __name__ == '__main__':
    print("Starting Flight Booking Server...")
    print("Server will be available at: http://localhost:50000")
    print("API Documentation: http://localhost:50000")
    print("Server is ready to accept connections!")
    app.run(debug=True, host='0.0.0.0', port=50000)