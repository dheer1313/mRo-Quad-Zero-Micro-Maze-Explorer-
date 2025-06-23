import time
import tkinter as tk

# 5x5 Maze Grid with goal at (4, 4)
MAZE_SIZE = 5
class MazeSim:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=500, height=500, bg='white')
        self.canvas.pack()
        self.pos = [0, 0]  # Start at top-left
        self.goal = [4, 4]
        self.draw_grid()
        self.move_drone()

    def draw_grid(self):
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                x0, y0 = i * 100, j * 100
                x1, y1 = x0 + 100, y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='gray')
        self.drone = self.canvas.create_oval(10, 10, 90, 90, fill='blue')
        self.goal_rect = self.canvas.create_rectangle(400, 400, 500, 500, fill='green')

    def move_drone(self):
        x, y = self.pos
        if x < MAZE_SIZE - 1:
            x += 1
        elif y < MAZE_SIZE - 1:
            x = 0
            y += 1
        self.pos = [x, y]
        self.canvas.coords(self.drone, x*100+10, y*100+10, x*100+90, y*100+90)
        if self.pos == self.goal:
            print("Goal reached!")
        else:
            root.after(1000, self.move_drone)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Phase 2 Maze Simulator")
    app = MazeSim(root)
    root.mainloop()