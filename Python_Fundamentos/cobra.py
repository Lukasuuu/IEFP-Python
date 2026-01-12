"""Jogo da Cobra simples usando tkinter (funciona no Windows).

Substitui a versão baseada em curses por uma implementação com tkinter.
Use as setas para controlar a cobra. Fecha a janela para sair.
"""

import tkinter as tk
import random


class SnakeGame(tk.Frame):
    def __init__(self, master=None, width=600, height=400, cell_size=20):
        super().__init__(master)
        self.master = master # type: ignore
        self.width = width
        self.height = height
        self.cell = cell_size
        self.columns = self.width // self.cell
        self.rows = self.height // self.cell

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        self.pack()

        self.direction = 'Right'
        self.next_direction = self.direction
        self.snake = [(self.rows//2, self.columns//4 + i) for i in range(3)][::-1]
        self.snake_ids = []
        self.food = None
        self.food_id = None
        self.score = 0
        self.running = True
        self.speed = 120  # ms entre frames

        self.master.title('Cobra - Tkinter') # type: ignore
        self.master.bind('<Key>', self.on_key)

        self.draw_board()
        self.place_food()
        self.update()

    def draw_board(self):
        for seg in self.snake:
            self.snake_ids.append(self.draw_cell(seg, 'green'))

    def draw_cell(self, pos, color):
        r, c = pos
        x1 = c * self.cell
        y1 = r * self.cell
        x2 = x1 + self.cell
        y2 = y1 + self.cell
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

    def place_food(self):
        while True:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            if (r, c) not in self.snake:
                self.food = (r, c)
                break
        if self.food_id:
            self.canvas.delete(self.food_id)
        r, c = self.food
        x1 = c * self.cell + 4
        y1 = r * self.cell + 4
        x2 = x1 + self.cell - 8
        y2 = y1 + self.cell - 8
        self.food_id = self.canvas.create_oval(x1, y1, x2, y2, fill='red', outline='')

    def on_key(self, event):
        key = event.keysym
        opposites = {'Up':'Down', 'Down':'Up', 'Left':'Right', 'Right':'Left'}
        mapping = {'Up':'Up', 'Down':'Down', 'Left':'Left', 'Right':'Right'}
        if key in mapping and mapping[key] != opposites.get(self.direction):
            self.next_direction = mapping[key]

    def step(self):
        if not self.running:
            return
        self.direction = self.next_direction
        head = self.snake[0]
        r, c = head
        if self.direction == 'Up':
            r -= 1
        elif self.direction == 'Down':
            r += 1
        elif self.direction == 'Left':
            c -= 1
        elif self.direction == 'Right':
            c += 1

        new_head = (r, c)
        # Verifica colisões
        if (r < 0 or r >= self.rows or c < 0 or c >= self.columns or new_head in self.snake):
            self.game_over()
            return

        # Insere nova cabeça
        self.snake.insert(0, new_head)
        new_id = self.draw_cell(new_head, 'green')
        self.snake_ids.insert(0, new_id)

        # Verifica se comeu
        if new_head == self.food:
            self.score += 10
            self.place_food()
        else:
            # Remove cauda
            tail = self.snake.pop()
            tail_id = self.snake_ids.pop()
            self.canvas.delete(tail_id)

    def update(self):
        self.step()
        if self.running:
            self.master.after(self.speed, self.update)

    def game_over(self):
        self.running = False
        self.canvas.create_text(self.width//2, self.height//2, text=f'GAME OVER\nPontos: {self.score}', fill='white', font=('Arial', 20))


def main():
    root = tk.Tk()
    app = SnakeGame(root, width=600, height=400, cell_size=20)
    app.mainloop()


if __name__ == '__main__':
    main()