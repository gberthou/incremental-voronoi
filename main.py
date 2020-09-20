import sys
import math

import voronoi

SIZE = (1024, 720)
FPS = 60

ZOOM = 4
PX_TO_WORLD = lambda x: x * ZOOM / SIZE[1]
WORLD_TO_PX = lambda x: int(x * SIZE[1] / ZOOM)

def to_px(point):
    return (WORLD_TO_PX(point[0]), WORLD_TO_PX(point[1]))

def update_viewport(voronoi_explorer, offset_x, offset_y):
    MARGINX = 1
    MARGINY = 1

    xmin = math.floor(PX_TO_WORLD(offset_x))
    xmax = math.ceil(PX_TO_WORLD(SIZE[0] + offset_x))

    ymin = math.floor(PX_TO_WORLD(offset_y))
    ymax = math.ceil(PX_TO_WORLD(SIZE[1] + offset_y))

    keys_to_keep = set((x, y) for x in range(xmin - MARGINX, xmax + MARGINX + 1) for y in range(ymin - MARGINY, ymax + MARGINY + 1))
    voronoi_explorer.keep_only_chunks(keys_to_keep)

    for key in keys_to_keep:
        voronoi_explorer.load_chunk(key)

v = voronoi.VoronoiExplorer("world0", 4)

import math
import pygame

import shapes

class VoronoiViewer:
    def __init__(self, v):
        self.v = v

    def draw(self, surface, offset_x, offset_y):
        for p in self.v.pointset.point_items:
            screen_pos = to_px(p.point)
            screen_pos = (screen_pos[0] - offset_x, screen_pos[1] - offset_y)
            pygame.draw.circle(surface, (0, 255, 0), screen_pos, 2)

            shape = shapes.Shape(p)
            if len(shape.vertices) >= 3:
                points = list(to_px(v) for v in shape.vertices)
                points = list((x - offset_x, y - offset_y) for x, y in points)
                pygame.draw.polygon(surface, (255, 0, 255), points, 4)

pygame.init()
screen = pygame.display.set_mode(SIZE)

done = False
clock_fps = pygame.time.Clock()

viewer = VoronoiViewer(v)

direction_x = 0
direction_y = 0

offset_x = 0
offset_y = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        direction_x = -5
    elif pressed[pygame.K_RIGHT]:
        direction_x = 5
    else:
        direction_x = 0
    if pressed[pygame.K_UP]:
        direction_y = -5
    elif pressed[pygame.K_DOWN]:
        direction_y = 5
    else:
        direction_y = 0
    if pressed[pygame.K_F1]:
        ZOOM += .1
    elif pressed[pygame.K_F2]:
        ZOOM -= .1
        if ZOOM < 1:
            ZOOM = 1

    offset_x += direction_x
    offset_y += direction_y
    update_viewport(v, offset_x, offset_y)

    screen.fill((0, 0, 0))
    viewer.draw(screen, offset_x, offset_y)
    pygame.display.flip()
    clock_fps.tick_busy_loop(FPS)
