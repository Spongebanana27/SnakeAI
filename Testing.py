import SnakeBot

bot = SnakeBot.SnakeBot()
bot.generateRandomWeights()
bot.loadWeights(open("weights\\gen499.npy", 'rb'))
bot.startWatching()
while not bot.snek.isColliding() and bot.lifetime < 200:
    bot.tick()
    print("---")