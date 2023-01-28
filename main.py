#=============================================================================================================#     
#                                                    *librerias      
#=============================================================================================================#
import pygame, sys, threading
from pygame.locals import *
from functions import load_image, resize, restart_game, redraw, fade_in, fade_out
from Grid_sprites import grid
from Buttons_sprites import number_buttons, actions_buttons, animated_button, word
from Loading_screen import loading_screen
#=============================================================================================================#     
#                                                  *Colores usados 
#=============================================================================================================#
RED_1 = (213, 57, 48)  
GREEN = (18, 247, 51)  
ORANGE = (255, 129, 0) 
RED_2 = (255, 17, 0) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
GREY = (169, 169, 169)  
DARK_GREY = (50, 50, 50)  
BLUE = (0, 96, 255)
DARK_BLUE = (0, 64, 255)
FADE_BLUE = (8, 100, 204)
SKY_BLUE = (135, 206, 235)
#=============================================================================================================#     
#                                                       *Main         
#=============================================================================================================#
def main():
    game = True  
    FPS = 60
    clicked = False

    #Config para el fullscreen
    screen_info = pygame.display.Info()  #Información de la pantalla en la que se esta corriendo el juego
    WIDTH = screen_info.current_w 
    HEIGHT = screen_info.current_h 
    fullscreen = False  
    #Config de la ventana
    design_width = 1280  #Ancho base para el que fue diseñado el juego
    design_height = 720  #Alto base para el que fue diseñado el juego
    screen = pygame.display.set_mode((design_width, design_height), pygame.RESIZABLE)  
    clock = pygame.time.Clock()  
    background_image = load_image("Assets/Images/Background.png", design_width, design_height)   
    icon = load_image("Assets/Images/Icon.png")  
    pygame.display.set_caption('Sudoku')  
    pygame.display.set_icon(icon)

    #Variables que se usan en el juego (se usa el global 2 veces dado que estan en una función anidada)
    global lifes, lifes_text, dificult_size, easy, medium, hard, dificult, buttons_width, buttons_height, hint, put_hint, answered, answer, new_game_width, new_game_height, new_game, button_numbers_group, buttons_size, one, two, three, four, five, six, seven, eight, nine, number_obtained, pressed_button, game_grid, subgrid_group, grid_lines, game_over_screen_fade, win_screen_fade, white_rect_box, go_text, mid_text, second_chance, restart, excelent_text, restart2, repeat, correct_num_sound, wrong_num_sound, number_sound, hint_sound, answer_sound, dificult_sound, win_sound, go_sound, finish
    
    #Pantalla de carga
    load_screen = loading_screen()
    finish = False  #Se usa para finalizar la pantalla de carga

    #Cargar todo lo que se usa en el juego
    def load_items():
        global lifes, lifes_text, dificult_size, easy, medium, hard, dificult, buttons_width, buttons_height, hint, put_hint, answered, answer, new_game_width, new_game_height, new_game, button_numbers_group, buttons_size, one, two, three, four, five, six, seven, eight, nine, number_obtained, pressed_button, game_grid, subgrid_group, grid_lines, game_over_screen_fade, win_screen_fade, white_rect_box, go_text, mid_text, second_chance, restart, excelent_text, restart2, repeat, correct_num_sound, wrong_num_sound, number_sound, hint_sound, answer_sound, dificult_sound, win_sound, go_sound, finish

        #Texto de las vidas
        lifes = 5  
        lifes_text = word(f"Lifes: {lifes}", 45, RED_1, (775, 18))  

        #Dificultades
        dificult = 50
        dificult_size = 28 
        easy = word(f"easy", dificult_size, GREEN, (930, 673))  
        medium = word(f"medium", dificult_size, GREY, (1035, 673))  
        hard = word(f"hard", dificult_size, GREY, (1180, 673))   

        #Botones de acciones (Pista, Solución y juego nuevo)
        buttons_width = 200  
        buttons_height = 79 
        new_game_width = 160  
        new_game_height = 46  
        hint = actions_buttons('Assets/Images/HintButton.png', (buttons_width, buttons_height), (800, 90))  
        answer = actions_buttons('Assets/Images/AnswerButton.png', (buttons_width, buttons_height), (1035, 90))  
        new_game = actions_buttons('Assets/Images/NewGameButton.png', (new_game_width, new_game_height), (757, 665))  
        put_hint = False 
        answered = False
        
        #Config de los botones númericos
        buttons_size = (140, 140)  
        first_xpos = 805 
        first_ypos = 210 
        second_xpos = 945 
        second_ypos = 350  
        third_xpos = 1085
        third_ypos = 490 
        one = number_buttons('Assets/Images/One.png', buttons_size, (first_xpos, first_ypos), 1)  
        two = number_buttons('Assets/Images/Two.png', buttons_size, (second_xpos, first_ypos), 2)  
        three = number_buttons('Assets/Images/Three.png', buttons_size, (third_xpos, first_ypos), 3)  
        four = number_buttons('Assets/Images/Four.png', buttons_size, (first_xpos, second_ypos), 4)  
        five = number_buttons('Assets/Images/Five.png', buttons_size, (second_xpos, second_ypos), 5)  
        six = number_buttons('Assets/Images/Six.png', buttons_size, (third_xpos, second_ypos), 6)  
        seven = number_buttons('Assets/Images/Seven.png', buttons_size, (first_xpos, third_ypos), 7)  
        eight = number_buttons('Assets/Images/Eight.png', buttons_size, (second_xpos, third_ypos), 8)  
        nine = number_buttons('Assets/Images/Nine.png', buttons_size, (third_xpos, third_ypos), 9) 
        button_numbers_group = pygame.sprite.Group()  
        button_numbers_group.add(one)
        button_numbers_group.add(two)
        button_numbers_group.add(three)
        button_numbers_group.add(four)
        button_numbers_group.add(five)
        button_numbers_group.add(six)
        button_numbers_group.add(seven)
        button_numbers_group.add(eight)
        button_numbers_group.add(nine)
        number_obtained = 0
        pressed_button = None

        #Crear una cuadricula y generar un sudoku
        grid_size = (693, 664)  
        subgrid_size = (211,203)  
        box_size = (69, 66)  
        num_size = (25, 25)  
        game_grid = grid(grid_size, subgrid_size, box_size, num_size, (377, 360))  
        grid_lines = load_image("Assets/Images/Sudoku_lines.png",753, 720, False, True) 
        game_grid.generator(dificult)  
        subgrid_group = game_grid.get_subgrid_group() 

        #Pantalla de derrota
        game_over_screen_fade = pygame.Surface((design_width, design_height))
        game_over_screen_fade.fill(BLACK)
        white_rect_box = pygame.Rect(0, 0, 500, 360)
        white_rect_box.center = (640, 360)
        go_text = word("game over", 40, DARK_GREY, ((0, 0)))
        mid_text = word(f"you lost all your lives", 20, GREY, ((0, 0)))
        go_text.rect.center = (640, 230)
        mid_text.rect.center = (640, 290)
        second_chance = animated_button("second chance", 30, (350, 60), (640, 370), 6, BLUE, DARK_BLUE, WHITE)
        restart = animated_button("restart", 30, (350, 60), (640, 450), 6, BLUE, DARK_BLUE, WHITE)

        #Pantalla de victoria
        win_screen_fade = pygame.Surface((design_width, design_height))
        win_screen_fade.fill(SKY_BLUE)
        excelent_text = word("excelent!",100, WHITE, ((0, 0)))
        excelent_text.rect.center = (640, 230)
        restart2 = animated_button("restart", 30, (350, 60), (640, 450), 6, WHITE, DARK_GREY, DARK_GREY)
        repeat = False

        #Efectos de sonido
        correct_num_sound = pygame.mixer.Sound("Assets/Sfx/correct_num.wav")
        wrong_num_sound = pygame.mixer.Sound("Assets/Sfx/wrong_num.wav")
        number_sound = pygame.mixer.Sound("Assets/Sfx/number_click.wav")
        hint_sound = pygame.mixer.Sound("Assets/Sfx/hint_click.wav")
        answer_sound = pygame.mixer.Sound("Assets/Sfx/answer_click.wav")
        dificult_sound = pygame.mixer.Sound("Assets/Sfx/dificult_click.wav")
        win_sound = pygame.mixer.Sound("Assets/Sfx/win.wav")
        go_sound = pygame.mixer.Sound("Assets/Sfx/game_over.wav")

        #Finaliza la carga del juego
        finish = True
        pygame.mixer.fadeout(1000)

    #Empezamos a cargar el juego, mientras se corre la pantalla de carga
    threading.Thread(target = load_items).start()

    #*Ciclo while del juego
    while game:
        clock.tick(FPS)  #Fotogramas por segundo
        screen.fill(WHITE)  #Cambio de fotograma

        if not finish:
            load_screen.run(screen)  #Correr la pantalla de carga
        else:
            #Colocar todos los elementos en la ventana
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

            #Detectar las entradas del teclado o ratón
            for event in pygame.event.get():  
                if event.type == QUIT:  #Si se presiona el boton con la X roja
                    pygame.quit()
                    sys.exit(0)

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  #Si se presiona la tecla escape
                        sys.exit(0)

                    if event.key == K_f:  #Si se presiona la tecla f, se pone o se quita pantalla completa
                        fullscreen = not fullscreen
                        if fullscreen:  
                            screen, background_image, grid_lines, buttons_size, buttons_width, buttons_height, new_game_width, new_game_height, dificult_size, win_screen_fade, game_over_screen_fade = resize(WIDTH, HEIGHT, design_width, design_height, lifes_text, easy, medium, hard, hint, answer, new_game, game_grid, one, two, three, four, five, six, seven, eight, nine, white_rect_box, go_text, mid_text, excelent_text, second_chance, restart, restart2, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((design_width, design_height), pygame.RESIZABLE)  #Si se quita la pantalla completa, se deja todo como estaba antes

                if event.type == VIDEORESIZE:  #Acomodar el tamaño de la ventana (event.w y event.h son las dimensiones actuales de la pantalla)
                    if not fullscreen:
                        screen, background_image, grid_lines, buttons_size, buttons_width, buttons_height, new_game_width, new_game_height, dificult_size, win_screen_fade, game_over_screen_fade = resize(event.w, event.h, design_width, design_height, lifes_text, easy, medium, hard, hint, answer, new_game, game_grid, one, two, three, four, five, six, seven, eight, nine, white_rect_box, go_text, mid_text, excelent_text, second_chance, restart, restart2, pygame.RESIZABLE)

                if event.type == MOUSEBUTTONDOWN and event.button == 1:  #Si se oprime el click izquierdo
                    clicked = True
            
            #Pantalla de derrota
            if lifes <= 0:  
                if not repeat: 
                    #Se hace el efecto fade
                    go_sound.play()
                    fade_in(game_over_screen_fade, 160, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
                    repeat = True
                else:  
                    game_over_screen_fade.set_alpha(160)
                    screen.blit(game_over_screen_fade, (0, 0))
                    pygame.draw.rect(screen, WHITE, white_rect_box, border_radius=12)
                    go_text.draw(screen)
                    mid_text.draw(screen)
                    second_chance.draw(screen)
                    restart.draw(screen)

                    #Salir de la pantalla final
                    if second_chance.check_click(BLUE, FADE_BLUE):
                        fade_out(game_over_screen_fade, 160, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
                        lifes = 1
                        repeat = False
                        second_chance.action = False
                        clicked = False

                    if restart.check_click(BLUE, FADE_BLUE):
                        lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                        fade_out(game_over_screen_fade, 160, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
                        number_buttons.check_if_pressed(pressed_button, buttons_size)
                        pressed_button = None
                        repeat = False
                        restart.action = False
                        clicked = False
            else:
                #Pantalla de victoria
                if game_grid.check_complete(): 
                    if not repeat: 
                        #Se hace el efecto fade
                        pygame.time.delay(400)
                        win_sound.play()
                        fade_in(win_screen_fade, 255, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
                        repeat = True
                    else:  
                        win_screen_fade.set_alpha(255)
                        screen.blit(win_screen_fade, (0, 0))
                        excelent_text.draw(screen)
                        restart2.draw(screen)

                        #Salir de la pantalla final
                        if restart2.check_click(WHITE, GREY):
                            lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                            fade_out(win_screen_fade, 255, screen, background_image, grid_lines, game_grid, lifes_text, hint, answer, button_numbers_group, new_game, easy, medium, hard)
                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                            pressed_button = None
                            repeat = False
                            restart2.action = False
                            clicked = False  
                else:
                    #Fluidez de los botones
                    if not answered:
                        if not put_hint:
                            for pulsed_button in button_numbers_group.sprites(): 
                                if  pulsed_button != pressed_button:
                                        pulsed_button.smoothness(buttons_size)
                            hint.smoothness((buttons_width, buttons_height))
                            answer.smoothness((buttons_width, buttons_height))

                    new_game.smoothness((new_game_width, new_game_height))
                    easy.smoothness(dificult_size)
                    medium.smoothness(dificult_size)
                    hard.smoothness(dificult_size)
                    
                    if answered:  #Delay para que se vea la animación del click
                        pygame.time.delay(100)
                        answer.click((buttons_width, buttons_height))

                    if clicked:    
                        clicked = False

                        #Se revisan los botones numericos en caso de que se haya hecho click sobre uno de ellos
                        if not answered:
                            if not put_hint:
                                for pulsed_button in button_numbers_group.sprites(): 
                                    if pulsed_button.rect.collidepoint(pygame.mouse.get_pos()):  
                                        number_buttons.check_if_pressed(pressed_button, buttons_size)  #Revisa si hay alguno oprimido para volverlo a su estado normal
                                        pulsed_button.click((buttons_size[0]*0.90, buttons_size[1]*0.90))  #Oprime el botón sobre el que se hizo click izquierdo
                                        number_sound.play()
                                        pressed_button = pulsed_button  #Se guarda el botón pulsado
                                        number_obtained = pulsed_button.get_number()  #Se guarda el valor obtenido del botón
                                        break
                                
                        #Se revisa la cuadricula en caso de que se haya hecho click en una casilla
                        for subgrid in subgrid_group.sprites():  
                            if subgrid.rect.collidepoint(pygame.mouse.get_pos()):  #Se revisan las subcuadriculas
                                box_group = subgrid.get_box_group()  
                                for box in box_group.sprites():  
                                    if box.rect.collidepoint(pygame.mouse.get_pos()):  #Después cada casilla de la subcuadricula  
                                        if put_hint:  #Si el botón de pista esta activo
                                            if box.get_data() == 0:  #Si la casilla está sin resolver
                                                box.set_data(box.get_correct_number(), 1, 1)  #Se pone el número correcto y se pone el fondo verde
                                                correct_num_sound.play()
                                                put_hint = False 
                                                subgrid.check_complete()  #Revisa si la subcuadricula está llena
                                                break

                                        if number_obtained != 0 and box.get_data() == 0:  #si se obtuvo un número del botón y la casilla no tiene número
                                            if box.get_correct_number() == number_obtained:  #Si el número que se va a colocar en la casilla es correcto
                                                box.set_data(number_obtained, 1, 1)  
                                                correct_num_sound.play()
                                                subgrid.check_complete()  #Revisa si la subcuadriculo está llena
                                            else:
                                                box.set_data(number_obtained, 1, 2) 
                                                wrong_num_sound.play()
                                                lifes -= 1  

                                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                                            pressed_button = None
                                            number_obtained = 0  #Se reinicia el número que estaba oprimido
                        
                        #Si se oprime el botón de pista
                        if hint.rect.collidepoint(pygame.mouse.get_pos()):  
                            if not put_hint:
                                if not answered:
                                    hint.click((buttons_width*0.90, buttons_height*0.90))
                                    hint_sound.play()
                                    put_hint = True  
                                    number_buttons.check_if_pressed(pressed_button, buttons_size)
                                    pressed_button = None
                                    number_obtained = 0  
                        
                        #Si se oprime el botón de resolver
                        if answer.rect.collidepoint(pygame.mouse.get_pos()):  
                            if not put_hint:
                                if not answered:
                                    answer.click((buttons_width*0.85, buttons_height*0.85))
                                    answer_sound.play()
                                    answered = True
                                    for subgrid in subgrid_group.sprites():  
                                        box_group = subgrid.get_box_group() 
                                        for box in box_group.sprites():  
                                            if box.get_data() == 0:  #Si aún no tiene dato la casilla
                                                box.set_data(box.get_correct_number(), 1, 1)  #Se coloca el dato resuelto y el fondo verde
                            
                        #Si se oprime el boton de juego nuevo
                        if new_game.rect.collidepoint(pygame.mouse.get_pos()):  
                            new_game.click((new_game_width*0.85, new_game_height*0.85))
                            dificult_sound.play()
                            lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                            pressed_button = None
                            answered = False

                        #Si se cambia a la dificultad facil
                        if easy.rect.collidepoint(pygame.mouse.get_pos()):  
                            easy.click(round(dificult_size*0.80))
                            dificult_sound.play()
                            easy.color_ = GREEN  #Se pone en color solo el botón de easy
                            medium.color_ = GREY
                            hard.color_ = GREY
                            dificult = 50
                            lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                            pressed_button = None
                            answered = False

                        #Si se cambia a la dificultad medio
                        if medium.rect.collidepoint(pygame.mouse.get_pos()):  
                            medium.click(round(dificult_size*0.80))
                            dificult_sound.play()
                            easy.color_ = GREY
                            medium.color_ = ORANGE  #Se pone en color solo el botón de medium
                            hard.color_ = GREY
                            dificult = 100 
                            lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                            pressed_button = None
                            answered = False
                        
                        #Si se cambia a la dificultad dificil
                        if hard.rect.collidepoint(pygame.mouse.get_pos()):  
                            hard.click(round(dificult_size*0.80))
                            dificult_sound.play()
                            easy.color_ = GREY
                            medium.color_ = GREY
                            hard.color_ = RED_2  #Se pone en color solo el botón de hard
                            dificult = 150 
                            lifes, put_hint, number_obtained = restart_game(game_grid, dificult)
                            number_buttons.check_if_pressed(pressed_button, buttons_size)
                            pressed_button = None
                            answered = False
                        
            lifes_text.text_ = f"lifes: {lifes}"  #Se actualizan las vidas
                        
        pygame.display.update() #Actualizar contenido en pantalla

if __name__ == '__main__':
    pygame.init()
    main()