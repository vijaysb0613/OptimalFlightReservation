import random
from tabulate import tabulate
class Flight:
    def __init__(self, flight_no, departure_time, arrival_time, price,total_seats):
        self.flight_no = flight_no
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.total_seats = total_seats
        self.remaining_seats = total_seats  # Initialize remaining seats to the total seats
    def book_seat(self):
        if self.remaining_seats > 0:
        # Ask for confirmation before booking
            confirm = input(f"Do you want to book a seat on flight {self.flight_no} for ${self.price}? (yes/no): ")
            if confirm.lower() == 'yes':
                self.remaining_seats -= 1
                print(f"✅ Seat successfully booked on flight {self.flight_no}!")
                self.print_ticket()  # Print ticket details
            else:
                print("🚫 Booking canceled.")  # Message if booking is canceled
        else:
            print(f"🚫 No seats available on flight {self.flight_no}.")
            print("Please try another flight or check back later.")
    #a function to print the ticket confirmation.
    def print_ticket(self):
        print("\n" + "="*40)
        print(f"🎟  Flight Ticket for {self.flight_no}")
        print("="*40)
        print(f"🛫 Departure: {self.departure_time}")
        print(f"🛬 Arrival: {self.arrival_time}")
        print(f"💸 Price: ${self.price}")
        print(f"💺 Remaining seats: {self.remaining_seats}")
        print("="*40 + "\n")


    def repr(self):
        return f"Flight({self.flight_no}, {self.departure_time}, {self.arrival_time}, {self.price})"
    def info(self):
        return {
            "Flight No": self.flight_no,
            "Departure": self.departure_time,
            "Arrival": self.arrival_time,
            "Price": f"${self.price}"
        }

class Node:
     def __init__(self, flight):
        self.flight = flight
        self.left = None
        self.right = None
        self.parent = None
        self.color = "RED"  # Red by default for new nodes in red-black trees.

class RedBlackTree:
    def __init__(self):
        self.nil = Node(None)  # Sentinel node for leaves.
        self.nil.color = "BLACK"
        self.root = self.nil
    def insert(self, flight):
        # Create the new node to insert.
        new_node = Node(flight)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.color = "RED"  # New nodes start as red.

        # Standard BST insert
        parent = None
        current = self.root
        
        while current != self.nil:
            parent = current
            if new_node.flight.price < current.flight.price:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.flight.price < parent.flight.price:
            parent.left = new_node
        else:
            parent.right = new_node

        # Call to fix violations and rebalance the tree
        self.fix_insert(new_node)

    def left_rotate(self, node):
        # Left rotate around the given node
        y = node.right
        node.right = y.left
        if y.left != self.nil:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def right_rotate(self, node):
        # Right rotate around the given node
        y = node.left
        node.left = y.right
        if y.right != self.nil:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def fix_insert(self, node):
        # Fix red-black tree properties after insertion
        while node != self.root and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Uncle is black and node is a right child
                        node = node.parent
                        self.left_rotate(node)
                    # Case 3: Uncle is black and node is a left child
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    # Case 1: Uncle is red
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Case 2: Uncle is black and node is a left child
                        node = node.parent
                        self.right_rotate(node)
                    # Case 3: Uncle is black and node is a right child
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)

        # Ensure the root is black
        self.root.color = "BLACK"
    def find_closest_price(self, price):
        # Find the flight with the closest price to the specified price
        closest_flight = None
        current = self.root
        min_difference = float("inf")

        while current != self.nil:
            current_difference = abs(current.flight.price - price)
            if current_difference < min_difference:
                min_difference = current_difference
                closest_flight = current.flight
            
            if price < current.flight.price:
                current = current.left
            else:
                current = current.right
        
        return closest_flight
    def print_tree(self):
        # Start the recursive printing from the root
        self._print_tree_helper(self.root, "", True)

    def _print_tree_helper(self, node, indent, last):
        if node != self.nil:
            print(indent, end="")
            if last:
                print("R----", end="")  # R for right child
                indent += "     "
            else:
                print("L----", end="")  # L for left child
                indent += "|    "
            print(f"{node.flight.price} ({node.color})")  # Print the price and color
            self._print_tree_helper(node.left, indent, False)
            self._print_tree_helper(node.right, indent, True)
def print_flights_table(airports_with_flights, airport_codes=None):
# If no specific airport codes are provided, print all airports
    if airport_codes is None:
        airport_codes = airports_with_flights.keys()

    for airport_code in airport_codes:
            # Check if the airport code exists in the dictionary
        if airport_code not in airports_with_flights:
            print(f"\n🚫 Airport code {airport_code} not found.")
            continue

        airport = airports_with_flights[airport_code]
        print(f"\nFlights from {airport_code}:\n")
            # Print the table headers
        print(f"{'Destination':<12} {'Flight No':<10} {'Departure':<10} {'Arrival':<10} {'Price':<10}{'Color':<6}")
        print("-" * 60)

            # Loop through each destination and red-black tree to display flights in tabular form
        for destination, rbtree in airport.flights_by_destination.items():
            flights = []
            colors = []
            
            # Helper function to collect all flights from the red-black tree
            def collect_flights(node):
                if node != rbtree.nil:
                    collect_flights(node.left)
                    flights.append(node.flight)
                    colors.append(node.color)
                    collect_flights(node.right)

            # Collect and print each flight for this destination
            collect_flights(rbtree.root)
            for i, flight in enumerate(flights):
                print(f"{destination:<12} {flight.flight_no:<10} {flight.departure_time:<10} {flight.arrival_time:<10} {flight.price:<10}{colors[i]:<10}")
        
        print("-" * 60)

 # Divider line between airports

# Call the function to display flights in table format
class Airport:
    def __init__(self, name):
        self.flights_by_destination = {}  # Dictionary of red-black trees for each destination.
        self.name = name

    def add_flight(self, flight, destination):
        if destination not in self.flights_by_destination:
            self.flights_by_destination[destination] = RedBlackTree()
        self.flights_by_destination[destination].insert(flight)

    def find_flight_by_price(self, destination, price):
        try:
            price = float(price)  # Ensure price is a numeric type for comparison.
        except ValueError:
            print("Invalid price format. Please enter a numeric value.")
            return None

        if destination in self.flights_by_destination:
            return self.flights_by_destination[destination].find_closest_price(price)
        else:
            print(f"No flights found for destination: {destination}")
            return None

graph = [
    [0, 2475, 790, 760, float('inf'), float('inf'), 4200, 3460],  # JFK
    [2475, 0, 1750, 2100, 5500, float('inf'), 5400, 5500], # LAX
    [790, 1750, 0, 590, float('inf'), 6300, float('inf'), float('inf')],   # ORD
    [760, 2100, 590, 0, 6050, float('inf'), 4600, 4250],   # ATL
    [float('inf'), 5500, float('inf'), 6050, 0, 3500, 6050, 5700], # HND
    [float('inf'),float('inf') , 6300, float('inf'), 3500, 0, 3500, 3400], # DXB
    [4200, 5400, float('inf'), 4600, 6050, 3500, 0, 700],   # FRA
    [3460, 5500, float('inf'), 4250, 5700, 3400, 700, 0]    # LHR
]


airports = {
    'JFK': 0,  
    'LAX': 1,  
    'ORD': 2,  
    'ATL': 3, 
    'HND': 4, 
    'DXB': 5,  
    'FRA': 6, 
    'LHR': 7   
}

def dijkstra(graph, start, target):
    n = len(graph)
    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0
    visited = [False] * n
    parent = [-1] * n  
    for _ in range(n):
        min_dist = INF
        u = -1
        for i in range(n):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i

        visited[u] = True

        for v in range(n):
            if graph[u][v] > 0 and not visited[v] and dist[u] + graph[u][v] < dist[v]:
                dist[v] = dist[u] + graph[u][v]
                parent[v] = u 

    path = []
    current = target
    while current != -1:
        path.append(current)
        current = parent[current]
    path.reverse() 

    return dist[target], path

def disp_info():
    print("Available airports and their indices:")
    for code, index in airports.items():
        print(f"{index}: {code}")
def get_airport_code_by_index(index):
    for code, idx in airports.items():
        if idx == index:
            return code
    return "Index not found"


disp_info()
# Example Usage:

# User interaction for selecting airports and price input
print("-----------------------------------------------------------------------------------")
def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02}:{minute:02}"

# Sample function to generate flights for each direct connection
def generate_flights_for_airport(airport_code, airport_index, num_flights=3):
    flights = []
    for dest_index, distance in enumerate(graph[airport_index]):
        if distance != float('inf') and distance > 0:  # Only consider reachable destinations
            for _ in range(num_flights):  # Generate multiple flights per destination
                flight_no = f"FL{random.randint(100, 999)}"  # Generate unique flight number
                departure_time = random_time()
                arrival_time = random_time()
                price = random.randint(200, 2000)  # Random price for the flight
                flight = Flight(flight_no, departure_time, arrival_time, price,5)
                flights.append((dest_index, flight))  # Store the destination and flight
    return flights


# Initialize airports and add flights
airports_with_flights = {}

for airport_code, airport_index in airports.items():
    airport = Airport(airport_code)
    # Specify the number of flights per destination here
    flights = generate_flights_for_airport(airport_code, airport_index, num_flights=5)
    for dest_index, flight in flights:
        destination_code = list(airports.keys())[dest_index]  # Get destination airport code
        airport.add_flight(flight, destination_code)
    airports_with_flights[airport_code] = airport 

# Print all flights going to each destination from every airport

selected_airports = input("Enter the airport codes you want to display : ")

# Convert the input string to a list by splitting on commas and removing extra spaces
selected_airports = [code.strip() for code in selected_airports.split(" ")]

# Print only flights from the selected airports
print_flights_table(airports_with_flights, selected_airports)

# Displaying the flights added to each airport
start = input("Enter the start airport code: ").upper()
target = input("Enter the target airport code: ").upper()

if start not in airports or target not in airports:
    print("Invalid airport code. Please enter valid airport codes.")
else:
    start_ID = airports[start]
    target_ID = airports[target]
    distance, path = dijkstra(graph, start_ID, target_ID)
    airport_names = list(airports.keys())
    print(f"Shortest distance from {start} to {target}: {distance} km")
    print("Path:", " -> ".join(airport_names[i] for i in path))
    print(path)

    # Retrieve the airport object for the start location

    start_airport = airports_with_flights[get_airport_code_by_index(path[0])]
    price = input("Enter your desired price: ")
    table_data = []  # Store data for table display

for i in range(1, len(path)):
    destination_code = get_airport_code_by_index(path[i])  # Get the correct destination code as a string
    closest_flight = start_airport.find_flight_by_price(destination_code, price)
    closest_flight.book_seat()
    if closest_flight:
        flight_info = closest_flight.info()
        row = [
            start_airport.name,
            destination_code,
            flight_info["Flight No"],
            flight_info["Departure"],
            flight_info["Arrival"],
            flight_info["Price"]
        ]
        table_data.append(row)
    else:
        table_data.append([start_airport.name, destination_code, "No matching flight", "-", "-", "-"])

    # Update start_airport for the next leg of the path
    start_airport = airports_with_flights[get_airport_code_by_index(path[i])]

# Define table headers
headers = ["From", "To", "Flight No", "Departure", "Arrival", "Price"]

# Display the table
print(tabulate(table_data, headers=headers, tablefmt="grid"))
