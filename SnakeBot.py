import numpy as np
import Model as snake
import tkinter as tk
import time

## INPUT: x and y coord of food, distance up, down, left, and right, to nearest body part, direction
## OUTPUT: 0 (right), 1 (down), 2 (left), 3 (right)

IN_SIZE = 9
HID1_SIZE = 18
HID2_SIZE = 4

# Sets negative values to 0, else returns x
def relu(x):
    return(x>0) * x

class SnakeBot:

    def __init__(self):
        self.snek = snake.Snake()
        self.watched = False
        self.score = 0
        self.totalTurns =  0
        self.lifetime = 0

    def reset(self):
        self.__init__()

    def startWatching(self):
        self.watched = True
        self.window = tk.Tk()
        self.window.config(width=800, height=800)

        self.frameArray = [[0 for i in range(snake.gridSize)] for j in range(snake.gridSize)]

        for row in range(snake.gridSize):
            for col in range(snake.gridSize):
                self.frameArray[row][col] = tk.Frame(width = 800/snake.gridSize, height = 800/snake.gridSize, bg="gray")
                self.frameArray[row][col].grid(row=row,column=col)

    def updateView(self):
        self.frameArray[self.snek.afterLast[0]][self.snek.afterLast[1]].configure(bg="gray")
        self.frameArray[self.snek.snake[len(self.snek.snake) - 1][0]][self.snek.snake[len(self.snek.snake) - 1][1]].configure(bg="black")
        tempRow = self.snek.food[0]
        tempCol = self.snek.food[1]
        self.frameArray[tempRow][tempCol].configure(bg="gray")
        self.frameArray[self.snek.food[0]][self.snek.food[1]].configure(bg="black")
        self.window.update()

    def loadWeights(self, weights):
        self.weights = weights
        self.in_h1 = self.weights[0]
        self.h1_h2 = self.weights[1]
        self.h2_out = self.weights[2]

    def changeWeightsABit(self):
        self.in_h1 += (np.random.normal(0, .00005, (IN_SIZE, HID1_SIZE)) / 100)
        self.h1_h2 += (np.random.normal(0, .00005, (HID1_SIZE, 4)) / 100)
        self.h2_out += np.random.normal(0, .02, (HID2_SIZE, 4))

    def generateRandomWeights(self):
        self.in_h1 = np.zeros((IN_SIZE, HID1_SIZE))
        self.h1_h2 = np.zeros((HID1_SIZE, 4))
        self.h2_out = np.zeros((HID2_SIZE, 4))
        self.weights = [self.in_h1, self.h1_h2, self.h2_out]

    def getWeightsAsString(self):
        return str(self.in_h1) + "\n" + str(self.h1_h2)

    def tick(self):

        self.lifetime += 1

        if(self.watched):
            time.sleep(.5)

        ## Gather inputs
        x = self.snek.snake[len(self.snek.snake) - 1][0]
        y = self.snek.snake[len(self.snek.snake) - 1][1]
        xFood = self.snek.food[0]
        yFood = self.snek.food[1]
        direction = self.snek.dir
        nearestUp = self.snek.nearestUp
        nearestDown = self.snek.nearestDown
        nearestLeft = self.snek.nearestLeft
        nearestRight = self.snek.nearestRight

        input = np.array([x,y, xFood, yFood, direction,nearestRight,nearestDown,nearestLeft,nearestUp])

        ## Run network

        h1 = relu(input.dot(self.in_h1))
        h2 = h1.dot(self.h1_h2)
        # out = h2.dot(self.h2_out)

        self.newDir = np.argmax(h2)
            
        match self.newDir:
                case 0:
                    if(xFood > x):
                        self.score += 5
                case 1:
                    if(yFood < y):
                        self.score += 5
                case 2:
                    if(xFood < x):
                        self.score += 5
                case 3:
                    if(yFood > y):
                        self.score += 5

        ## Change snake direction

        self.snek.changeDir(self.newDir)

        size = self.snek.size
        self.snek.move()
        if(self.snek.size > size):
            self.score += 50

        if(self.watched):
            print("X: " + str(x))
            print("Y: " + str(y))
            print("Food x: " + str(xFood))
            print("Food y: " + str(yFood))
            print("Direction: " + str(direction))
            print("Nearest Up: " + str(nearestUp))
            print("Nearest Down: " + str(nearestDown))
            print("Nearest Left: " + str(nearestLeft))
            print("Nearest Right: " + str(nearestRight))
            self.updateView()


# snek = SnakeBot()

# snek.generateRandomWeights()

# outFile = open('weights\\gen0.npy', 'wb')
# inFile = open('weights\\gen0.npy', 'rb')

# snek.saveWeights(outFile)
# snek.loadWeights(inFile)

# print(snek.in_h1)
# print(snek.h1_h2)
# print(snek.h2_out)
    
# snek.startWatching()

# while not snek.snek.isColliding():
#     snek.tick()
#     time.sleep(.2)