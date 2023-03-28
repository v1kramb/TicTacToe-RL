from game import TicTacToe
from agent import *

N = 3
NUM_GAMES = 100

p1 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)
p2 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)

for i in range(1, NUM_GAMES + 1):
    print(f"Game #{i}")
    game = TicTacToe(n=N, p1=p1, p2=p2, tie_reward=0.5)
    game.run()
