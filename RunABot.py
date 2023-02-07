import numpy as np
import SnakeBot

weights = np.load(open("weights\\gen2000.npy", "rb"))

newBot = SnakeBot.SnakeBot()

newBot.in_h1 = weights['inh1']
newBot.h1_h2 = weights['h1h2']
newBot.h2_out = weights['h2out']

newBot.startWatching()
print("\n\n\n\n")
while not newBot.rep.isColliding() and newBot.lifetime < 200:
    newBot.tick()
    print(newBot.score)