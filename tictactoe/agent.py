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
        self.n = n
        self.last_board = ['-'] * n * n

    def getQ(self, state, action):
        if (state, action) not in self.q:
            self.q[(state, action)] = 1.0
        return self.q[(state, action)]

    def move(self, board):
        self.last_board = tuple(board)
        actions = self.available_moves(board)

        if random.random() < self.epsilon:  # epsilon-greedy
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
        maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(state)])
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev) # traditional update rule

class ImprovedQLearningPlayer(QLearningPlayer):
    """Uses action space reduction method proposed in Woo & Sung (2020)
        - Only track state space for first four turns, compute the fifth automatically
        - g(a_t), h(s_t)
        - Reduce action space to actions within a particular distance from existing marks
    """
    def __init__(self, n, epsilon, alpha, gamma, char):
        super().__init__(n, epsilon, alpha, gamma)
        self.char = char

        # Generate win_sets (taken from game.py)
        self.win_sets = []
        for i in range(0, n * n, n): # rows
            self.win_sets.append([j for j in range(i, i + n)])
        for i in range(n): # columns
            self.win_sets.append([j for j in range(i, n * n, n)])
        self.win_sets.append([i for i in range(0, n * n, n + 1)]) # diagonal
        self.win_sets.append([i for i in range(n - 1, (n * n) - 1, n - 1)]) # anti-diagonal

    """Returns the spatial data of a possible action"""
    def g(self, state): # the action has already been played
        distance_board = [100] * len(state)

        # Go through existing positions, find neighbors
        # Shortcut: only evaluate immediate neighbors instead of generating entire distance board
        for i in range(len(state)):
            if state[i] != '-':
                distance_board[i] = 0

                # Up/down
                up = i - self.n
                if up >= 0: 
                    distance_board[up] = min(1, distance_board[up])
                down = i + self.n
                if down < self.n * self.n:
                    distance_board[down] = min(1, distance_board[down])

                # Left/right
                left = i - 1
                if left % self.n != self.n - 1:
                    distance_board[left] = min(1, distance_board[left])
                right = i + 1
                if right % self.n != 0:
                    distance_board[right] = min(1, distance_board[right])

                # Diagonal
                diag = i + self.n + 1
                if diag % self.n != 0 and diag < self.n * self.n:
                    distance_board[diag] = min(1.4, distance_board[diag])
                diag2 = i - self.n - 1
                if diag2 % self.n != self.n - 1 and diag2 >= 0:
                    distance_board[diag2] = min(1.4, distance_board[diag2])

                # Anti-diagonal
                antidiag = i - self.n + 1
                if antidiag % self.n != 0 and antidiag >= 0:
                    distance_board[antidiag] = min(1.4, distance_board[antidiag])
                antidiag2 = i + self.n - 1
                if antidiag2 % self.n != self.n - 1 and antidiag2 < self.n * self.n:
                    distance_board[antidiag2] = min(1.4, distance_board[antidiag2])

        return distance_board

    """Returns possible spatial data on a particular state"""
    def h(self, state):
        distance_board = tuple(self.g(state))
        return [i for i in range(len(distance_board)) if distance_board[i] < 1.414]

    """Overridden from Player superclass"""
    def available_moves(self, board):
        moves = self.h(board)
        if len(moves) == 0: # first turn
            moves = super().available_moves(board)
        return moves

    def win_test(self, char, board):
        for win_set in self.win_sets:
            count = 0
            for i in range(len(win_set)):
                if char == board[win_set[i]]:
                    count += 1
                else:
                    break
            if count == self.n:
                return True
        return False

    """Modified to only compute four moves + one manual for fifth.
    Hardcoded for the purposes on benchmarking."""
    def move(self, board):
        self.last_board = tuple(board)

        actions = self.available_moves(board)

        # Check if we're on turn 5
        if len(self.last_board) - self.last_board.count('-') == 4:
            # Attempt to compute best action manually
            board = list(self.last_board)
            for action in actions:
                board[action] = self.char
                if self.win_test(self.char, board):
                    return action
                board[action] = '-'
            return -0.5

        if random.random() < self.epsilon:  # epsilon-greedy
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