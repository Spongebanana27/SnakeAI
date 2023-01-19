import tkinter as tk
import Model    
import time

window = tk.Tk()

window.config(width=900, height=900)

gridSize = 9
gridPixels = 900 / gridSize

snek = Model.Head(0,0)

frameArray = [[0 for i in range(gridSize)] for j in range(gridSize)]

for row in range(gridSize):
    for col in range(gridSize):
        frameArray[row][col] = tk.Frame(width = gridPixels, height = gridPixels, bg="white")
        frameArray[row][col].grid(row=row,column=col)

def right(event):
    snek.changeDir(3)

window.bind('<Right>', right)

def left(event):
    snek.changeDir(1)

window.bind('<Left>', left)

def up(event):
    snek.changeDir(2)

window.bind('<Up>', up)

def down(event):
    snek.changeDir(0)

window.bind('<Down>', down)

def updateGame():
    snek.move()
    frameArray[snek.x][snek.y].configure(bg="blue")
    window.update()
    updateGame()
updateGame()

window.mainloop()