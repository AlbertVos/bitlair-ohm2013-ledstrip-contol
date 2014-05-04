import pygame
from pygame.locals import *

pygame.init()
surf=pygame.display.set_mode((200,200))
pygame.display.set_caption("Child Window")

gameOver=False

while not gameOver:
    for e in pygame.event.get():
        if e.type==QUIT:
            gameOver=True
        if e.type==KEYDOWN:
            if e.key==K_ESCAPE:
                gameOver=True
                
