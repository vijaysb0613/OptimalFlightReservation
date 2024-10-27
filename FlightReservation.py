class Flight:
    def __init__(self, flight_no, departure_time, arrival_time, price):
        self.flight_no = flight_no
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price

    def __repr__(self):
        return f"Flight({self.flight_no}, {self.departure_time}, {self.arrival_time}, {self.price})"
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

class Airport:
    def __init__(self):
        self.flights_by_destination = {}  # Dictionary of red-black trees for each destination.

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
    [0, 2451, 790, 763, 6742, 6860, 3930, 3460],  
    [2451, 0, 1745, 393, 5503, 8277, 5653, 5432], 
    [790, 1745, 0, 606, 6623, 7190, 602, 3850],  
    [763, 393, 606, 0, 6960, 7481, 5433, 4150],  
    [6742, 5503, 6623, 6960, 0, 7359, 6170, 9715], 
    [6860, 8277, 7190, 7481, 7359, 0, 5631, 7155], 
    [3930, 5653, 602, 5433, 6170, 5631, 0, 780], 
    [3460, 5432, 3850, 4150, 9715, 7155, 780, 0]
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


disp_info()
# Example Usage:
FL123 = Flight("FL123", "08:00", "10:00", 500)
FL124 = Flight("FL124", "09:00", "11:00", 300)
FL125 = Flight("FL125", "12:00", "14:00", 450)

LAX = Airport()
LAX.add_flight(FL123, "ATL")
LAX.add_flight(FL124, "ATL")
LAX.add_flight(FL125, "JFK")

# User interaction for selecting airports and price input
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

    price = input("Enter your desired price: ")
    closest_flight = LAX.find_flight_by_price(target, price)
    if closest_flight:
        print(f"Closest flight to {price} for {target}: {closest_flight}")
    else:
        print(f"No matching flights found for price {price} at destination {target}.")
print("-----------------------------------------------------------------------------------")
if start not in airports or target not in airports:
    print("Invalid airport code. Please enter valid airport codes.")
else:
    start_ID = airports[start]  
    target_ID = airports[target]  
    distance, path = dijkstra(graph, start_ID, target_ID)
    airport_names = list(airports.keys())
    print(f"Shortest distance from {start_ID} to {target_ID}: {distance} km")
    print("Path:", " -> ".join(airport_names[i] for i in path))
    price=input()
    closest_flight = LAX.find_flight_by_price(target, price)
    print(closest_flight)
