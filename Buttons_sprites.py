#=============================================================================================================#
#                                                    *librerias  
#=============================================================================================================#
import pygame
from pygame.locals import *
from functions import load_image
#=============================================================================================================#
#                                           *Clase Botones de los números         
#=============================================================================================================#
class number_buttons(pygame.sprite.Sprite):  #Se hereda de la clase sprite de pygame para usar los grupos sprite
    def __init__(self, image_pic, img_size:tuple, pos:tuple, number:int):
        super().__init__()

        #Condiciones para que el programa cumpla su función adecuadamente
        if(number not in range(1,10)):
            raise ValueError ("Solo se reciben valores del 1 al 9")

        #Atributos
        self.image_pic = image_pic 
        self.number = number  
        self.image = load_image(self.image_pic, img_size[0], img_size[1], False, True)  
        self.rect = self.image.get_rect(topleft=pos)  
    
    #Métodos
    def get_number(self):  #Getter que retorna el número del botón
        return self.number

    def update(self, img_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.image = load_image(self.image_pic, img_size[0], img_size[1], False, True)  
        self.rect.update(pos, img_size)  

    def draw(self, surface):  
        surface.blit(self.image, self.rect)

    def click(self, size:tuple):  #Cambia el tamaño del botón para mostrar un click
        center = self.rect.center
        self.image = load_image(self.image_pic, size[0], size[1], False, True)
        self.rect.size = size
        self.rect.center = center
    
    def smoothness(self, size:tuple):  #Cambia el tamaño cuando se le pasa por encima el mouse
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.click((size[0]*0.95, size[1]*0.95))
        else:
            self.click(size)
    
    @staticmethod
    def check_if_pressed(button, size:tuple):  #Revisa si un botón númerico esta oprimido, y lo devuelve a su estado normal
        if button != None:
            button.click(size)
#=============================================================================================================# 
#                                             *Clase Botones con acciones 
#=============================================================================================================#
class actions_buttons: 
    def __init__(self, image_pic, img_size:tuple, pos:tuple):

        #Atributos
        self.image_pic = image_pic  
        self.image = load_image(self.image_pic, img_size[0], img_size[1], False, True)  
        self.rect = self.image.get_rect(topleft=pos)  
    
    #Métodos
    def update(self, img_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.image = load_image(self.image_pic, img_size[0], img_size[1], False, True)  
        self.rect.update(pos, img_size)  

    def draw(self, surface):  
        surface.blit(self.image, self.rect)

    def click(self, size:tuple):  #Cambia el tamaño del botón para mostrar un click
        center = self.rect.center
        self.image = load_image(self.image_pic, size[0], size[1], False, True)
        self.rect.size = size
        self.rect.center = center

    def smoothness(self, size:tuple):  #Cambia el tamaño cuando se le pasa por encima el mouse
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.click((size[0]*0.95, size[1]*0.95))
        else:
            self.click(size)
#=============================================================================================================#
#                                                   *Clase palabra   
#=============================================================================================================#
class word: 
    def __init__(self, text:str, size:int, color:tuple, pos:tuple):
        
        #Atributos
        self.font = pygame.font.Font('Assets/Images/Font.TTF', size)  #Se elige la fuente para el texto
        self.text = text  
        self.color = color  
        self.image = self.font.render(self.text, True, self.color)  #Se pone el texto y el color en una imagen renderizada
        self.rect = self.image.get_rect(topleft=pos)  

    #Getters y setters
    @property
    def text_(self):  
        return self.text

    @text_.setter
    def text_(self, text:str):  
        self.text = text
        self.image = self.font.render(self.text, True , self.color)  #Se actualiza el texto

    @property
    def color_(self):  
        return self.color
    
    @color_.setter
    def color_(self, color:tuple):  
        self.color = color 
        self.image = self.font.render(self.text, True , self.color)  #Se actualiza el color

    #Métodos
    def update(self, size:int, pos:tuple):  #Se actualiza el tamaño y la posición
        self.font = pygame.font.Font('Assets/Images/Font.TTF', size) 
        self.image = self.font.render(self.text, True, self.color)  
        self.rect = self.image.get_rect(topleft=pos) 

    def draw(self, surface):  #Se dibuja el texto en la ventana
        surface.blit(self.image, self.rect)
    
    def click(self, size:int):  #Cambia el tamaño del botón para mostrar un click
        center_ = self.rect.center
        self.font = pygame.font.Font('Assets/Images/Font.TTF', size)  
        self.image = self.font.render(self.text, True, self.color) 
        self.rect = self.image.get_rect(center=center_)
    
    def smoothness(self, size:int):  #Cambia el tamaño cuando se le pasa por encima el mouse
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.click(round(size*0.90))
        else:
            self.click(size)
#=============================================================================================================#
#                                            *Clase botones con animación
#=============================================================================================================#
class animated_button:
    def __init__(self, text:str, text_size:int, button_size:tuple, pos:tuple, elevation, top_color:tuple, botton_color:tuple, text_color:tuple):
        
        #Atributos
        self.action = False
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.click_sound = pygame.mixer.Sound("Assets/Sfx/button_click.wav")
        self.hover_sound = pygame.mixer.Sound("Assets/Sfx/hover.wav")
        self.actived = False

        #rectángulo superior 
        self.top_rect = pygame.Rect((0, 0), button_size)
        self.top_rect.center = pos
        self.top_color = top_color

        #rectángulo inferior
        self.bottom_rect = pygame.Rect((0, 0), button_size)
        self.bottom_rect.center = pos
        self.bottom_color = botton_color 
        
        #texto
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font('Assets/Images/Font.TTF', text_size)
        self.text_surf = self.font.render(self.text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)  #La flag "border radius" se usa para que el rectángulo tenga los bordes redondeados
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self, color:tuple, hover_color:tuple):
        if self.top_rect.collidepoint(pygame.mouse.get_pos()):
            self.top_color = hover_color  #Si el mouse está encima del botón, se cambia el color
            if not self.actived:
                self.hover_sound.play()
                self.actived = True
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0  #Cuando se oprime el click, se hace el efecto de hundirse
                self.pressed = True  #Y se guarda en este atributo que se oprimió
            else:
                self.dynamic_elevation = self.elevation  #Si no esta oprimido, el botón vuelve a la normalidad
                if self.pressed == True:  
                    self.action = True  #Y si se habia oprimido el click anteriormente, se activa la acción correspondiente
                    self.click_sound.play()
                    self.pressed = False
        else:
            self.pressed = False  #Si se sale el mouse del botón, se desactiva el click en caso de haber sido oprimido
            self.dynamic_elevation = self.elevation  #El botón vuelve a la normalidad
            self.top_color = color  #Y el color vuelve a su color base}
            self.actived = False

        return self.action
    
    def update(self, text_size, button_size, pos, elevation):
        self.original_y_pos = pos[1]
        self.elevation = elevation
        self.dynamic_elevation = elevation

        self.top_rect.size = button_size
        self.top_rect.center = pos
        self.bottom_rect.size = button_size
        self.bottom_rect.center = pos

        self.font = pygame.font.Font('Assets/Images/Font.TTF', text_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
