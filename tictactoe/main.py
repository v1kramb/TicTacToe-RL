from game import TicTacToe
from agent import *
import matplotlib.pyplot as plt

N = 5  # NxN board size
NUM_EPISODES = 100000

p1 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)
p2 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)

# Training sequence
y = []
for i in range(1, NUM_EPISODES + 1):
    # print(f"Game #{i}")
    game = TicTacToe(n=N, p1=p1, p2=p2, tie_reward=0.5)
    game.run()
    y.append(len(p1.q)) # append size of q-dict

# Graph episodes
x = [i for i in range(NUM_EPISODES)]
plt.plot(x, y, '--')
plt.title('Action Space vs Episodes for Traditional Q-learning')
plt.xlabel('# of episodes')
plt.ylabel('# of State Space')
plt.show()
