import random
import itertools


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()
        self.assign_values_to_board()

        self.dug = set()  # si cava en 0, 0: self.dug = {(0, 0)}

    def make_new_board(self):
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

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs

    def dig(self, row, col):
        # Devuelve True si es un dig satisfactorio, False si es una bomba
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        colores = {
            0: 39,
            1: 36,
            2: 32,
            3: 31,
            4: 34,
            5: 33,
            '*': 35
        }
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = '\033['+ str(colores[self.board[row][col]]) + 'm' + \
                                              str(self.board[row][col]) + '\033[39m'
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        # obtiene el ancho de las cols para impresion
        widths = []
        for idx in range(self.dim_size):
            widths.append(1)

        # muestra los strings csv
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % col)
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = (3+1) * self.dim_size - self.dim_size // 2
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    safe = True
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = input("Para jugar, escribe 'fila, col' : ").replace(" ", "").split(",")
        row, col = int(user_input[0]), int(user_input[1])
        if row < 0 or row > dim_size or col < 0 or col > dim_size:
            print("Locación inválida, inténtelo de nuevo")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        colors = ['\033[3{}m{{}}\033[0m'.format(n) for n in range(1, 7)]
        rainbow = itertools.cycle(colors)
        letters = [next(rainbow).format(L) for L in 'Felicidades!!, ganaste!!']
        print(''.join(letters))
    else:
        print("Maldito perdedor!!")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


if __name__ == '__main__':
    print("Bienvenido al proyecto Mineswepper")
    print("Escoje el modo de juego:")
    print("1. Principiante")
    print("2. Intermedio")
    print("3. Experto")
    opc = int(input("Opción: "))
    if opc == 1:
        play(6, 6)
    elif opc == 2:
        play(10, 10)
    elif opc == 3:
        play(14, 14)
    else:
        print("Opción inválida, juego terminado")
