import pygame
import random
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("La librería RPi.GPIO no está disponible. El control de LEDs no funcionará.")

# --- Definición de Colores ---
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE_COLOR = (0, 128, 0)
ROJO_COLOR = (255, 0, 0)
AMARILLO_COLOR = (255, 255, 0)
CIAN_COLOR = (128, 0, 128)
MORADO_COLOR = (0, 255, 255)

COLOR_NUMEROS = {
    1: AZUL,
    2: VERDE_COLOR,
    3: ROJO_COLOR,
    4: CIAN_COLOR,
    5: MORADO_COLOR,
    6: AMARILLO_COLOR,
    0: GRIS_OSCURO
}

LED_AMARILLO_PIN = 17
LED_VERDE_PIN = 27
LED_ROJO_PIN = 22

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self._make_new_board()
        self._assign_values_to_board()
        self.dug = set()
        self.flags = set()
        self.game_over = False

    def _make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == '*':
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def _assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self._get_num_neighboring_bombs(r, c)

    def _get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        if self.game_over or (row, col) in self.dug:
            return False

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            self.game_over = True
            return False
        elif self.board[row][col] > 0:
            return True
        else:
            for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
                for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                    if (r, c) not in self.dug:
                        self.dig(r, c)
            return True

    def toggle_flag(self, row, col):
        if not self.game_over and (row, col) not in self.dug:
            if (row, col) in self.flags:
                self.flags.remove((row, col))
            else:
                self.flags.add((row, col))

    def check_win(self):
        return len(self.dug) == self.dim_size ** 2 - self.num_bombs

class MinesweeperGame:
    def __init__(self, dim_size, num_bombs, cell_size=30):
        pygame.init()
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.cell_size = cell_size
        self.board = Board(dim_size, num_bombs)
        self.width = dim_size * cell_size
        self.height = dim_size * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Buscaminas")
        self.font = pygame.font.Font(None, 30)
        self.game_started = False
        self.playing = False # Nuevo estado para indicar si el juego está activo

        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM) 
            GPIO.setup(LED_AMARILLO_PIN, GPIO.OUT)
            GPIO.setup(LED_VERDE_PIN, GPIO.OUT)
            GPIO.setup(LED_ROJO_PIN, GPIO.OUT)
            self.turn_off_leds()

    def turn_on_led(self, pin):
        if GPIO_AVAILABLE:
            GPIO.output(pin, GPIO.HIGH)

    def turn_off_led(self, pin):
        if GPIO_AVAILABLE:
            GPIO.output(pin, GPIO.LOW)

    def turn_off_leds(self):
        self.turn_off_led(LED_AMARILLO_PIN)
        self.turn_off_led(LED_VERDE_PIN)
        self.turn_off_led(LED_ROJO_PIN)

    def draw_grid(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GRIS_CLARO, rect, 1)
                pygame.draw.rect(self.screen, GRIS_OSCURO, rect)

    def draw_board(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GRIS_CLARO, rect, 1)
                if (row, col) in self.board.dug:
                    value = self.board.board[row][col]
                    pygame.draw.rect(self.screen, BLANCO, rect)
                    if value == '*':
                        pygame.draw.circle(self.screen, ROJO_COLOR, rect.center, self.cell_size // 3)
                    elif value > 0:
                        text = self.font.render(str(value), True, COLOR_NUMEROS[value])
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, GRIS_OSCURO, rect)
                    if (row, col) in self.board.flags:
                        pygame.draw.polygon(self.screen, ROJO_COLOR, [rect.topright, (rect.centerx + self.cell_size // 4, rect.centery - self.cell_size // 4), rect.bottomright])
                        pygame.draw.line(self.screen, BLANCO, rect.topright, rect.bottomright, 2)

    def handle_click(self, pos, button):
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        if not self.game_started:
            self.game_started = True
            self.playing = True
            self.board = Board(self.dim_size, self.num_bombs)
            self.board.dig(row, col)
            self.turn_on_led(LED_AMARILLO_PIN)
        else:
            if not self.board.game_over and not self.board.check_win():
                self.playing = True
                self.turn_on_led(LED_AMARILLO_PIN)
                if button == 1:
                    self.board.dig(row, col)
                elif button == 3:
                    self.board.toggle_flag(row, col)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    button = event.button
                    self.handle_click(pos, button)

            self.screen.fill(GRIS_CLARO)
            if not self.game_started:
                self.draw_grid()
                start_text = self.font.render("Haz clic para empezar", True, NEGRO)
                text_rect = start_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(start_text, text_rect)
                self.turn_off_leds()
            else:
                self.draw_board()
                if self.board.game_over:
                    self.playing = False
                    self.turn_off_led(LED_AMARILLO_PIN)
                    self.turn_on_led(LED_ROJO_PIN)
                    game_over_text = self.font.render("¡¡Maldito perdedor!!", True, ROJO_COLOR)
                    text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(game_over_text, text_rect)
                elif self.board.check_win():
                    self.playing = False
                    self.turn_off_led(LED_AMARILLO_PIN)
                    self.turn_on_led(LED_VERDE_PIN)
                    win_text = self.font.render("¡Ganaste!", True, VERDE_COLOR)
                    text_rect = win_text.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(win_text, text_rect)
                elif self.playing:
                    self.turn_on_led(LED_AMARILLO_PIN)
                else:
                    self.turn_off_led(LED_AMARILLO_PIN) # Apaga el amarillo si no está jugando (ej: después de ganar/perder)

            pygame.display.flip()

        if GPIO_AVAILABLE:
            GPIO.cleanup() # Limpia los pines GPIO al cerrar Pygame

if __name__ == '__main__':
    print("Bienvenido al proyecto Mineswepper")
    print("Escoge el modo de juego:")
    print("1. Principiante")
    print("2. Intermedio")
    print("3. Experto")
    opc = int(input("Opción: "))
    if opc == 1:
        game = MinesweeperGame(6, 6)
    elif opc == 2:
        game = MinesweeperGame(10, 10)
    elif opc == 3:
        game = MinesweeperGame(14, 14)
    else:
        print("Opción inválida, juego terminado")
        exit()
    game.run()