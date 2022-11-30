import tkinter as tk
from copy import deepcopy
from tkinter import messagebox as mb
from random import choice


class Cell(tk.Canvas):
    def __init__(self, master, x, y):
        super().__init__(master, bg='#222222', bd=0, highlightthickness=1,
                         width=200, height=200)
        self.bind('<Button-1>', self.event)
        self.grid(column=x, row=y)
        self.value = None
        self.y = y
        self.x = x

    def clear(self):
        self.value = None
        self.delete('all')

    def event(self, event):
        if self.value is None:
            if self.place_char(player_char) is None:
                computer_move(computer_char)

    def place_char(self, char):
        self.value = char
        if char == 'x':
            self.create_line(30, 30, 170, 170, fill='#FF6188', width=5,
                             capstyle='round')
            self.create_line(30, 170, 170, 30, fill='#FF6188', width=5,
                             capstyle='round')
        else:
            self.create_oval(30, 30, 170, 170, outline='#78DCE8', width=5)
        if (res := win_check(char, [[x.value for x in y] for y in cells],
                             self.x, self.y)) is not None:
            match res:
                case 'win':
                    mb.showinfo('Winner, winner chicken dinner!',
                                f'{char} won!{" "*29}')
                case 'draw':
                    mb.showinfo('Draw', 'Draw')
            for y in cells:
                for cell in y:
                    cell.clear()
            if computer_char == 'x':
                cells[choice((0, 2))][choice((0, 2))].place_char('x')
            return True


class ChoiceBtn(Cell):
    def __init__(self, master, x, y, char):
        super().__init__(master, x, y)
        self.char = char
        self.place_char(char)

    def event(self, event):
        global player_char, computer_char
        player_char = self.char
        computer_char = '0' if self.char == 'x' else 'x'
        self.master.destroy()
        if computer_char == 'x':
            cells[choice((0, 2))][choice((0, 2))].place_char('x')


def win_check(char, board, x, y):
    if any((all([i == char for i in board[y]]),
            all([i[x] == char for i in board]),
            all([board[i][i] == char for i in range(3)]),
            all([board[i][2 - i] == char for i in range(3)]))):
        return 'win'
    elif [board[i // 3][i % 3] for i in range(9)].count(None) == 0:
        return 'draw'


def computer_move(char):
    best_score = -2
    best_x, best_y = 0, 0
    board = [[x.value for x in y] for y in cells]
    for y in range(3):
        for x in range(3):
            if board[y][x] is None:
                board[y][x] = computer_char
                if win_check(char, board, x, y) is not None:
                    cells[y][x].place_char(computer_char)
                    return None
                score = (minimax(board))
                if score > best_score:
                    best_score = score
                    best_x, best_y = x, y
                board[y][x] = None
    cells[best_y][best_x].place_char(computer_char)


def minimax(board, fac=-1):
    char = computer_char if fac == 1 else player_char
    new_board = deepcopy(board)
    results = []
    for y in range(3):
        for x in range(3):
            if new_board[y][x] is None:
                new_board[y][x] = char
                match win_check(char, new_board, x, y):
                    case 'win':
                        return fac
                    case 'draw':
                        return 0
                results.append(minimax(new_board, -fac))
                new_board[y][x] = None
    return max(results) if fac == 1 else min(results)


root = tk.Tk()
root.title('Tic tac toe')
root.geometry('600x600')
root.resizable(False, False)
root.config(bg='#222222')
board_frame = tk.Frame(root, bg='#222222')
board_frame.grid()

cells = [[Cell(board_frame, x, y) for x in range(3)] for y in range(3)]

choice_frame = tk.Frame(bg='#222222')
choice_frame.columnconfigure((0, 1), weight=1)
choice_frame.rowconfigure((0, 1), weight=1)
choice_frame.grid(row=0, column=0, sticky='nsew')
tk.Label(choice_frame, text='Выберите символ', fg='white', font=('Arial', 20),
         bg='#222222').grid(sticky='ew', columnspan=2)
ChoiceBtn(choice_frame, 0, 1, 'x')
ChoiceBtn(choice_frame, 1, 1, '0')

root.mainloop()
