# TripPlanner

This program uses an object oriented version of the A* algorithm (pathfinder.py) to determine the shortest
path between two cities in a given collection of cities. The program is initially loaded with a
collection of 23 cities from my great home state of Montana. It could work with any collection of cities,
so long as the correct coordinates are generated using coords_generator.py (you will need to replace
assets/map.png with the correct map picture) and the correct city relationships are given in
assets/city_dists.csv. In assets/city_dists.csv, you need only provide a pair of cities and their
corresponding distance once.