import pygame
import sys
from ball import Balon
from player import Player
from scoreboard import Scoreboard
from power_bar import PowerBar
from clock import Clock

class Field:
    def __init__(self, width=920, height=586, title="Barracuda King"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.color1 = (255,0,0)
        self.color2 = (0,0,255)
        self.balon = Balon((255,0,0),10,"cuero",460,293,2,3)
        self.background = pygame.image.load("C:/Users/Juegos/Documents/barracuda_game/assets/field_image.png").convert_alpha()
        self.keys_pressed = set()


        self.zonas_prohibidas = [
            pygame.Rect(0, 0, 920, 20),
            pygame.Rect(0, 20, 36, 200),
            pygame.Rect(0, 372, 36, 280),
            pygame.Rect(0,560,920,20),
            pygame.Rect(884,20,36,200),
            pygame.Rect(884,370,36,280)
        ]

        self.zonas_gol = [
            pygame.Rect(0,221,36,150),
            pygame.Rect(884,221,36,150)
        ]

        self.controles_jugador1 = {'arriba': pygame.K_w, 'abajo': pygame.K_s, 'izquierda': pygame.K_a, 'derecha': pygame.K_d,'tiro':pygame.K_x,'habilidad-ataque':pygame.K_q,'habilidad-defensa':pygame.K_e}
        self.controles_jugador2 = {'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN, 'izquierda': pygame.K_LEFT, 'derecha': pygame.K_RIGHT,'tiro':pygame.K_SPACE,'habilidad-ataque':pygame.K_m,'habilidad-defensa':pygame.K_n}

        self.jugadores_equipo1 = [
            Player(100,221,1,20),
            Player(100,381,1,12),
            Player(320,221,1,16),
            Player(320,381,1,18)]

        self.jugadores_equipo2 = [
            Player(600,221,2,17),
            Player(600,381,2,16),
            Player(820,221,2,15),
            Player(820,381,2,13)]

        self.jugador_seleccionado_1 = 0
        self.jugador_seleccionado_2 = 0

        self.marcador = Scoreboard(tamano_fuente=40,posicion=(0,10))
        self.barra_poder_1 = PowerBar(x=10, y=65)
        self.barra_poder_2 = PowerBar(x=890,y=60)
        self.game_clock = Clock()

        self.poder_ataque_activo_1 = False
        self.poder_defensa_activo_1 = False
        self.poder_ataque_activo_2 = False
        self.poder_defensa_activo_2 = False 
        self.tiempo_poder_1 = 0
        self.tiempo_poder_2 = 0
        self.incremento_barra = 1
        self.poder_activo = False
        self.score_equipo1 = 0
        self.score_equipo2 = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)

                if event.key == pygame.K_TAB:
                    self.jugador_seleccionado_1 = (self.jugador_seleccionado_1 + 1) % len(self.jugadores_equipo1)
                if event.key == pygame.K_RETURN:
                    self.jugador_seleccionado_2 = (self.jugador_seleccionado_2 + 1) % len(self.jugadores_equipo2)

                jugador1 = self.jugadores_equipo1[self.jugador_seleccionado_1]
                jugador2 = self.jugadores_equipo2[self.jugador_seleccionado_2]

                # Disparo jugador 1
                if event.key == self.controles_jugador1['tiro']:
                    offset_x = int(self.balon.rect_normal.x - jugador1.rect.x)
                    offset_y = int(self.balon.rect_normal.y - jugador1.rect.y)
                    if jugador1.mascara.overlap(self.balon.mascara, (offset_x, offset_y)):
                        jugador1.shoot(self.balon)

                # Disparo jugador 2
                if event.key == self.controles_jugador2['tiro']:
                    offset_x = int(self.balon.rect_normal.x - jugador2.rect.x)
                    offset_y = int(self.balon.rect_normal.y - jugador2.rect.y)
                    if jugador2.mascara.overlap(self.balon.mascara, (offset_x, offset_y)):
                        jugador2.shoot(self.balon)

                # Poder de ataque jugador 1 (si defensa de jugador 2 no está activa)
                if event.key == self.controles_jugador1['habilidad-ataque'] and not self.poder_defensa_activo_2:
                    if self.barra_poder_1.disminuir_poder(jugador1.costo_tiro, True):
                        self.poder_ataque_activo_1 = True
                        self.poder_ataque_activo_2 = False
                        self.poder_defensa_activo_2 = False

                # Poder de ataque jugador 2 (si defensa de jugador 1 no está activa)
                if event.key == self.controles_jugador2['habilidad-ataque'] and not self.poder_defensa_activo_1:
                    if self.barra_poder_2.disminuir_poder(jugador2.costo_tiro, True):
                        self.poder_ataque_activo_2 = True
                        self.poder_ataque_activo_1 = False
                        self.poder_defensa_activo_1 = False

                # Poder de defensa jugador 1 (si jugador 2 tiene ataque activo)
                if event.key == self.controles_jugador1['habilidad-defensa'] and self.poder_ataque_activo_2:
                    if self.barra_poder_1.disminuir_poder(jugador1.costo_defensa,True):
                        self.poder_defensa_activo_1 = True
                        self.poder_ataque_activo_2 = False

                # Poder de defensa jugador 2 (si jugador 1 tiene ataque activo)
                if event.key == self.controles_jugador2['habilidad-defensa'] and self.poder_ataque_activo_1:
                    if self.barra_poder_2.disminuir_poder(jugador2.costo_defensa,True):
                        self.poder_defensa_activo_2 = True
                        self.poder_ataque_activo_1 = False

    def update(self):
        teclas = pygame.key.get_pressed()
        jugador1 = self.jugadores_equipo1[self.jugador_seleccionado_1]
        jugador2 = self.jugadores_equipo2[self.jugador_seleccionado_2]

        jugador1.barra_vida.x = jugador1.x
        jugador1.barra_vida.y = jugador1.y + 20

        jugador2.barra_vida.x = jugador2.x
        jugador2.barra_vida.y = jugador2.y + 20

        if (not self.poder_ataque_activo_1 and not self.poder_ataque_activo_2 and not self.poder_defensa_activo_1 and not self.poder_defensa_activo_2):
            for jugador in self.jugadores_equipo1 + self.jugadores_equipo2:
                jugador.colision_activa = False


        prev_x1, prev_y1 = jugador1.x, jugador1.y
        prev_x2, prev_y2 = jugador2.x, jugador2.y

        self.actualizar_barra_vida()
        jugador1.mover(teclas, self.controles_jugador1)
        jugador2.mover(teclas, self.controles_jugador2)
        self.balon.mover(self.width, self.height)
        #jugador1.colisiona_con_balon(self.balon,self.colision_activa)
        #jugador2.colisiona_con_balon(self.balon,self.colision_activa)
        self.barra_poder_1.aumentar_poder(0.05 * self.incremento_barra)
        self.barra_poder_2.aumentar_poder(0.05 * self.incremento_barra)
        self.actualizar_tiempo()

        for jugador in self.jugadores_equipo1 + self.jugadores_equipo2:
            jugador.colisiona_con_balon(self.balon)

        for zona in self.zonas_prohibidas:
            # Balón y zonas
            if self.balon.rect_normal.colliderect(zona):
                if abs(self.balon.rect_normal.right - zona.left) < 10 or abs(self.balon.rect_normal.left - zona.right) < 10:
                    self.balon.vx = -self.balon.vx
                    self.balon.x += self.balon.vx
                    self.balon.rect_normal.move_ip(self.balon.vx * 2, 0)
                if abs(self.balon.rect_normal.bottom - zona.top) < 10 or abs(self.balon.rect_normal.top - zona.bottom) < 10:
                    self.balon.vy = -self.balon.vy
                    self.balon.y += self.balon.vy
                    self.balon.rect_normal.move_ip(self.balon.vy * 2, 0)

            if zona.contains(self.balon.rect_normal):
                self.balon.x = self.width // 2
                self.balon.y = self.height // 2
                self.balon.actualizar_rects()

            # Jugador 1 y zonas
            if jugador1.rect.colliderect(zona):
                jugador1.x = prev_x1
                jugador1.y = prev_y1
                jugador1.actualizar_rect()

            # Jugador 2 y zonas
            if jugador2.rect.colliderect(zona):
                jugador2.x = prev_x2
                jugador2.y = prev_y2
                jugador2.actualizar_rect()

        for zona_gol in self.zonas_gol:
            if zona_gol.contains(self.balon.rect_normal):
                jugador1.tiro_activo = False
                jugador2.tiro_activo = False
                if zona_gol == self.zonas_gol[0]:
                    self.marcador.aumentar_score(2)
                    self.reiniciar_posiciones
                    self.score_equipo2 += 5

                    if self.tiempo_poder_2 > 0:
                        self.incremento_barra = 3
                else:
                    if self.tiempo_poder_1 > 0:
                        self.incremento_barra = 3
                    self.marcador.aumentar_score(1)
                    self.reiniciar_posiciones
                    self.score_equipo1 += 5

                self.balon.x = self.width // 2
                self.balon.y = self.height // 2
                self.balon.vx = -self.balon.vx
                self.balon.vy = -self.balon.vy
                self.balon.actualizar_rects()

            if jugador1.rect.colliderect(zona_gol):
                jugador1.x = prev_x1
                jugador1.y = prev_y1
                jugador1.actualizar_rect()

            if jugador2.rect.colliderect(zona_gol):
                jugador2.x = prev_x2
                jugador2.y = prev_y2
                jugador2.actualizar_rect()

    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.marcador.dibujar(self.screen)
        self.game_clock.draw(self.screen)
        self.barra_poder_1.dibujar(self.screen)
        self.barra_poder_2.dibujar(self.screen)
        
            # Dibujar poder defensivo activo como rectángulo (visualización provisional)
        for zona in self.zonas_gol:
            pygame.draw.rect(self.screen,(255,255,255),zona)

        self.balon.dibujar(self.screen)

        for jugador in self.jugadores_equipo1 + self.jugadores_equipo2:
            jugador.barra_vida.draw(self.screen)
            jugador.dibujar(self.screen)

        self.dibujar_rectangulos()
        pygame.display.flip()

    def actualizar_tiempo(self):
        if self.poder_ataque_activo_1:
            self.balon.color = (0, 255, 0)
            self.tiempo_poder_1 += 1
            if self.tiempo_poder_1 >= 420:
                self.tiempo_poder_1 = 0
                self.poder_ataque_activo_1 = False

        if self.poder_defensa_activo_1:
            self.tiempo_poder_1 += 1
            if self.tiempo_poder_1 >= 420:
                self.tiempo_poder_1 = 0
                self.poder_defensa_activo_1 = False

        if self.poder_defensa_activo_2:
            self.tiempo_poder_2 += 1
            if self.tiempo_poder_2 >= 420:
                self.tiempo_poder_2 = 0
                self.poder_defensa_activo_2 = False

        if self.poder_ataque_activo_2:
            self.balon.color = (0, 255, 0)
            self.tiempo_poder_2 += 1
            if self.tiempo_poder_2 >= 420:
                self.tiempo_poder_2 = 0
                self.poder_ataque_activo_2 = False

        # Si ninguno está activo, se resetea el estado del balón
        if not self.poder_ataque_activo_1 and not self.poder_ataque_activo_2:
            self.balon.color = (255, 0, 0)
            self.incremento_barra = 1
            self.poder_activo = False
    
    def dibujar_rectangulos(self):
        pygame.draw.rect(self.screen, (0, 0, 255), (self.jugadores_equipo1[self.jugador_seleccionado_1].x-25,
                                                    self.jugadores_equipo1[self.jugador_seleccionado_1].y-25,
                                                    20,20)) 
         
        pygame.draw.rect(self.screen, (255, 0, 0), (self.jugadores_equipo2[self.jugador_seleccionado_2].x-25,
                                                    self.jugadores_equipo2[self.jugador_seleccionado_2].y-25,
                                                    20, 20))
     
        if self.poder_defensa_activo_1:
            pygame.draw.rect(self.screen, (0, 255, 255), (self.jugadores_equipo1[self.jugador_seleccionado_1].x-25,
                                                        self.jugadores_equipo1[self.jugador_seleccionado_1].y-25,
                                                        50,50),3)                                         
        if self.poder_defensa_activo_2:
            pygame.draw.rect(self.screen, (255, 255, 0), (self.jugadores_equipo2[self.jugador_seleccionado_2].x-25,
                                                        self.jugadores_equipo2[self.jugador_seleccionado_2].y-25,
                                                      50, 50), 3)

    def actualizar_barra_vida(self):
        jugador1 = self.jugadores_equipo1[self.jugador_seleccionado_1]
        jugador2 = self.jugadores_equipo2[self.jugador_seleccionado_2]

        for jugador in self.jugadores_equipo2:    
            if jugador.colision_activa and self.poder_ataque_activo_1:
                jugador.barra_vida.set_health(jugador2.dano_tiro)
                self.score_equipo1 += 3
                jugador.colision_activa = False

        for jugador in self.jugadores_equipo1:  
            if jugador.colision_activa and self.poder_ataque_activo_2:
                jugador.barra_vida.set_health(jugador1.dano_tiro)
                self.score_equipo1 += 3
                jugador.colision_activa = False

    def reset_juego(self):
        if self.game_clock.get_elapsed_time == 300000:
            self.game_clock.reset
        for jugador in self.jugadores_equipo1:
            jugador.barra_vida.current_health     

    def reiniciar_posiciones(self):
        self.jugadores_equipo1[0].x = 100
        self.jugadores_equipo1[0].y = 221
        self.jugadores_equipo1[1].x = 100
        self.jugadores_equipo1[1].y = 381
        self.jugadores_equipo1[2].x = 320
        self.jugadores_equipo1[2].y = 221
        self.jugadores_equipo1[3].x = 320
        self.jugadores_equipo1[3].y = 381
        self.jugadores_equipo2[0].x = 600
        self.jugadores_equipo2[0].y = 221
        self.jugadores_equipo2[1].x = 600
        self.jugadores_equipo2[1].y = 381
        self.jugadores_equipo2[2].x = 820
        self.jugadores_equipo2[2].y = 221
        self.jugadores_equipo2[3].x = 820
        self.jugadores_equipo2[3].y = 381


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
