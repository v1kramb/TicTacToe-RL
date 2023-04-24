from game import TicTacToe
from agent import *
import matplotlib.pyplot as plt

N = 5  # NxN board size
NUM_EPISODES = 100000

p1 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)
p2 = QLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9)
p3 = ImprovedQLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9, char='X')
p4 = ImprovedQLearningPlayer(n=N, epsilon=0.2, alpha=0.3, gamma=0.9, char='O')

# Training sequence
space_sizes = []
space_sizes2 = []
accumulated_wins = []
accumulated_wins2 = []
win_count = 0
win_count2 = 0
for i in range(1, NUM_EPISODES + 1):
    # print(f"Game #{i}")
    game = TicTacToe(n=N, p1=p1, p2=p2, tie_reward=0.5, set_turn=True)
    winner = game.run()

    space_sizes.append(len(p2.q)) # append size of state x action space for player 2
    if winner == 'O':
        win_count += 1
    accumulated_wins.append(win_count)

    game2 = TicTacToe(n=N, p1=p3, p2=p4, tie_reward=0.5, set_turn=True)
    winner2 = game2.run()

    space_sizes2.append(len(p4.q))
    if winner2 == 'O':
        win_count2 += 1
    accumulated_wins2.append(win_count2)
    

# Graph episodes
x = [i for i in range(NUM_EPISODES)]
plt.plot(x, space_sizes, '--')
plt.title('State Space vs Episodes for Traditional Q-learning')
plt.xlabel('# of episodes')
plt.ylabel('# of State Space')
plt.show()

plt.plot(x, space_sizes2)
plt.title('State Space vs Episodes for Proposed Method')
plt.xlabel('# of episodes')
plt.ylabel('# of State Space')
plt.show()


plt.plot(x, space_sizes, '--')
plt.plot(x, space_sizes2)
plt.title('State Space vs Episodes')
plt.xlabel('# of episodes')
plt.ylabel('# of State Space')
plt.legend(["traditional q-learning", "proposed method"])
plt.show()

plt.plot(x, accumulated_wins, '--')
plt.plot(x, accumulated_wins2)
plt.title('Accumulated Wins vs Training Count for Traditional Q-learning')
plt.xlabel('Training Count')
plt.ylabel('Accumulated Count of Wins')
plt.legend(["traditional q-learning", "proposed method"])
plt.show()