
import random

# Model of snake using array of tuples

gridSize = 20

class Snake():

    def __init__(self):
        self.snake = [(0, 0)]
        self.afterLast = (0,0)
        self.dir = 0
        self.food = (random.randint(0, gridSize - 1), random.randint(0, gridSize - 1))
        self.size = 1
        self.nearestDown = gridSize
        self.nearestLeft = gridSize
        self.nearestRight = gridSize
        self.nearestUp = gridSize

    def changeDir(self, newDir):
        if self.dir + 2 != newDir and self.dir - 2 != newDir:
            self.dir = newDir

    def move(self):
        match self.dir:
            case 0: # Right
                self.next = (self.snake[len(self.snake)-1][0] + 1, self.snake[len(self.snake)-1][1])
                self.snake.append(self.next)
            case 1: # Down
                self.next = (self.snake[len(self.snake)-1][0], self.snake[len(self.snake)-1][1] - 1)
                self.snake.append(self.next)
            case 2: # Left
                self.next = (self.snake[len(self.snake)-1][0] - 1, self.snake[len(self.snake)-1][1])
                self.snake.append(self.next)
            case 3: # Up
                self.next = (self.snake[len(self.snake)-1][0], self.snake[len(self.snake)-1][1] + 1)
                self.snake.append(self.next)
        if(self.snake[len(self.snake) - 1] == self.food):
            self.food = (random.randint(0, gridSize - 1), random.randint(0, gridSize - 1))
            self.size += 1
            return
        self.afterLast = self.snake.pop(0)
        self.calculateDistances()

    def isColliding(self):
        bodyParts = self.snake[0:self.size-1]
        if(self.size > 2):
            if bodyParts.__contains__(self.snake[self.size - 1]):
                return True
        x = self.snake[self.size - 1][0]
        y = self.snake[self.size - 1][1]
        if x >= gridSize or y >= gridSize or x < 0 or y < 0:
            return True

    def calculateDistances(self):

        # Calculate distance to nearest body part in each direction

        x, y = self.snake[self.size - 1][0], self.snake[self.size - 1][1]
        tX, tY = x, y

        self.nearestLeft = x
        tX = 0
        tY = y
        while tX < x:
            if self.snake.__contains__((tX, tY)):
                self.nearestLeft = x - tX
            tX += 1
        
        self.nearestRight = gridSize - x
        tX = gridSize
        tY = y
        while tX > x:
            if self.snake.__contains__((tX, tY)):
                self.nearestRight = tX - x
            tX -= 1
        
        self.nearestDown = y
        tX = x
        tY = 0
        while tY < x:
            if self.snake.__contains__((tX, tY)):
                self.nearestDown = y - tY
            tY += 1
        
        self.nearestUp = gridSize - y
        tX = x
        tY = gridSize
        while tY > y:
            if self.snake.__contains__((tX, tY)):
                self.nearestUp = tY - y
            tY -= 1
