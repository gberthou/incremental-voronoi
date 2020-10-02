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

    keys_to_keep = set((x, y) for x in range(xmin - MARGINX, xmax + 1 + MARGINX) for y in range(ymin - MARGINY, ymax + 1 + MARGINY))
    voronoi_explorer.keep_only_chunks(keys_to_keep)

    for key in keys_to_keep:
        voronoi_explorer.load_chunk(key)

def point_item_to_hull(point_item, offset_x, offset_y):
    shape = shapes.Shape(point_item)
    points = list(to_px(v) for v in shape.vertices)
    return list((x - offset_x, y - offset_y) for x, y in points)

v = voronoi.VoronoiExplorer("world0", 4)

import math
import pygame

import shapes

class VoronoiViewer:
    def __init__(self, v):
        self.v = v
        self.offset_x = 0
        self.offset_y = 0

        self.selected_polygon = None
        #self.selected_neighbors = None

    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y

        centerX = PX_TO_WORLD(SIZE[0] / 2 + offset_x)
        centerY = PX_TO_WORLD(SIZE[1] / 2 + offset_y)
        point_item_center = self.v.pointset.item_that_contains((centerX, centerY))

        self.selected_polygon = point_item_to_hull(point_item_center, x, y)
        #self.selected_neighbors = self.v.pointset.neighbors_of(point_item_center)
        print(len(self.v.pointset.neighbors_of(point_item_center)))

    def draw(self, surface):
        for p in self.v.pointset.point_items:
            screen_pos = to_px(p.point)
            screen_pos = (screen_pos[0] - self.offset_x, screen_pos[1] - self.offset_y)
            pygame.draw.circle(surface, (0, 255, 0), screen_pos, 2)

            points = point_item_to_hull(p, self.offset_x, self.offset_y)
            if len(points) >= 3:
                pygame.draw.polygon(surface, (255, 0, 255), points, 4)

            if self.selected_polygon != None:
                pygame.draw.polygon(surface, (255, 0, 255), self.selected_polygon)

                #for neighbor in self.selected_neighbors:
                #    points = point_item_to_hull(neighbor, offset_x, offset_y)
                #    if len(points) >= 3:
                #        pygame.draw.polygon(surface, (255, 255, 255), points)

pygame.init()
screen = pygame.display.set_mode(SIZE)

done = False
clock_fps = pygame.time.Clock()

viewer = VoronoiViewer(v)

direction_x = 0
direction_y = 0

offset_x = 0
offset_y = 0

update_viewport(v, offset_x, offset_y)
viewer.set_offset(offset_x, offset_y)

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
    if direction_x != 0 or direction_y != 0:
        viewer.set_offset(offset_x, offset_y)

    update_viewport(v, offset_x, offset_y)

    screen.fill((0, 0, 0))
    viewer.draw(screen)
    pygame.display.flip()
    clock_fps.tick_busy_loop(FPS)
