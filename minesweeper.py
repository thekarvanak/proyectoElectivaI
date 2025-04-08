import pygame
import random

# --- Definición de Colores ---
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 128, 0)
ROJO = (255, 0, 0)
MORADO = (128, 0, 128)
CIAN = (0, 255, 255)
AMARILLO = (255, 255, 0)

COLOR_NUMEROS = {
    1: AZUL,
    2: VERDE,
    3: ROJO,
    4: MORADO,
    5: CIAN,
    6: AMARILLO,
    0: GRIS_OSCURO
}

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self._make_new_board()
        self._assign_values_to_board()
        self.dug = set()
        self.flags = set() # Para marcar posibles bombas
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
        else: # self.board[row][col] == 0
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
        self.game_started = False # Nuevo estado para controlar la pantalla inicial

    def draw_grid(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GRIS_CLARO, rect, 1) # Bordes de las celdas
                pygame.draw.rect(self.screen, GRIS_OSCURO, rect) # Celdas sin descubrir

    def draw_board(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, GRIS_CLARO, rect, 1) # Bordes de las celdas
                if (row, col) in self.board.dug:
                    value = self.board.board[row][col]
                    pygame.draw.rect(self.screen, BLANCO, rect)
                    if value == '*':
                        pygame.draw.circle(self.screen, ROJO, rect.center, self.cell_size // 3)
                    elif value > 0:
                        text = self.font.render(str(value), True, COLOR_NUMEROS[value])
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.screen, GRIS_OSCURO, rect)
                    if (row, col) in self.board.flags:
                        pygame.draw.polygon(self.screen, ROJO, [rect.topright, (rect.centerx + self.cell_size // 4, rect.centery - self.cell_size // 4), rect.bottomright])
                        pygame.draw.line(self.screen, BLANCO, rect.topright, rect.bottomright, 2)


    def handle_click(self, pos, button):
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        if not self.game_started:
            self.game_started = True # El primer clic inicia el juego
            self.board = Board(self.dim_size, self.num_bombs) # Generar el tablero al primer clic
            self.board.dig(row, col) # Descubrir la primera celda
        else:
            if button == 1: # Clic izquierdo
                self.board.dig(row, col)
            elif button == 3: # Clic derecho
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
                self.draw_grid() # Dibuja la cuadrícula en la pantalla inicial
                start_text = self.font.render("Haz clic para empezar", True, NEGRO)
                text_rect = start_text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(start_text, text_rect)
            else:
                self.draw_board() # Dibuja el tablero durante el juego
                if self.board.game_over:
                    game_over_text = self.font.render("¡BOOM! Perdiste", True, ROJO)
                    text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(game_over_text, text_rect)
                elif self.board.check_win():
                    win_text = self.font.render("¡Ganaste!", True, VERDE)
                    text_rect = win_text.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(win_text, text_rect)

            pygame.display.flip()

        pygame.quit()

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