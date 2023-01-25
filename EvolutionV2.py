import SnakeBot
import numpy as np
import sys
# Second attempt at evolutionary algorithm. This one will save the top 10% snakes from the population and randomly select 2 to pass on their weights

generation = 1
generationSize = 100
totalGenerations = 5001

newBot = SnakeBot.SnakeBot()
newBot.generateRandomWeights()
currentWeights = newBot.weights

while generation < totalGenerations:

    genBest = 0
    avg = 0

    topScores = [-20]
    topWeights = [[currentWeights]]

    for i in range(generationSize):

        score = 0
        newBot.reset()
        newBot.lifetime = 0
        newBot.in_h1, newBot.h1_h2, newBot.h2_out = np.copy(currentWeights[0]), np.copy(currentWeights[1]), np.copy(currentWeights[2])
        newBot.changeWeightsABit()

        while not newBot.snek.isColliding() and newBot.lifetime < 500:
            newBot.tick()

        score = newBot.score * newBot.snek.size + newBot.lifetime

        j = 0
        found = False
        while j < (len(topWeights)) and not found and j <= generationSize / 10:
            if(score > topScores[j]):
                topScores.insert(j, score)
                topWeights.insert(j, [np.copy(newBot.in_h1),np.copy(newBot.h1_h2),np.copy(newBot.h2_out)])
                found = True
            j += 1

        avg += score

    avg /= generationSize

    # Pick 2 random weights from the top x%
    x, y = np.random.randint(0, 5), np.random.randint(0, 5)
    parent1 = topWeights[x]
    parent2 = topWeights[y]
    currentWeights = [np.copy(parent1[0]), np.copy(parent2[1]), np.copy(parent1[2])]
    if(x > y):
        currentWeights[2] = np.copy(parent2[2])

    if generation % 100 == 0:
        np.savez(open("weights\\gen"+str(generation)+".npy", 'wb'), currentWeights[0], currentWeights[1], currentWeights[2])

    sys.stdout.write("Generation: " + str(generation) + ' \n')
    sys.stdout.write("Best GenScore: " + str(topScores[0]) + '   \n')
    sys.stdout.write("Avg score: " + str(avg) + '    \r\033[A\033[A')

    if(generation % 100 == 0):


    generation += 1


newBot.reset
newBot.startWatching()
print("\n\n\n\n")
while not newBot.snek.isColliding() and newBot.lifetime < 200:
    newBot.tick()
    print(newBot.score)