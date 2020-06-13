import pygame
import tkinter as tk
pygame.font.init()

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

GROESSE = BREITE, HOEHE = screen_width, screen_height

# menu
GROESSEBUTTONS = 300
GROESSEMESSAGES = (BREITE // 6, HOEHE // 5)
# Game
ZOOM = 0.9
GROESSEBUTTONSGAME = 200
GROESSEBUTTONSNEUERZUG = 200
GROESSECARD = (200, 300)
BARBREITE = int(BREITE - BREITE / 6)
# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
FARBENSPIELER = [(0, 0, 255), (255, 0, 0),
                 (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255), (150, 255, 150),
                 (200,200,0), (0, 150, 255), (255, 100, 50)]

# Schriftarten
FONT1 = pygame.font.SysFont("chiller", 50)
FONT2 = pygame.font.SysFont("Times", 30)
FONT2BIG = pygame.font.SysFont("Times", 70)
# Bildgroessen
BILDGROESSESCHNECKE = (16, 8)
BILDGROESSEMAUS = (16, 16)
BILDGROESSEKRABBE = (16, 8)
BILDGROESSEFALKE = (16, 16)
BILDGROESSEKAEFER = (16, 8)
BILDGROESSEDOKTORFISCH = (16, 8)
BILDGROESSEFUCHS = (16, 16)
BILDGROESSEKANINCHEN = (14, 14)
BILDGROESSEZIEGE = (20, 20)
BILDGROESSESINGVOGEL = (16, 16)
