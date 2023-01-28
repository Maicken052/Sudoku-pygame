#=============================================================================================================#
#                                                     *librerias      
#=============================================================================================================#
import pygame
from pygame.locals import *
#=============================================================================================================#
#                                          *Función para cargar imagenes      
#=============================================================================================================#
def load_image(filename, width=None, height=None, transparent=False, alpha=False):  #convierte las imagenes a el formato aceptado por pygame y le da las dimensiones deseadas
    try: image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit  #Si la imagen no es valida, muestra un error

    if width != None and height != None:  #Si se coloca un ancho y un alto como parametros, redefine el tamaño de la imagen
        image = pygame.transform.scale(image, (width, height))
    
    if alpha:
        image = image.convert_alpha()  #  Conversión alpha
    else:
        image = image.convert()  #Conversión estandar

    if transparent:  #Quita el fondo a la imagen
        color = pygame.PixelArray(image)
        image.set_colorkey(color[0, 0], RLEACCEL)

    return image
#=============================================================================================================#
#                                                 *Redimensionar    
#=============================================================================================================#
def resize(width, height, design_width, design_height, lifes_text, easy, medium, hard, hint, answer, new_game, game_grid, one, two, three, four, five, six, seven, eight, nine, white_rect_box, go_text, mid_text, excelent_text, second_chance, restart, restart2, flag):
    screen = pygame.display.set_mode((width, height), flag)  
    background_image = load_image("Assets/Images/Background.png", width, height)  
    grid_lines = load_image("Assets/Images/Sudoku_lines.png", width/1.7, height, False, True) 
    win_screen_fade = pygame.Surface((width, height))
    win_screen_fade.fill((135, 206, 235))
    game_over_screen_fade = pygame.Surface((width, height))
    game_over_screen_fade.fill((0, 0, 0))

    #*Actualizar todos los sprites (Se usa la regla de 3 con los tamaños para mantener la proporción)
    #Actualizar textos
    if height < width:  #Condiciones para que los textos no den problemas al cambiar el tamaño de la pantalla
        if width - height <= 270:
            lifes_size = round((width*45)/design_width)
            dificult_size = round((width*28)/design_width)
            go_size = round((width*40)/design_width)
            mid_size = round((width*20)/design_width)
            excelent_size = round((width*100)/design_width)
            text_button_size = round((width*30)/design_width) 
        else:
            lifes_size = round((height*45)/design_height)
            dificult_size = round((height*28)/design_height) 
            go_size = round((height*40)/design_height)
            mid_size = round((height*20)/design_height)
            excelent_size = round((height*100)/design_height)  
            text_button_size = round((height*30)/design_height)       
    else:
        lifes_size = round((width*45)/design_width)
        dificult_size = round((width*28)/design_width)
        go_size = round((width*40)/design_width)
        mid_size = round((width*20)/design_width)
        excelent_size = round((width*100)/design_width)
        text_button_size = round((width*30)/design_width) 

    lifes_text.update(lifes_size, (width/1.65, height/40)) 
    easy.update(dificult_size, (width/1.376, height/1.0698)) 
    medium.update(dificult_size,(width/1.236, height/1.0698)) 
    hard.update(dificult_size, (width/1.0847, height/1.0698)) 

    #Actualizar botones
    buttons_width = (width*200)/design_width  
    buttons_height = (height*79)/design_height
    buttons_height = (height*79)/design_height 
    new_game_width = (width*160)/design_width
    new_game_height = (height*46)/design_height  
    hint.update((buttons_width, buttons_height), (width/1.6, height/8))  
    answer.update((buttons_width, buttons_height), (width/1.2367, height/8))  
    new_game.update((new_game_width, new_game_height), (width/1.69, height/1.0827)) 

    #Actualizar botones numericos
    buttons_size = ((width*140)/design_width, (height*140)/design_height)  
    first_xpos =  width/1.590062111801243
    first_ypos = height/3.42857142857143 
    second_xpos = width/1.354497354497355 
    second_ypos = height/2.057142857142855  
    third_xpos = width/1.17972350230415 
    third_ypos = height/1.46938775510204 
    one.update(buttons_size, (first_xpos, first_ypos))
    two.update(buttons_size, (second_xpos, first_ypos))
    three.update(buttons_size, (third_xpos, first_ypos))
    four.update(buttons_size, (first_xpos, second_ypos))
    five.update(buttons_size, (second_xpos, second_ypos))
    six.update(buttons_size, (third_xpos, second_ypos))
    seven.update(buttons_size, (first_xpos, third_ypos))
    eight.update(buttons_size, (second_xpos, third_ypos))
    nine.update(buttons_size, (third_xpos, third_ypos))

    #Actualizar la cuadricula
    grid_size = ((width*693)/design_width, (height*664)/design_height)
    subgrid_size = ((width*211)/design_width, (height*203)/design_height)
    box_size = ((width*69)/design_width, (height*66)/design_height)
    num_size = ((width*25)/design_width, (height*25)/design_height)
    pos = ((width/1.7)/2, height/2)
    game_grid.update(grid_size, subgrid_size, box_size, num_size, pos)
    
    #Actualizar elementos de pantallas finales
    white_box_size = ((width*500)/design_width, (height*360)/design_height)
    white_box_center = (width/2, height/2)
    white_rect_box.size = white_box_size
    white_rect_box.center = white_box_center
    button_size = ((width*350)/design_width, (height*60)/design_height)
    elevation = round((height*6)/design_height) 
    go_text.update(go_size, (0, 0))
    mid_text.update(mid_size, (0, 0)) 
    excelent_text.update(excelent_size, (0, 0)) 
    go_text.rect.center = (width/2, height/3.1304347826087)
    mid_text.rect.center = (width/2, height/2.482758620689655)
    excelent_text.rect.center = (width/2, height/2.482758620689655)
    second_chance.update(text_button_size, button_size, (width/2, height/1.945945945945945), elevation)
    restart.update(text_button_size, button_size, (width/2, height/1.6), elevation)
    restart2.update(text_button_size, button_size, (width/2, height/1.6), elevation)

    return screen, background_image, grid_lines, buttons_size, buttons_width, buttons_height, new_game_width, new_game_height, dificult_size, win_screen_fade, game_over_screen_fade
#=============================================================================================================#
#                                                 *Reiniciar juego    
#=============================================================================================================#
def restart_game(game_grid, dificult:int):
    game_grid.generator(dificult)  #Generamos una nueva partida con su respectiva dificultad
    lifes = 5  #Reiniciamos las vidas
    put_hint = False  #Quitamos las pistas en caso de que estuvieran activas
    number_obtained = 0  #Quitamos los números obtenidos
    return lifes, put_hint, number_obtained
#=============================================================================================================#
#                                        *Redibujar los elementos del juego 
#=============================================================================================================#
def redraw(screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard):
    screen.blit(background_image, (0, 0))  
    game_grid.draw(screen)  
    screen.blit(grid_lines, (0, 0))  
    lifes_text.draw(screen)  
    hint.draw(screen)  
    answer.draw(screen) 
    button_numbers_group.draw(screen)  
    new_game.draw(screen)  
    easy.draw(screen) 
    medium.draw(screen) 
    hard.draw(screen)  
#=============================================================================================================#
#                                                   *Fade in 
#=============================================================================================================#
def fade_in(screen_fade, range_, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard):
    for alpha in range(0, range_):
        screen_fade.set_alpha(alpha)  #Se va ajustando la transparencia de la superficie
        redraw(screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
        screen.blit(screen_fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)
#=============================================================================================================#
#                                                   *Fade out 
#=============================================================================================================#
def fade_out(screen_fade, range_, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard):
    fade_out_ = range_
    for alpha in range(0, range_):
        fade_out_ -= 1
        screen_fade.set_alpha(fade_out_)  #Se va ajustando la transparencia de la superficie
        redraw(screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
        screen.blit(screen_fade, (0, 0))
        pygame.display.update()