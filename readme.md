# Flight Booking System

A simple flight booking system built using MCP (Model Context Protocol) Server-Client architecture.

## Project Overview

This is a project that demonstrates how to build a distributed system using MCP protocol. The system allows users to search for flights, book tickets, and check booking status.

## Architecture

### Why MCP Server-Client Architecture?

1. **Separation of Concerns**: Server handles flight data and booking logic, client handles user interface
2. **Scalability**: Multiple clients can connect to one server (like multiple booking websites using same flight data)
3. **Security**: Sensitive booking data stays on the server, clients only get what they need
4. **Real-time Updates**: When one client books a flight, the server updates availability for all clients
5. **Modularity**: Easy to add new features without changing client code

### System Components

- **Server** (`server/server.py`): Handles flight data, booking logic, and provides MCP resources
- **Client** (`client/flight_client.py`): User interface that connects to the server
- **Demo** (`demo.py`): Shows how the system works

##  How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Option 1: Interactive Mode
```bash
python client/flight_client.py
```

### Option 2: Demo Mode
```bash
python demo.py
```

## Available Operations

1. **Search Flights**: Find flights between two cities
2. **Book Flight**: Reserve a seat on a flight
3. **Check Booking**: View booking details and status
4. **List Flights**: See all available flights


