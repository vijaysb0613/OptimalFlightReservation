from sortedcontainers import SortedDict
import heapq

# Define Airport and Flight classes
class Airport:
    def __init__(self, name):
        self.name = name
        self.flights = []

class Flight:
    def __init__(self, flight_number, destination, cost, duration):
        self.flight_number = flight_number

        self.destination = destination
        self.cost = cost
        self.duration = duration

class FlightOption:
    def __init__(self, flight_number, cost, duration):
        self.flight_number = flight_number
        self.cost = cost
        self.duration = duration
    
    def __lt__(self, other):
        if self.cost == other.cost:
            return self.duration < other.duration
        return self.cost < other.cost

# Seat management with Red-Black Tree (using SortedDict)
class FlightSeatManagement:
    def __init__(self, total_seats):
        self.seat_map = SortedDict()
        for i in range(1, total_seats + 1):
            self.seat_map[i] = False  # False means seat is not booked

    def book_seat(self, seat_number):
        if seat_number in self.seat_map and not self.seat_map[seat_number]:
            self.seat_map[seat_number] = True
            print(f"Seat {seat_number} booked successfully.")
            return True
        print(f"Seat {seat_number} is already booked or unavailable.")
        return False

    def show_available_seats(self):
        for seat_number, booked in self.seat_map.items():
            if not booked:
                print(f"Seat {seat_number} is available.")

# Main Flight Registration System
class FlightRegistrationSystem:
    def __init__(self):
        self.airports = {}
        self.seat_management = {}

    def add_airport(self, name):
        if name not in self.airports:
            self.airports[name] = Airport(name)

    def add_flight(self, from_airport, to_airport, flight_number, cost, duration, total_seats):
        if from_airport not in self.airports or to_airport not in self.airports:
            raise ValueError("One or both airports not found")
        
        source = self.airports[from_airport]
        destination = self.airports[to_airport]
        flight = Flight(flight_number, destination, cost, duration)
        source.flights.append(flight)
        
        # Initialize seat management for this flight
        self.seat_management[flight_number] = FlightSeatManagement(total_seats)

    def find_optimal_flights(self, from_airport, to_airport):
        if from_airport not in self.airports or to_airport not in self.airports:
            raise ValueError("One or both airports not found")

        # Dijkstra's algorithm
        distances = {airport: float('inf') for airport in self.airports.values()}
        previous_flights = {}
        distances[self.airports[from_airport]] = 0
        priority_queue = [(0, 0, "", self.airports[from_airport])]

        while priority_queue:
            current_cost, current_duration, flight_number, current_airport = heapq.heappop(priority_queue)

            for flight in current_airport.flights:
                new_cost = current_cost + flight.cost
                new_duration = current_duration + flight.duration

                if new_cost < distances[flight.destination]:
                    distances[flight.destination] = new_cost
                    previous_flights[flight.destination] = flight
                    heapq.heappush(priority_queue, (new_cost, new_duration, flight.flight_number, flight.destination))

        # Backtrack to get the optimal path
        optimal_flights = []
        destination = self.airports[to_airport]
        while destination in previous_flights:
            flight = previous_flights[destination]
            optimal_flights.append(FlightOption(flight.flight_number, flight.cost, flight.duration))
            destination = self.airports.get(flight.destination.name)

        return optimal_flights[::-1]  # Reverse to get the correct order

    def book_seat(self, flight_number, seat_number):
        if flight_number not in self.seat_management:
            print("Flight does not exist.")
            return False
        
        return self.seat_management[flight_number].book_seat(seat_number)

    def show_available_seats(self, flight_number):
        if flight_number not in self.seat_management:
            print("Flight does not exist.")
            return
        self.seat_management[flight_number].show_available_seats()

# Usage Example
if __name__ == "__main__":
    system = FlightRegistrationSystem()
    
    # Add airports
    system.add_airport("JFK")
    system.add_airport("LAX")
    system.add_airport("ORD")
    
    # Add flights
    system.add_flight("JFK", "LAX", "FL123", 300.50, 360, 200)
    system.add_flight("JFK", "ORD", "FL456", 150.75, 180, 150)
    
    # Find optimal flights
    print("Finding optimal flights from JFK to LAX...")
    options = system.find_optimal_flights("JFK", "LAX")
    for option in options:
        print(f"Flight: {option.flight_number}, Cost: ${option.cost}, Duration: {option.duration} minutes")
    
    # Book seats
    print("\nBooking seat 25 on flight FL123...")
    system.book_seat("FL123", 25)
    print("\nAvailable seats on flight FL123:")
    system.show_available_seats("FL123")
