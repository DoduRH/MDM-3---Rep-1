# Contains the obstacle class
import pygame as pg
import globalVariables as gv


class Obstacle:

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    # Draws the obstacle to display
    def draw(self, display):
        pg.draw.rect(display, gv.red, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
