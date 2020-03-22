import sys
import requests
import pygame
import os
from random import randrange, choice
from mapModule import *

cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Красноярск', 'Екатеринбург']

mapFile = "map.png"

pygame.init()
screen = pygame.display.set_mode((600, 450))
counter = 0
run = True
time = -4000
while run:
    if pygame.time.get_ticks() - time < 4000:
        screen.blit(pygame.image.load(mapFile), (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    else:
        time = pygame.time.get_ticks()
        coords = getAddressCoords(choice(cities))
        scale = getScale(coords[1:])
        scale = (min(scale[0], 0.15), min(scale[1], 0.15))
        x, y = randrange(0, int(scale[0] * 10 ** 6), 1), randrange(0, int(scale[1] * 10 ** 6), 1)
        mapParams = {
            'll': ','.join(map(str, [coords[0][0] - scale[0] / 2 + x / 10 ** 6, coords[0][1] - scale[1] / 2 + y / 10 ** 6])),
            'z': 15,
            'l': choice(['map', 'sat']),
        }
        mapServer = 'http://static-maps.yandex.ru/1.x/'
        response = requests.get(mapServer, params=mapParams)
        with open(mapFile, "wb") as file:
            file.write(response.content)
pygame.quit()
os.remove(mapFile)
