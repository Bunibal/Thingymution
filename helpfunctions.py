import math
import numpy as np
import pygame


# allgemeine Funktionen
def abst(v1, v2):
    """Rechnet v2 minus v1"""
    return (v2[0] - v1[0], v2[1] - v1[1])


def norm(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def normabst(v1, v2):
    return norm(abst(v1, v2))


def mult(v, a, toInteger=False):
    if toInteger:
        return int(v[0] * a), int(v[1] * a)
    return (v[0] * a, v[1] * a)


def addieren(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])


def pInRect(p, rectInfo):
    return pygame.rect.Rect(rectInfo).collidepoint(p)


def getSpeeds(speed, angle):
    angle = angle * math.pi / 180
    return math.cos(angle) * speed, math.sin(angle) * speed


def calcAngle(pos):
    z = np.array(pos[0] + pos[1] * 1.j)
    return np.angle(z) * 180 / math.pi


def getTile(pos):
    return mult(pos, 1 / 16, True)

def tileCoords(tile):
    return mult(tile, 16, True)

def zuschneiden_image(image, rectInfo, scale=1):
    rect = pygame.rect.Rect(rectInfo)
    newImage = pygame.transform.chop(image, (rect.right, rect.bottom, 10000, 10000))  # spaghetti
    newImage = pygame.transform.chop(newImage, (0, 0, rect.left, rect.top))
    size = newImage.get_rect().size
    newImage = pygame.transform.scale(newImage, mult(size, scale, True))
    return newImage
