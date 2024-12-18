import pygame
import random

# Inicializar Pygame y el mixer de sonido
pygame.init()
pygame.mixer.init()

# Cargar la música de fondo
pygame.mixer.music.load('./sounds/musica_fondo.mp3')
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle

# Cargar sonidos
sonido_colision_meteorito = pygame.mixer.Sound("./sounds/colision_meteorito.wav")
sonido_recolectar_estrella = pygame.mixer.Sound("./sounds/recolectar_estrella.wav")

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carrera Espacial 🚀")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fuentes
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Variables del jugador
nombre_jugador = "Jugador"

# Fondo
background = pygame.image.load('./assets/espacio.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# FPS
clock = pygame.time.Clock()
FPS = 60

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Menú principal
def menu_principal():
    menu_options = ["Iniciar Juego", "Instrucciones", "Ingresar Nombre", "Ver Puntajes", "Salir"]
    selected = 0
    running = True

    while running:
        screen.fill(BLACK)
        draw_text("Menú Principal", big_font, WHITE, screen, WIDTH // 3, 50)

        # Dibujar opciones del menú
        for i, option in enumerate(menu_options):
            color = GREEN if i == selected else WHITE
            draw_text(option, font, color, screen, WIDTH // 3, 150 + i * 50)

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    return menu_options[selected].lower().replace(" ", "_")

# Mostrar instrucciones
def mostrar_instrucciones():
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Instrucciones", big_font, WHITE, screen, WIDTH // 3, 50)
        instrucciones = [
            "Usa las flechas para mover la nave.",
            "Evita los meteoritos y recoge las estrellas.",
            "¡Alcanza el puntaje objetivo (2000) para ganar!",
            "Presiona ESC para regresar al menú.",
        ]
        for i, line in enumerate(instrucciones):
            draw_text(line, font, WHITE, screen, 50, 150 + i * 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Ingresar nombre del jugador
def ingresar_nombre():
    global nombre_jugador
    name = ""
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Ingresa tu nombre:", font, WHITE, screen, 50, 50)
        draw_text(name, big_font, WHITE, screen, 50, 150)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Finalizar ingreso
                    nombre_jugador = name if name else "Jugador"
                    return
                elif event.key == pygame.K_BACKSPACE:  # Borrar
                    name = name[:-1]
                else:
                    name += event.unicode

# Ver puntajes más altos
def ver_puntajes():
    try:
        with open("puntajes.txt", "r") as f:
            scores = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        scores = ["No hay puntajes registrados"]

    running = True
    while running:
        screen.fill(BLACK)
        draw_text("Puntajes más altos", big_font, WHITE, screen, WIDTH // 3, 50)
        for i, score in enumerate(scores[:5]):
            draw_text(f"{i+1}. {score}", font, WHITE, screen, 50, 150 + i * 50)
        draw_text("Presiona ESC para regresar.", font, GRAY, screen, 50, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Guardar puntaje
def guardar_puntaje(nombre, puntaje):
    with open("puntajes.txt", "a") as f:
        f.write(f"{nombre}: {puntaje}\n")

# Clase para la nave del jugador
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/nave.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

# Clase para los meteoritos
class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/meteorito.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self, keys):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Clase para las estrellas
class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./assets/estrella.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self, keys):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Juego principal
def juego_principal():
    global nombre_jugador
    running = True
    score = 0
    win_score = 2000
    vidas = 3

    # Sprites
    all_sprites = pygame.sprite.Group()
    meteoritos = pygame.sprite.Group()
    estrellas = pygame.sprite.Group()
    jugador = Nave()
    all_sprites.add(jugador)

    for _ in range(5):
        meteorito = Meteorito()
        all_sprites.add(meteorito)
        meteoritos.add(meteorito)

    for _ in range(3):
        estrella = Estrella()
        all_sprites.add(estrella)
        estrellas.add(estrella)

    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualización
        keys = pygame.key.get_pressed()
        all_sprites.update(keys)

        # Colisiones con meteoritos
        if pygame.sprite.spritecollide(jugador, meteoritos, True):
            sonido_colision_meteorito.play()
            vidas -= 1
            if vidas <= 0:
                guardar_puntaje(nombre_jugador, score)
                running = False
                perdiste(score)

        # Colisiones con estrellas
        estrellas_recogidas = pygame.sprite.spritecollide(jugador, estrellas, True)
        for estrella in estrellas_recogidas:
            sonido_recolectar_estrella.play()
            score += 100
            nueva_estrella = Estrella()
            all_sprites.add(nueva_estrella)
            estrellas.add(nueva_estrella)

        # Dibujar
        all_sprites.draw(screen)
        draw_text(f"Jugador: {nombre_jugador}", font, WHITE, screen, 10, 10)
        draw_text(f"Score: {score}", font, WHITE, screen, 10, 50)
        draw_text(f"Vidas: {vidas}", font, WHITE, screen, 10, 90)

        # Incrementar puntaje
        # score += 1
        if score >= win_score:
            guardar_puntaje(nombre_jugador, score)
            running = False
            ganaste(score)

        pygame.display.flip()

    # Fin del juego
    # screen.fill(BLACK)
    # draw_text("Fin del juego :(", big_font, WHITE, screen, WIDTH // 3, HEIGHT // 3)
    # draw_text(f"Puntaje Final: {score}", font, WHITE, screen, WIDTH // 3, HEIGHT // 2)
    # pygame.display.update()
    # pygame.time.delay(5000)


def ganaste(score):
    screen.fill(BLACK)
    draw_text("¡Ganaste! :)", big_font, WHITE, screen, WIDTH // 3, HEIGHT // 3)
    draw_text(f"Puntaje Final: {score}", font, WHITE, screen, WIDTH // 3, HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(5000)

def perdiste(score):
    screen.fill(BLACK)
    draw_text("¡Juego Terminado! :(", big_font, WHITE, screen, WIDTH // 3, HEIGHT // 3)
    draw_text(f"Puntaje Final: {score}", font, WHITE, screen, WIDTH // 3, HEIGHT // 2)
    pygame.display.update()
    pygame.time.delay(5000)
        

# Flujo principal
def main():
    while True:
        opcion = menu_principal()
        if opcion == "iniciar_juego":
            juego_principal()
        elif opcion == "instrucciones":
            mostrar_instrucciones()
        elif opcion == "ingresar_nombre":
            ingresar_nombre()
        elif opcion == "ver_puntajes":
            ver_puntajes()
        elif opcion == "salir":
            pygame.quit()
            return

if __name__ == "__main__":
    main()
