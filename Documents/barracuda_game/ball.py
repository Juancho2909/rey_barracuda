import pygame

class Balon:
    def __init__(self, color, tamano, material, x, y, vx, vy):
        self.color = color
        self.tamano = tamano  # radio
        self.material = material
        self.inflado = True
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.actualizar_rects()
        self.generar_superficie_y_mascara()


    def actualizar_rects(self):
        # Rectángulo que encierra el balón
        self.rect_normal = pygame.Rect(self.x - self.tamano, self.y - self.tamano, 2 * self.tamano, 2 * self.tamano)
        
        # Rectángulo "diagonal" que cubre el área del movimiento
        desplazamiento_x = self.vx if self.vx != 0 else 1
        desplazamiento_y = self.vy if self.vy != 0 else 1
        self.rect_diagonal = pygame.Rect(
            min(self.x, self.x + desplazamiento_x) - self.tamano,
            min(self.y, self.y + desplazamiento_y) - self.tamano,
            abs(desplazamiento_x) + 2 * self.tamano,
            abs(desplazamiento_y) + 2 * self.tamano
        )

    def patear(self):
        if self.inflado:
            print(f"¡Has pateado el balón {self.color}!")
        else:
            print("El balón está desinflado. No puedes patearlo.")

    def desinflar(self):
        if self.inflado:
            self.inflado = False
            print("El balón ha sido desinflado.")
        else:
            print("El balón ya está desinflado.")

    def inflar(self):
        if not self.inflado:
            self.inflado = True
            print("El balón ha sido inflado.")
        else:
            print("El balón ya está inflado.")

    def mover(self, ancho_ventana, alto_ventana):
        if not self.inflado:
            print("El balón está desinflado. No se puede mover.")
            return

        self.x += self.vx
        self.y += self.vy

        # Rebote contra bordes de la ventana
        if self.x - self.tamano <= 0 or self.x + self.tamano >= ancho_ventana:
            self.vx = -self.vx
            self.x += self.vx   #corrige la posición tras el rebote

        if self.y - self.tamano <= 0 or self.y + self.tamano >= alto_ventana:
            self.vy = -self.vy
            self.y += self.vy   #corrige la posición tras el rebote

                # Aplicar fricción para que el balón se desacelere con el tiempo
        friccion = 0.985
        self.vx *= friccion
        self.vy *= friccion
        self.actualizar_rects()  # actualizar los rectángulos tras moverse

    def dibujar(self, pantalla):
        if self.inflado:
            self.generar_superficie_y_mascara()  # actualizar el color actual
            pantalla.blit(self.superficie, (self.x - self.tamano, self.y - self.tamano))
        else:
            # Dibujo para el balón desinflado
            pygame.draw.circle(pantalla, (100, 100, 100), (int(self.x), int(self.y)), self.tamano, 2)

    def generar_superficie_y_mascara(self):
        diametro = self.tamano * 2
        self.superficie = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
        self.superficie.fill((0, 0, 0, 0))  # transparente
        pygame.draw.circle(self.superficie, self.color, (self.tamano, self.tamano), self.tamano)
        self.mascara = pygame.mask.from_surface(self.superficie)
