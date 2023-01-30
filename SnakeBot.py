import numpy as np
import Model as snake
import tkinter as tk
import time

## INPUT: x and y coord of food, distance up, down, left, and right, to nearest body part, direction
## OUTPUT: 0 (right), 1 (down), 2 (left), 3 (right)

IN_SIZE = 9
HID1_SIZE = 7
HID2_SIZE = 5

MUTATION_CHANCE = .25
ALPHA = .0001

MUTATION_UPPER_BOUND = int(3 / MUTATION_CHANCE)

# Sets negative values to 0, else returns x
def relu(x):
    return(x>0) * x

class SnakeBot:

    def __init__(self):
        self.rep = snake.Snake()
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
        self.frameArray[self.rep.afterLast[0]][self.rep.afterLast[1]].configure(bg="gray")
        self.frameArray[self.rep.snake[len(self.rep.snake) - 1][0]][self.rep.snake[len(self.rep.snake) - 1][1]].configure(bg="black")
        tempRow = self.rep.food[0]
        tempCol = self.rep.food[1]
        self.frameArray[tempRow][tempCol].configure(bg="gray")
        self.frameArray[self.rep.food[0]][self.rep.food[1]].configure(bg="black")
        self.window.update()

    def loadWeights(self, weights):
        self.weights = weights
        self.in_h1 = self.weights[0]
        self.h1_h2 = self.weights[1]
        self.h2_out = self.weights[2]

    def mutate(self):

        x = np.random.randint(0, MUTATION_UPPER_BOUND)
        match x:
            case 0:
                self.in_h1 += (np.random.normal(0, ALPHA, (IN_SIZE, HID1_SIZE)))
            case 1:
                self.h1_h2 += (np.random.normal(0, ALPHA, (HID1_SIZE, HID2_SIZE)))
            case 2:
                self.h2_out += np.random.normal(0, ALPHA, (HID2_SIZE, 4))
        x = np.random.randint(0, MUTATION_UPPER_BOUND)
        match x:
            case 0:
                self.in_h1 += (np.random.normal(0, ALPHA, (IN_SIZE, HID1_SIZE)))
            case 1:
                self.h1_h2 += (np.random.normal(0, ALPHA, (HID1_SIZE, HID2_SIZE)))
            case 2:
                self.h2_out += np.random.normal(0, ALPHA, (HID2_SIZE, 4))

    def generateRandomWeights(self):
        self.in_h1 = np.zeros((IN_SIZE, HID1_SIZE))
        self.h1_h2 = np.zeros((HID1_SIZE, HID2_SIZE))
        self.h2_out = np.zeros((HID2_SIZE, 4))
        self.weights = [self.in_h1, self.h1_h2, self.h2_out]

    def getWeightsAsString(self):
        return str(self.in_h1) + "\n" + str(self.h1_h2)

    def tick(self):

        self.lifetime += 1

        if(self.watched):
            time.sleep(.25)

        ## Gather inputs
        x = self.rep.snake[len(self.rep.snake) - 1][0]
        y = self.rep.snake[len(self.rep.snake) - 1][1]
        xFood = self.rep.food[0]
        yFood = self.rep.food[1]
        direction = self.rep.dir
        nearestUp = self.rep.nearestUp
        nearestDown = self.rep.nearestDown
        nearestLeft = self.rep.nearestLeft
        nearestRight = self.rep.nearestRight

        input = np.array([x,y, xFood, yFood, direction,nearestRight,nearestDown,nearestLeft,nearestUp])

        ## Run network

        h1 = relu(input.dot(self.in_h1))
        h2 = relu(h1.dot(self.h1_h2))
        out = h2.dot(self.h2_out)
        self.newDir = np.argmax(out)

        ## Change snake direction and move

        self.rep.changeDir(self.newDir)
        prevSize = self.rep.size
        self.rep.move()

        ## Update score

        match self.newDir:
                case 0:
                    if(xFood > x):
                        self.score += int(10 / (xFood-x))
                case 1:
                    if(yFood < y):
                        self.score += int(10 / (y-yFood))
                case 2:
                    if(xFood < x):
                        self.score += int(10 / (x-xFood))
                case 3:
                    if(yFood > y):
                        self.score += int(10 / (yFood-y))
        if(self.rep.size > prevSize):
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