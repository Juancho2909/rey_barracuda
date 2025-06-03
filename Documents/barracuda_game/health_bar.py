import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health, border_color=(255, 255, 255), bg_color=(60, 60, 60)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.border_color = border_color
        self.bg_color = bg_color
        self.border_thickness = 2

    def set_health(self, dano):
        diferencia = self.current_health - dano
        self.current_health = max(0, diferencia)

    def get_health_color(self):
        porcentaje = self.current_health / self.max_health
        if porcentaje > 0.6:
            return (0, 255, 0)  # Verde
        elif porcentaje > 0.3:
            return (255, 215, 0)  # Amarillo
        else:
            return (255, 0, 0)  # Rojo

    def draw(self, surface):
        # Fondo
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))

        # Barra de salud con color dinámico
        health_width = int((self.current_health / self.max_health) * self.width)
        pygame.draw.rect(surface, self.get_health_color(), (self.x, self.y, health_width, self.height))

        # Borde
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), self.border_thickness)
