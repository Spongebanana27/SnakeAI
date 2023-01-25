import SnakeBot
import numpy as np

generation = 1
generationSize = 100
totalGenerations = 1000

bot = SnakeBot.SnakeBot()
bot.generateRandomWeights()
bot.saveWeights(open("weights\\gen0.npy", 'wb'))
    
bestWeights = np.load(open("weights\\gen0.npy", 'rb'))
secondBestWeights = np.load(open("weights\\gen0.npy", 'rb'))

while generation < totalGenerations:

    genBest = 0
    genSecondBest = 0

    avg = 0

    for i in range(generationSize):

        newBot = SnakeBot.SnakeBot()
        newBot.loadWeights(open("weights\\gen" + str(generation - 1) + ".npy", 'rb'))
        newBot.changeWeightsABit()

        while not newBot.snek.isColliding() and newBot.lifetime < 200:
            newBot.tick()

        score = newBot.score  + (newBot.snek.size * 10) + (newBot.lifetime * 2)

        if score > genBest:
            genBest = score
            newBot.saveWeights(open("weights\\gen" + str(generation) + ".npy", 'wb'))
            bestSize = newBot.snek.size

        # if score > genBest:
        #     secondBestWeights = bestWeights
        #     genSecondBest = genBest
        #     genBest = score
        #     bestSize = newBot.snek.size
        #     bestWeights = newBot.weights
        # elif score > genSecondBest:
        #     genSecondBest = score
        #     secondBestWeights = newBot.weights

        avg += score

    avg /= generationSize
    
    # # Average the top two weights and pass that on

    # newWeights0 = (bestWeights['inh1'] + secondBestWeights['inh1']) / 2.0
    # newWeights1 = (bestWeights['h1h2'] + secondBestWeights['h1h2']) / 2.0
    # newWeights2 = (bestWeights['h2out'] + secondBestWeights['h2out']) / 2.0

    # np.savez(open("weights\\gen" + str(generation) + ".npy", 'wb'), inh1=newWeights0, h1h2=newWeights1, h2out=newWeights2)

    print("Generation: " + str(generation))
    print("Best GenScore: " + str(genBest))
    print("Size of best bot: " + str(bestSize))
    print("Avg score: " + str(avg))

    generation += 1

newBot = SnakeBot.SnakeBot()
newBot.loadWeights(open("weights\\gen98.npy", 'rb'))
newBot.startWatching()
while not newBot.snek.isColliding() and newBot.lifetime < 200:
    newBot.tick()
    print(newBot.score)