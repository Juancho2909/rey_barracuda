import pygame

class PowerBar:
    def __init__(self, x, y,width=20, height=100, max_power=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_power = max_power
        self.current_power = 0
        self.color_fondo = (50, 50, 50)
        self.color_llenado = (255, 255, 0)
        self.color_lleno = (0, 255, 0)
        self.borde_color = (255, 255, 255)
        self.borde_color_lleno = (255, 0, 0)
        self.borde_grosor = 2

    def aumentar_poder(self, aumento, cantidad=1):
        self.current_power = min(self.current_power + aumento * cantidad, self.max_power)

    def disminuir_poder(self, cantidad, poder):
        disminucion = self.current_power - cantidad
        if disminucion > 0:
            self.current_power = max(disminucion, 0)
            poder = True
        else:
            poder = False
        return poder

    def reiniciar(self):
        self.current_power = 0

    def obtener_poder_normalizado(self):
        return self.current_power / self.max_power

    def dibujar(self, pantalla):
        # Dibujar fondo
        pygame.draw.rect(pantalla, self.color_fondo, (self.x, self.y, self.width, self.height))

        # Calcular altura del llenado
        altura_llenado = int((self.current_power / self.max_power) * self.height)
        y_llenado = self.y + self.height - altura_llenado

        # Cambiar color si está llena
        if self.current_power >= self.max_power:
            color_actual = self.color_lleno
            borde_actual = self.borde_color_lleno
        else:
            color_actual = self.color_llenado
            borde_actual = self.borde_color

        # Dibujar barra de llenado
        pygame.draw.rect(pantalla, color_actual, (self.x, y_llenado, self.width, altura_llenado))

        # Dibujar borde
        pygame.draw.rect(pantalla, borde_actual, (self.x, self.y, self.width, self.height), self.borde_grosor)
