import random

class Player:
    """Superclass for all players"""
    def __init__(self): pass
    def move(self, board): pass
    def reward(self, val, board): pass
    def available_moves(self, board):
        return [i for i in range(0, len(board)) if board[i] == '-']

class HumanPlayer(Player):
    def __init__(self):
        self.breed = "Human"
    
    def move(self, board):
        return int(input("Your move: "))

    def reward(self, val, board):
        print(f"{self.breed} earned: {val}")

class QLearningPlayer(Player):
    def __init__(self, n, epsilon, alpha, gamma):
        self.breed = "Q"
        self.q = dict() # Q-table, key = (state, action)
        self.epsilon = epsilon # chance for random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor
        self.last_move = None
        self.last_board = ['-'] * n * n

    def getQ(self, state, action):
        if (state, action) not in self.q:
            self.q[(state, action)] = 1.0
        return self.q[(state, action)]

    def move(self, board):
        self.last_board = tuple(board)
        actions = self.available_moves(board)

        if random.random() < self.epsilon:
            self.last_move = random.choice(actions)
            return self.last_move

        qs = [self.getQ(self.last_board, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1: # choose randomly among multiple top options
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = actions[i]
        return actions[i]

    def reward(self, val, board):
        if self.last_move: self.learn(self.last_board, self.last_move, val, tuple(board))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(result_state)])
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev) # traditional update rule

