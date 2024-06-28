import pygame
import random

# Inicialización de PyGame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Disparos Espaciales")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Cargar imágenes
jugador_img = pygame.image.load("jugador.png")
enemigo_img = pygame.image.load("enemigo.png")
bala_img = pygame.image.load("bala.png")

# Clase Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(jugador_img, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0

    def update(self):
        self.velocidad_x = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
        self.rect.x += self.velocidad_x
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_las_sprites.add(bala)
        balas.add(bala)

# Clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemigo_img, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidad_y = random.randrange(1, 8)

# Clase Bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bala_img, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidad_y = -10

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

# Función principal del juego
def juego():
    global todas_las_sprites, enemigos, balas
    todas_las_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    jugador = Jugador()
    todas_las_sprites.add(jugador)

    for i in range(8):
        enemigo = Enemigo()
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)

    puntuacion = 0

    reloj = pygame.time.Clock()
    corriendo = True
    while corriendo:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.disparar()

        todas_las_sprites.update()

        # Colisiones
        colisiones = pygame.sprite.groupcollide(enemigos, balas, True, True)
        for colision in colisiones:
            puntuacion += 1
            enemigo = Enemigo()
            todas_las_sprites.add(enemigo)
            enemigos.add(enemigo)

        pantalla.fill(NEGRO)
        todas_las_sprites.draw(pantalla)
        pygame.display.flip()

# Menú principal
def mostrar_menu():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render("Pulsa Enter para jugar", True, BLANCO)
    pantalla.blit(texto, (100, ALTO // 2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RETURN:
                    esperando = False

# Bucle principal
mostrar_menu()
juego()
pygame.quit()





                    