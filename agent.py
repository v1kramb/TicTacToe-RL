import random

class Player:
    """Superclass for all players"""
    def __init__(self): pass
    def move(self, board): pass
    def reward(self, val, board): pass
    def available_moves(self, board):
        return [i for i in range(0, len(board) * len(board)) if board[i] == "-"]

class HumanPlayer(Player):
    def __init__(self):
        self.breed = "Human"
    
    def move(self, board):
        return int(input("Your move: "))

    def reward(self, val, board):
        print(f"{self.breed} earned: {val}")

class QLearningPlayer(Player):
    def __init__(self, epsilon, alpha, gamma):
        self.breed = "Q"
        self.q = dict() # Q-table
        self.epsilon = epsilon # chance for random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor

    def move(self, board):
        pass

    def reward(self, val, board):
        pass

    def learn(self, state, action, reward, result_state):
        pass