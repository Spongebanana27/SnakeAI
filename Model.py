
# Model of snake using a linked list

class BodyPart():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.follower = None

    def move(self):
        if(self.follower != None):
            self.follower.move()
            self.follower.x = self.x
            self.follower.y = self.y

class Head():

    def __init__(self, x, y):
        self.dir = 0
        self.x = x
        self.y = y
        self.follower = None

    def addFollower(self):
        last = self
        while(last.follower != None):
            last = last.follower
        newPart = BodyPart(last.x, last.y)
        last.follower = newPart

    def changeDir(self, newDir):
        self.dir = newDir

    def move(self):
        if self.follower != None:
            self.follower.move()
            self.follower.x = self.x
            self.follower.y = self.y
        match self.dir:
            case 0:
                self.x += 1
            case 1:
                self.y -= 1
            case 2:
                self.x -= 1
            case 3:
                self.y += 1