import networkx as nx
import heapq

# Graph representation using NetworkX for finding optimal flights
class FlightGraph:
    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph for flights

    def add_flight(self, from_airport, to_airport, weight):
        self.graph.add_edge(from_airport, to_airport, weight=weight)

    def find_optimal_route(self, start, end):
        try:
            # Dijkstra's algorithm to find the shortest path
            path = nx.dijkstra_path(self.graph, start, end, weight="weight")
            cost = nx.dijkstra_path_length(self.graph, start, end, weight="weight")
            return path, cost
        except nx.NetworkXNoPath:
            return None, float('inf')

# Red-Black Tree Node and Tree Structure for managing flights and seats
class RBTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.color = "red"  # Red-Black Tree property

class RBT:
    def __init__(self):
        self.root = None

    def insert(self, node):
        if not self.root:
            self.root = node
            self.root.color = "black"
        else:
            # Insert logic here for Red-Black Tree (simplified for demonstration)
            pass

    def search(self, key):
        current = self.root
        while current:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

# Priority Queue for presenting optimal flights based on criteria
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add_flight(self, cost, flight_info):
        heapq.heappush(self.queue, (cost, flight_info))

    def get_best_flights(self):
        best_flights = []
        while self.queue:
            best_flights.append(heapq.heappop(self.queue))
        return best_flights

# Seat Management with HashMap and RBT for seats
class Seat:
    def __init__(self, seat_id):
        self.seat_id = seat_id

class SeatManager:
    def __init__(self):
        self.seats = {}  # HashMap mapping flight number to RBT of seats

    def add_seat(self, flight_number, seat_id):
        if flight_number not in self.seats:
            self.seats[flight_number] = RBT()  # Initialize RBT for the flight
        seat_node = RBTNode(seat_id)
        self.seats[flight_number].insert(seat_node)

    def book_seat(self, flight_number, seat_id):
        flight_tree = self.seats.get(flight_number)
        if flight_tree:
            seat = flight_tree.search(seat_id)
            if seat:
                print(f"Seat {seat_id} booked successfully on flight {flight_number}")
            else:
                print(f"Seat {seat_id} not available on flight {flight_number}")

# Main function to bring it all together
def main():
    # Initialize graph, priority queue, and seat manager
    flight_graph = FlightGraph()
    priority_queue = PriorityQueue()
    seat_manager = SeatManager()

    # Add flights to the graph (from_airport, to_airport, cost)
    flight_graph.add_flight("JFK", "LAX", 300)
    flight_graph.add_flight("JFK", "ORD", 150)
    flight_graph.add_flight("ORD", "LAX", 200)

    # Find optimal route between two airports
    route, cost = flight_graph.find_optimal_route("JFK", "LAX")
    if route:
        print("Optimal route:", " -> ".join(route), "with cost:", cost)
    else:
        print("No route found.")

    # Add flights to priority queue based on criteria
    priority_queue.add_flight(300, {"flight_no": "AA101", "from": "JFK", "to": "LAX"})
    priority_queue.add_flight(200, {"flight_no": "UA102", "from": "ORD", "to": "LAX"})
    priority_queue.add_flight(400, {"flight_no": "DL103", "from": "JFK", "to": "LAX"})

    # Get best flights sorted by cost
    best_flights = priority_queue.get_best_flights()
    print("Best flight options based on cost:")
    for cost, flight in best_flights:
        print(f"Flight {flight['flight_no']} from {flight['from']} to {flight['to']} - Cost: {cost}")

    # Seat management - Adding and booking seats
    seat_manager.add_seat("AA101", "12A")
    seat_manager.add_seat("AA101", "12B")
    seat_manager.book_seat("AA101", "12A")  # Should succeed
    seat_manager.book_seat("AA101", "12C")  # Should fail (not added)

if __name__ == "__main__":
    main()
