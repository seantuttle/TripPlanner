import os
import sys
import math
import time
import tkinter
import tkinter.messagebox
import pygame
import pandas as pd
import graph
import pathfinder as pf

pygame.init()
tkinter.Tk().withdraw()

BASE_PATH = os.path.join(os.path.dirname(__file__), 'assets')
CITY_COORDS_PATH = os.path.join(BASE_PATH, 'city_coords.csv')
CITY_DISTS_PATH = os.path.join(BASE_PATH, 'city_dists.csv')
IMG_PATH = os.path.join(BASE_PATH, 'map.png')
ICON_PATH = os.path.join(BASE_PATH, 'icon.ico')
DIST_THRESHOLD = 10
RADIUS = 6
START_COLOR = (0, 173, 67)
END_COLOR = (255, 0, 0)
MIDPOINT_COLOR = (136, 0, 133)

pygame.display.set_caption('Montana Trip Planner')
pygame.display.set_icon(pygame.image.load(ICON_PATH))


def get_closest_city(pos, cities):
    min_dist = math.inf
    closest_city = None
    for city in cities.index:
        dist = math.sqrt((pos[0] - cities.at[city, 'X']) ** 2 + (pos[1] - cities.at[city, 'Y']) ** 2)
        if dist < min_dist:
            min_dist = dist
            closest_city = city

    return closest_city if min_dist < DIST_THRESHOLD else None


def get_cities(win, cities):
    map_img = pygame.image.load(IMG_PATH)
    win.blit(map_img, (0, 0))
    pygame.display.update()
    endpoints = []

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_BACKSPACE or (event.mod & pygame.KMOD_CTRL and event.key == pygame.K_c):
                    return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    city = get_closest_city(event.pos, cities)
                    if city:
                        endpoints.append((city, cities.at[city, 'X'], cities.at[city, 'Y']))
                        if len(endpoints) == 1:
                            pygame.draw.circle(win, START_COLOR, (endpoints[0][1], endpoints[0][2]), RADIUS)
                        elif len(endpoints) == 2:
                            if endpoints[0][0] != endpoints[1][0]:
                                pygame.draw.circle(win, END_COLOR, (endpoints[1][1], endpoints[1][2]), RADIUS)
                                pygame.display.update()

                                msg = f'You want to go from {endpoints[0][0]} to {endpoints[1][0]}?'
                                run = not tkinter.messagebox.askyesno('Confirm Trip', msg)

                                win.fill((0, 0, 0))
                                win.blit(map_img, (0, 0))
                                if run:
                                    endpoints.clear()
                            else:
                                endpoints.pop()

        pygame.display.update()

    if len(endpoints) < 2:
        pygame.quit()
        sys.exit()

    return endpoints[0][0], endpoints[1][0]


def display_results(win, path, distance, cities):
    get_xy = lambda city_name: (cities.at[city_name, 'X'], cities.at[city_name, 'Y'])
    
    count = 0
    for city in path:
        if count in range(1, len(path) - 1):
            color = MIDPOINT_COLOR
        else:
            color = START_COLOR if count == 0 else END_COLOR

        if count != len(path) - 1:
            pygame.draw.line(win, MIDPOINT_COLOR, get_xy(city), get_xy(path[count + 1]), 2)
        pygame.draw.circle(win, color, get_xy(city), RADIUS)
        count += 1

    fnt = pygame.font.SysFont('comicsans', 40)
    text = fnt.render(f'Total Distance: {round(distance, 1)} miles', True, END_COLOR)
    win.blit(text, (460, 495))

    pygame.display.update()


def plan_trip(win, city_coords, city_graph):
    run = True
    while run:
        start, end = get_cities(win, city_coords)
        run = not (start and end)

    try:
        pathfinder = pf.PathFinder(start, end, city_graph)
        path, distance = pathfinder.find_path()
    except RuntimeError as error:
        pygame.quit()
        sys.exit(error)

    time.sleep(0.5)  # a little pause for effect

    display_results(win, path, distance, city_coords)


def main():
    win_size = pygame.image.load(IMG_PATH).get_size()
    win = pygame.display.set_mode(win_size)

    city_graph = graph.Graph(CITY_DISTS_PATH, CITY_COORDS_PATH)

    city_coords = pd.read_csv(CITY_COORDS_PATH, names=['City', 'X', 'Y'], index_col='City', comment='#')
    
    run = True
    while run:
        plan_trip(win, city_coords, city_graph)
        run = tkinter.messagebox.askyesno('Plan Another Trip', 'Do you want to plan another trip?')

    pygame.quit()


if __name__ == "__main__":
    main()
