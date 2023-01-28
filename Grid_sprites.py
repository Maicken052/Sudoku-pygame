#=============================================================================================================#
#                                                    *librerias  
#=============================================================================================================#
import pygame
from pygame.locals import *
from dokusan import generators
import numpy as np
from copy import deepcopy
from functions import load_image
#=============================================================================================================#
#                                           *Clase números de las casillas      
#=============================================================================================================#
class box_numbers: 
    def __init__(self, img_size:tuple, pos:tuple, number:int=0):

        #Condiciones para que el programa cumpla su función adecuadamente
        if(number not in range(0,10)):
            raise ValueError ("Solo se reciben valores del 0 al 9")

        #Atributos
        self.img_size = img_size 
        self.number = number 
        self.possible_imgs = { 
            0:"Assets/Images/WHITE.png",
            1:"Assets/Images/1.png",
            2:"Assets/Images/2.png",
            3:"Assets/Images/3.png",
            4:"Assets/Images/4.png",
            5:"Assets/Images/5.png",
            6:"Assets/Images/6.png",
            7:"Assets/Images/7.png",
            8:"Assets/Images/8.png",
            9:"Assets/Images/9.png",
        }
        self.image = load_image(self.possible_imgs[self.number], self.img_size[0], self.img_size[1])  #Se ajusta al tamaño deseado y se escoge una imagen del diccionario según el número que corresponda
        self.rect = self.image.get_rect(center=pos)  

    #Métodos
    def set_number(self, num:int):  #Setter para actualizar el número de la casilla
        self.number = num
        self.image = load_image(self.possible_imgs[self.number], self.img_size[0], self.img_size[1]) 

    def get_number(self):  #Getter para obtener el número de la casilla
        return self.number

    def update(self, img_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.img_size = img_size  
        self.image = load_image(self.possible_imgs[self.number], self.img_size[0], self.img_size[1])  
        self.rect.size = img_size  
        self.rect.center = pos  

    def draw(self, surface):  
        surface.blit(self.image, self.rect)
#=============================================================================================================# 
#                                                 *Clase casilla   
#=============================================================================================================#
class box(pygame.sprite.Sprite): #Se hereda de la clase sprite de pygame para usar los grupos sprite
    def __init__(self, img_size:tuple, num_size:tuple, pos:tuple, num_in_box:int=0, background_color:int=0):
        super().__init__()

        #Condiciones para que el programa cumpla su función adecuadamente
        if(num_in_box not in range(0,10)):
            raise ValueError ("Solo se reciben valores del 0 al 9")

        #Atributos
        self.image = load_image('Assets/Images/Box.png', img_size[0], img_size[1], True) 
        self.rect = self.image.get_rect()  
        self.background_color = background_color  #El color de fondo de la casilla 

        #Posición de la casilla (Arriba, Abajo, Derecha, Izquierda, Centro en x, Centro en y)
        if pos[0] != None:
            self.rect.top = pos[0]
        if pos[1] != None:
            self.rect.bottom = pos[1]
        if pos[2] != None:
            self.rect.right = pos[2]
        if pos[3] != None:
            self.rect.left = pos[3]
        if pos[4] != None:
            self.rect.centerx = pos[4]
        if pos[5] != None:
            self.rect.centery = pos[5]

        self.data = box_numbers(num_size, self.rect.center, num_in_box)  #El número dentro de la casilla 
        self.correct_number = 0  #El número que debe ir en la casilla

        #Imagen del color verde dentro de la casilla
        self.correct_num_color = load_image("Assets/Images/LightGreen.png", self.rect.width/1.5, self.rect.height/1.5)  
        self.correct_num_color_rect = self.correct_num_color.get_rect(center=self.rect.center)  

        #Imagen del color rojo dentro de la casilla
        self.wrong_num_color = load_image("Assets/Images/LightRed.png", self.rect.width/1.5, self.rect.height/1.5)  
        self.wrong_num_color_rect = self.wrong_num_color.get_rect(center=self.rect.center) 

    #Métodos
    def get_data(self):  #Getter que retorna el número en la casilla
        if self.background_color == 2:  #Si el fondo está en rojo, es porque el número esta mal, por lo que se retorna 0
            return 0
        else:
            return self.data.get_number()

    def get_correct_number(self):  #Getter que retorna el número correcto
        return self.correct_number

    def set_data(self, num:int, option:int, color:int=0):  #setter con dos opciones
        if option == 1:  #Poner el número que se ve en la ventana y el color de fondo
            self.data.set_number(num)
            self.background_color = color
        if option == 2:  #Poner el dato correcto
            self.correct_number = num

    def update(self, img_size:tuple, num_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.image = load_image('Assets/Images/Box.png', img_size[0], img_size[1], True)  
        self.rect.size = img_size  

        if pos[0] != None:
            self.rect.top = pos[0]
        if pos[1] != None:
            self.rect.bottom = pos[1]
        if pos[2] != None:
            self.rect.right = pos[2]
        if pos[3] != None:
            self.rect.left = pos[3]
        if pos[4] != None:
            self.rect.centerx = pos[4]
        if pos[5] != None:
            self.rect.centery = pos[5]

        self.data.update(num_size, self.rect.center) 
        
        self.correct_num_color = load_image("Assets/Images/LightGreen.png", self.rect.width/1.5, self.rect.height/1.5)  
        self.correct_num_color_rect = self.correct_num_color.get_rect(center=self.rect.center)  
        self.wrong_num_color = load_image("Assets/Images/LightRed.png", self.rect.width/1.5, self.rect.height/1.5) 
        self.wrong_num_color_rect = self.wrong_num_color.get_rect(center=self.rect.center)  


    def draw(self, surface): #Dibuja la casilla, su color de fondo y número según corresponda
        if self.background_color == 0:  #Si no lleva color de fondo
            surface.blit(self.image, self.rect)  
            self.data.draw(surface)  

        if self.background_color == 1:  #Si se pone color verde de fondo
            surface.blit(self.correct_num_color, self.correct_num_color_rect)  
            surface.blit(self.image, self.rect)  
            self.data.draw(surface)  

        if self.background_color == 2:  #Si se pone color rojo de fondo
            surface.blit(self.wrong_num_color, self.wrong_num_color_rect)  
            surface.blit(self.image, self.rect) 
            self.data.draw(surface)  
#=============================================================================================================#
#                                             *Clase subcuadricula  
#=============================================================================================================#
class subgrid(pygame.sprite.Sprite):  #Se hereda de la clase sprite de pygame para usar los grupos sprite
    def __init__(self, rect_size:tuple, box_size:tuple, num_size:tuple, pos:tuple):
        super().__init__()
        
        #Atributos
        self.complete = False  #Para saber si la subcuadricula está llena
        self.rect = pygame.Rect((0, 0), rect_size)  #Se crea un rectángulo para que se pueda interactuar con la subcuadricula

        #Posición de la subcuadricula (Arriba, Abajo, Derecha, Izquierda, Centro en x, Centro en y)
        if pos[0] != None:
            self.rect.top = pos[0]
        if pos[1] != None:
            self.rect.bottom = pos[1]
        if pos[2] != None:
            self.rect.right = pos[2]
        if pos[3] != None:
            self.rect.left = pos[3]
        if pos[4] != None:
            self.rect.centerx = pos[4]
        if pos[5] != None:
            self.rect.centery = pos[5]

        self.pos_of_boxes = {  #Posición que van a tener cada una de las 9 casillas, dependiendo de las coordenadas del rectángulo de la subcuadricula
                    1: (self.rect.top, None, None, self.rect.left, None, None), #Superior izquierdo 
                    2: (self.rect.top, None, None, None, self.rect.centerx, None), #Superior centrado
                    3: (self.rect.top, None, self.rect.right, None, None, None), #Superior derecho

                    4: (None, None, None, self.rect.left, None, self.rect.centery), #Centro izquierda
                    5: (None, None, None, None, self.rect.centerx, self.rect.centery), #Centro 
                    6: (None, None, self.rect.right, None, None, self.rect.centery), #Centro derecha
                    
                    7: (None, self.rect.bottom, None, self.rect.left, None, None), #Inferior izquierda
                    8: (None, self.rect.bottom, None, None, self.rect.centerx, None), #Inferior centrado
                    9: (None, self.rect.bottom, self.rect.right, None, None, None), #Inferior derecha
                    }

        #Creación de una matriz con todos los objetos casilla
        self.matrix_of_boxes = []
        self.box_group = pygame.sprite.Group()  
        count = 1

        for i in range(3):
            list_of_rows = []  #crea la lista donde guarda cada fila con casillas
            for j in range(3):
                box_ = box(box_size, num_size, self.pos_of_boxes[count]) #crea un objeto casilla y le asigna una posición del diccionario
                list_of_rows.append(box_) 
                self.box_group.add(box_)  
                count += 1
            self.matrix_of_boxes.append(list_of_rows)

    #Métodos
    def get_data(self, x:int, y:int):  #Getter para obtener el dato de la casilla que esta en la matriz
        return self.matrix_of_boxes[x][y].get_data()

    def get_box_group(self):  #Getter para obtener el grupo sprite de casillas
        return self.box_group
        
    def set_data(self, num:int, x:int, y:int, option:int):  #Setter para poner un dato en una casilla de la matriz según la opción
        if option == 1:
            self.matrix_of_boxes[x][y].set_data(num, 1)
        if option == 2:
            self.matrix_of_boxes[x][y].set_data(num, 2)
    
    def update(self, rect_size:tuple, box_size:tuple, num_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.rect.size = rect_size

        if pos[0] != None:
            self.rect.top = pos[0]
        if pos[1] != None:
            self.rect.bottom = pos[1]
        if pos[2] != None:
            self.rect.right = pos[2]
        if pos[3] != None:
            self.rect.left = pos[3]
        if pos[4] != None:
            self.rect.centerx = pos[4]
        if pos[5] != None:
            self.rect.centery = pos[5]

        self.pos_of_boxes.update({
            1: (self.rect.top, None, None, self.rect.left, None, None), #Superior izquierdo 
            2: (self.rect.top, None, None, None, self.rect.centerx, None), #Superior centrado
            3: (self.rect.top, None, self.rect.right, None, None, None), #Superior derecho

            4: (None, None, None, self.rect.left, None, self.rect.centery), #Centro izquierda
            5: (None, None, None, None, self.rect.centerx, self.rect.centery), #Centro 
            6: (None, None, self.rect.right, None, None, self.rect.centery), #Centro derecha
            
            7: (None, self.rect.bottom, None, self.rect.left, None, None), #Inferior izquierda
            8: (None, self.rect.bottom, None, None, self.rect.centerx, None), #Inferior centrado
            9: (None, self.rect.bottom, self.rect.right, None, None, None), #Inferior derecha
        })

        count = 1
        for i in range(3):
            for j in range(3):
                self.matrix_of_boxes[i][j].update(box_size, num_size, self.pos_of_boxes[count])  #Se actualizan los parametros de cada casilla
                count += 1     

    def draw(self, surface):  #Dibuja la subcuadricula, invocando el draw de cada casilla
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        for i in range(3):
            for j in range(3):
                self.matrix_of_boxes[i][j].draw(surface)  #Y después cada casilla
    
    def check_complete(self):  #Revisa si la subcuadricula tiene todas sus casillas llenas
        count = 0
        for box in self.box_group.sprites():
            if box.get_data() != 0:
                count += 1
            else:
                break
        if count == 9:
            self.complete = True
#=============================================================================================================#
#                                                *Clase cuadricula
#=============================================================================================================#
class grid(pygame.sprite.Sprite):  #Se hereda de la clase sprite de pygame para usar los grupos sprite
    def __init__(self, rect_size:tuple, subgrid_size:tuple, box_size:tuple, num_size:tuple, pos:tuple):
        super().__init__()

        self.rect = pygame.Rect((0, 0), rect_size)
        self.rect.center = pos

        self.pos_of_subgrids = {  #Posición que va a tener cada una de las 9 subcuadriculas, dependiendo de las coordenadas del rectángulo de la cuadricula
                    1: (self.rect.top, None, None, self.rect.left, None, None), #Superior izquierdo 
                    2: (self.rect.top, None, None, None, self.rect.centerx, None), #Superior centrado
                    3: (self.rect.top, None, self.rect.right, None, None, None), #Superior derecho

                    4: (None, None, None, self.rect.left, None, self.rect.centery), #Centro izquierda
                    5: (None, None, None, None, self.rect.centerx, self.rect.centery), #Centro 
                    6: (None, None, self.rect.right, None, None, self.rect.centery), #Centro derecha
                    
                    7: (None, self.rect.bottom, None, self.rect.left, None, None), #Inferior izquierda
                    8: (None, self.rect.bottom, None, None, self.rect.centerx, None), #Inferior centrado
                    9: (None, self.rect.bottom, self.rect.right, None, None, None), #Inferior derecha
                    }
        
        self.sudoku = []  #En esta matriz se almacena el sudoku sin resolver
        self.solved_sudoku = []  #En esta matriz se almacena el sudoku resuelto

        #Creación de una matriz con las subcuadriculas
        self.matrix_of_subgrids = []
        self.subgrid_group = pygame.sprite.Group() 
        count = 1

        for i in range(3):
            list_of_rows = []  #Se crea una lista que guarda las rows
            for j in range(3):
                sub = subgrid(subgrid_size, box_size, num_size, self.pos_of_subgrids[count])  #Se crea la subcuadricula con la posición correspondiente
                list_of_rows.append(sub)  
                self.subgrid_group.add(sub)  
                count += 1
            self.matrix_of_subgrids.append(list_of_rows)  

    #Métodos
    def get_data(self, x:int, y:int, xs:int, ys:int):  #Getter que retorna una casilla, dependiendo del indice de la cuadricula y subcuadricula
        return self.matrix_of_subgrids[x][y].get_data(xs, ys)

    def get_subgrid_group(self):  #Getter que retorna el grupo sprite de subcuadriculas
        return self.subgrid_group

    def set_data(self, num:int, x:int, y:int, xs:int, ys:int, option: int):  #Setter que pone un dato en una casilla, dependiendo del indice de la cuadricula, subcuadricula y la opción escogida
        if option == 1:
            self.matrix_of_subgrids[x][y].set_data(num, xs, ys, 1)
        if option == 2:
            self.matrix_of_subgrids[x][y].set_data(num, xs, ys, 2)

    def update(self, rect_size:tuple, subgrid_size:tuple, box_size:tuple, num_size:tuple, pos:tuple):  #Se actualiza el tamaño y la posición
        self.rect.size = rect_size
        self.rect.center = pos  

        self.pos_of_subgrids.update({
            1: (self.rect.top, None, None, self.rect.left, None, None), #Superior izquierdo 
            2: (self.rect.top, None, None, None, self.rect.centerx, None), #Superior centrado
            3: (self.rect.top, None, self.rect.right, None, None, None), #Superior derecho

            4: (None, None, None, self.rect.left, None, self.rect.centery), #Centro izquierda
            5: (None, None, None, None, self.rect.centerx, self.rect.centery), #Centro 
            6: (None, None, self.rect.right, None, None, self.rect.centery), #Centro derecha
            
            7: (None, self.rect.bottom, None, self.rect.left, None, None), #Inferior izquierda
            8: (None, self.rect.bottom, None, None, self.rect.centerx, None), #Inferior centrado
            9: (None, self.rect.bottom, self.rect.right, None, None, None), #Inferior derecha
        })

        count = 1
        for i in range(3):
            for j in range(3):
                (self.matrix_of_subgrids[i][j]).update(subgrid_size, box_size, num_size, self.pos_of_subgrids[count])  #Se actualizan los parametros de cada subcuadricula
                count += 1

    def draw(self, surface): #Dibuja la cuadricula, invocando el draw de cada subcuadricula
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        for i in range(3):
            for j in range(3):
                (self.matrix_of_subgrids[i][j]).draw(surface)  #Y después cada subcuadricula

    def check_complete(self):  #Revisa si el juego ha terminado
        count = 0
        for subgrid in self.subgrid_group.sprites():
            if subgrid.complete == True:
                count += 1
            else:
                break
        if count == 9:
            return True

    #*Logica Sudoku
    def possible_num(self, row, column, num, grid):  #Función que busca si un número ya está en la fila, columna o subcuadricula deseada
        for i in range(0, 9):  #Revisamos toda la fila, y si el número ya está, retorna false
            if grid[row][i] == num:
                return False

        for i in range(0, 9):  #Revisamos toda la columna, y si el número ya está, retorna false
            if grid[i][column] == num:
                return False

        row_sub = (row//3)*3  #Se obtiene la fila inicial de la subcuadricula
        col_sub = (column//3)*3  #Se obtiene la columna inicial de la subcuadricula

        for i in range(0,3):
            for j in range(0,3):
                if grid[row_sub + i][col_sub + j] == num:  #Revisamos la subcuadricula, y si el número ya está, retorna false
                    return False
        return True

    def sudoku_solver(self, grid):
        for row in range(0,9):
            for column in range(0,9):
                if grid[row][column] == 0:  #Si esa casilla esta sin resolver
                    for num in range(1, 10):
                        if(self.possible_num(row, column, num, grid)):  #Si el número es una posible solución
                            grid[row][column] = num
                            posible_result = self.sudoku_solver(grid)  #Se hace la recursión
                            if(type(posible_result) == np.ndarray):  #Si el resultado es una solución valida, devuelve la cuadricula
                                return posible_result
                            else:
                                grid[row][column] = 0  #Sino, se vuelve a buscar
                    return None  #Si ningún número es valido, es porque el resultado no sirve
        return grid

    def generator(self, dificult:int):
        """
        Función encargada de generar un sudoku y llenar las casillas con el dato del sudoku incompleto que se muestra en la ventana, además del dato correcto para su posterior verificación y reiniciar el color de las casillas.
        """
        self.sudoku = np.array(list(str(generators.random_sudoku(avg_rank=dificult)))).reshape(9,9).astype(int)  #Se crea el sudoku en base a un generador
        self.solved_sudoku = self.sudoku_solver(deepcopy(self.sudoku))  #Se hace una copia del sudoku para no modificar la variable original, despúes se usa la función para resolver ese sudoku y se guarda en una variable
        """"
        #Con las variables x, y recorremos la subcuadricula, mientras que con xs y el modulo 3 de c, recorremos las casillas, para que se llene la cuadricula de la misma manera que se recorre la matriz normalmente.
        """
        xs = 0
        x = 0
        y = 0
        for f in range(9):      
            if f <= 2:
                x = 0
            elif 2 < f <= 5:
                x = 1
            elif 5 < f <= 8:
                x = 2
            for c in range(9):
                if c <= 2:
                    y = 0
                elif 2 < c <= 5:
                    y = 1
                elif 5 < c <= 8:
                    y = 2
                self.set_data(self.sudoku[f][c], x, y, xs, c%3, 1)
                self.set_data(self.solved_sudoku[f][c], x, y, xs, c%3, 2)
            if xs == 2:
                xs = 0
            else:
                xs += 1

        for subgrid in self.subgrid_group.sprites():  #Como el juego se reinicia, se regresa a False esta variable
            subgrid.complete = False