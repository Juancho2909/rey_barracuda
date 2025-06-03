import pygame

class Clock:
    def __init__(self, fps=60, font_size=30, text_color=(255, 255, 255), 
                 bg_color=(0, 0, 0), pos=(210, 10), padding=10):
        self.clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.pos = pos
        self.fps = fps
        self.padding = padding

    def tick(self):
        """Llamar una vez por frame para limitar FPS"""
        return self.clock.tick(self.fps)

    def get_elapsed_time(self):
        """Devuelve el tiempo transcurrido en segundos"""
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        return elapsed_ms // 1000 

    def reset(self):
        """Reinicia el cronómetro"""
        self.start_ticks = pygame.time.get_ticks()
    
    def draw(self, surface):
        """Dibuja el tiempo transcurrido dentro de un rectángulo"""
        seconds = self.get_elapsed_time()
        minutes = seconds // 60
        secs = seconds % 60
        time_str = f"{minutes:02}:{secs:02}"

        text_surface = self.font.render(time_str, True, self.text_color)

        # Calcular el tamaño del rectángulo de fondo
        text_rect = text_surface.get_rect()
        bg_rect = pygame.Rect(
            self.pos[0], self.pos[1],
            text_rect.width + self.padding * 2,
            text_rect.height + self.padding * 2
        )

        # Dibujar el fondo (rectángulo) y luego el texto
        pygame.draw.rect(surface, self.bg_color, bg_rect, border_radius=8)
        surface.blit(text_surface, (self.pos[0] + self.padding, self.pos[1] + self.padding))
