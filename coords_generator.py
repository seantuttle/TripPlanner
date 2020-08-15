import os
from tkinter import *
import pygame

pygame.init()

BASE_PATH = os.path.join(os.path.dirname(__file__), 'assets')
CSV_PATH = os.path.join(BASE_PATH, 'city_coords.csv')
TSV_PATH = os.path.join(BASE_PATH, 'city_coords.tsv')
IMG_PATH = os.path.join(BASE_PATH, 'map.png')
ICON_PATH = os.path.join(BASE_PATH, 'icon.ico')
RADIUS = 6

pygame.display.set_caption('Coordinates Generator')
pygame.display.set_icon(pygame.image.load(ICON_PATH))


def point_name_callback(root, entry, point):
    point.append(entry.get())
    if point and point[0]:
        is_valid = True
        for token in point[0].split():
            if not token[0].isupper():
                is_valid = False
                break

        if is_valid:
            root.destroy()
        else:
            point.clear()
    else:
        point.clear()


def get_point_name():
    point = []
    root = Tk()

    entry = Entry(root, width=15)
    entry.pack()
    entry.focus_set()

    point_name_lambda = lambda: point_name_callback(root, entry, point)
    Button(root, text='Set Point', width=10, command=point_name_lambda).pack()
    Button(root, text='Cancel', width=10, command=root.destroy).pack()

    mainloop()

    return point[0] if point else None


def write_point_to_file(point, x, y, path, sep):
    if point:
        with open(path, 'a') as f:
            f.write(f'\n{point}{sep}{x}{sep}{y}')


def point_creation_loop(win, csv_or_tsv_path, sep):
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONUP:
                curr_img = pygame.display.get_surface().copy()
                pygame.draw.circle(win, (255, 0, 0), event.pos, RADIUS)
                pygame.display.update()
                point = get_point_name()
                if point:
                    write_point_to_file(point, event.pos[0], event.pos[1], csv_or_tsv_path, sep)
                else:
                    win.fill((255, 255, 255))
                    win.blit(curr_img, (0, 0))
                    pygame.display.update()

    pygame.quit()


def make_file(img_path, csv_or_tsv_path, sep):
    img = pygame.image.load(img_path)
    win = pygame.display.set_mode(img.get_size())
    win.blit(img, (0, 0))
    pygame.display.update()

    with open(csv_or_tsv_path, 'w') as f:
        f.write('# name,x_coord,y_coord')

    point_creation_loop(win, csv_or_tsv_path, sep)


def make_csv(img_path, csv_path):
    if os.path.basename(csv_path)[-4:] == '.csv':
        make_file(img_path, csv_path, ',')
    else:
        raise ValueError('Path needs to lead to a .csv file')

def make_tsv(img_path, tsv_path):
    if os.path.basename(tsv_path)[-4:] == '.tsv':
        make_file(img_path, tsv_path, '\t')
    else:
        raise ValueError('Path needs to lead to a .tsv file')


if __name__ == "__main__":
    make_csv(IMG_PATH, CSV_PATH)
