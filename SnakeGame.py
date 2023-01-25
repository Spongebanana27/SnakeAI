import tkinter as tk
import Model    
import time
import datetime

window = tk.Tk()

window.config(width=800, height=800)

gridSize = 20
gridPixels = 800 / gridSize

snek = Model.Snake()

frameArray = [[0 for i in range(gridSize)] for j in range(gridSize)]

for row in range(gridSize):
    for col in range(gridSize):
        frameArray[row][col] = tk.Frame(width = gridPixels, height = gridPixels, bg="gray")
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

    frameArray[snek.afterLast[0]][snek.afterLast[1]].configure(bg="gray")
    frameArray[snek.snake[len(snek.snake) - 1][0]][snek.snake[len(snek.snake) - 1][1]].configure(bg="black")
    tempRow = snek.food[0]
    tempCol = snek.food[1]
    if(snek.isColliding()):
        window.quit()
    snek.move()
    frameArray[tempRow][tempCol].configure(bg="gray")
    frameArray[snek.food[0]][snek.food[1]].configure(bg="black")
    window.after(200, updateGame)

window.after(0, updateGame)
window.mainloop()
