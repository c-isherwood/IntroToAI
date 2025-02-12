import random
import math

def generate_cities(n, width=100, height=100):
    # Generates n random cities within a given width and height
    return [(random.randint(0, width), random.randint(0, height)) for _ in range(n)]

def calculate_distance(city1, city2):
    # Calculates  distance between two cities
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def closest_neighbor(cities):
    #Finds the nearest neighbor tour to a given city
    if not cities:
        return [], 0

    start_city = cities[0]
    tour = [start_city]
    current_city = start_city
    unvisited_cities = set(cities[1:])
    total_dist = 0

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: calculate_distance(current_city, city))
        total_dist += calculate_distance(current_city, next_city)
        tour.append(next_city)
        current_city = next_city
        unvisited_cities.remove(next_city)

    # Returning to the start city to complete the tour
    total_dist += calculate_distance(current_city, start_city)
    tour.append(start_city)

    return tour, total_dist

# Generate 10 random cities
cities = generate_cities(10)
tour, distance = closest_neighbor(cities)

# Print the results
print("Tour:", tour)
print("Total Distance:", distance)
