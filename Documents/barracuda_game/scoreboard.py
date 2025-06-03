import pygame

class Scoreboard:
    def __init__(self, fuente=None, tamano_fuente=36, color_texto=(255, 255, 255), color_fondo1=(0, 0, 255), color_fondo2=(255, 0, 0), posicion=(10, 10), ancho=100, alto=50):
        pygame.font.init()
        self.equipo1 = 0
        self.equipo2 = 0
        self.color_texto = color_texto
        self.color_fondo1 = color_fondo1
        self.color_fondo2 = color_fondo2
        self.posicion = posicion  # (x, y) de la esquina izquierda del primer rectángulo
        self.ancho = ancho
        self.alto = alto
        self.fuente = pygame.font.Font(fuente, tamano_fuente)

    def aumentar_score(self, equipo):
        if equipo == 1:
            self.equipo1 += 1
        elif equipo == 2:
            self.equipo2 += 1

    def resetear_score(self):
        self.equipo1 = 0
        self.equipo2 = 0

    def dibujar(self, pantalla):
        x, y = self.posicion

        # Rectángulo equipo 1
        rect1 = pygame.Rect(x, y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, self.color_fondo1, rect1)
        texto1 = self.fuente.render(str(self.equipo1), True, self.color_texto)
        texto_rect1 = texto1.get_rect(center=rect1.center)
        pantalla.blit(texto1, texto_rect1)

        # Rectángulo equipo 2 (al lado del primero)
        rect2 = pygame.Rect(x + self.ancho + 10, y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, self.color_fondo2, rect2)
        texto2 = self.fuente.render(str(self.equipo2), True, self.color_texto)
        texto_rect2 = texto2.get_rect(center=rect2.center)
        pantalla.blit(texto2, texto_rect2)
