import pygame
from health_bar import HealthBar

class Player:
    def __init__(self, x, y,team,tiro):
        self.x = x
        self.y = y
        self.tiro = tiro
        self.team = team
        self.costo_tiro = 80
        self.costo_defensa = 40
        self.imagen_jugador = pygame.image.load("C:/Users/Juegos/Documents/barracuda_game/assets/players/azul.png").convert_alpha()
        self.dx = 4  # velocidad en x (puedes ajustar)
        self.dy = 4  # velocidad en y
        self.vector_long = (self.dx**2 + self.dy**2)**0.5
        self.vector_posicion = pygame.math.Vector2(self.x,self.y)
        self.vector = pygame.math.Vector2()
        self.long_x = self.imagen_jugador.get_width()
        self.long_y = self.imagen_jugador.get_height()
        self.rect = pygame.Rect(self.x - self.long_x // 2, self.y - self.long_y // 2, self.long_x, self.long_y)
        self.mascara = pygame.mask.from_surface(self.imagen_jugador)
        self.tiro_x = 1
        self.tiro_y = 1
        self.dano_tiro = 15
        self.colision_activa = False
        self.dano = False
        self.habilidad_activa = False
        self.defensa_activa = False
        self.barra_vida = HealthBar(x=self.x, y=self.y+25, width=50, height=10, max_health=100)
        

    def mover(self, teclas, controles):
        self.vector = pygame.math.Vector2(0, 0)  # reiniciar dirección acumulada

        if teclas[controles['arriba']]:
            self.vector.y -= 1
        if teclas[controles['abajo']]:
            self.vector.y += 1
        if teclas[controles['izquierda']]:
            self.vector.x -= 1
        if teclas[controles['derecha']]:
            self.vector.x += 1

        # Normalizar vector para mantener velocidad constante en diagonales
        if self.vector.length() != 0:
            self.vector = self.vector.normalize()

        # Mover al jugador según el vector resultante
        self.x += self.vector.x * self.dx
        self.y += self.vector.y * self.dy

        # Actualizar rectángulo para que esté centrado en (x,y)
        self.rect.topleft = (self.x - self.long_x // 2, self.y - self.long_y // 2)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_jugador, self.rect)

    def colisiona_con_balon(self, balon):
        # Posición relativa entre el jugador y el balón
        offset_x = balon.rect_normal.left - self.rect.left
        offset_y = balon.rect_normal.top - self.rect.top

        # Verifica superposición de máscaras
        if self.mascara.overlap(balon.mascara, (offset_x, offset_y)):
            # Usa la dirección de movimiento del jugador como impulso
            movimiento_magnitud = (self.dx ** 2 + self.dy ** 2) ** 0.5 or 1

            dir_x = self.dx / movimiento_magnitud
            dir_y = self.dy / movimiento_magnitud

            fuerza_rebote = 1

            balon.vx = dir_x * fuerza_rebote
            balon.vy = dir_y * fuerza_rebote
            self.colision_activa = True
        


    def actualizar_rect(self):
        self.rect.topleft = (self.x, self.y)


    def shoot(self, balon):
        # Obtener el centro del jugador y del balón
        centro_jugador = pygame.math.Vector2(self.x + self.long_x // 2, self.y + self.long_y // 2)
        centro_balon = pygame.math.Vector2(balon.x + balon.tamano // 2, balon.y + balon.tamano // 2)

        # Calcular vector desde jugador al balón
        direccion = centro_balon - centro_jugador

        # Si la magnitud es muy pequeña (están superpuestos o muy cerca), usar la última dirección de movimiento
        if direccion.length() < 1e-3:
            if self.vector.length() > 0:
                direccion = self.vector
            else:
                direccion = pygame.math.Vector2(1, 0)  # Disparo por defecto

        direccion = direccion.normalize()

        velocidad = self.tiro  # Magnitud del disparo

        # Asignar velocidad al balón
        balon.vx = direccion.x * velocidad
        balon.vy = direccion.y * velocidad



