#=============================================================================================================#
#                                                    *librerias  
#=============================================================================================================#
import pygame, sys
from pygame.locals import *
from functions import load_image
#=============================================================================================================#
#                                              *Clase pantalla de carga         
#=============================================================================================================#
class loading_screen:
    def __init__(self):
        
        #Atributos
        self.gif = []  #Lista donde se guarda cada una de las imagenes del gif

        for i in range(30):  #Se añaden las imagenes a la lista
            self.gif.append(load_image(f"Assets/Loading screen/{i}.png", 1280, 720))

        self.current_img = 0  
        self.image = self.gif[self.current_img]
        self.rect = self.image.get_rect(center=(640, 360))
        self.sound = pygame.mixer.Sound("Assets/Sfx/Nyan.wav")
        self.sound.play(-1)
        
    def update(self, speed):  #Hacer que las imagenes parezcan un gif
        self.current_img += speed
        if self.current_img < len(self.gif):
            self.image = self.gif[int(self.current_img)]
        else:
            self.current_img = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def run(self, surface):
        for event in pygame.event.get():  
            if event.type == QUIT:  
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  
                    sys.exit(0)

        self.draw(surface)
        self.update(0.4)