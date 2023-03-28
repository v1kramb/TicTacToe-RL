import random
from agent import *

class TicTacToe:
    """Game class, works for any NxN board."""
    def __init__(self, n=3, p1=Player(), p2=Player(), tie_reward=0.2):
        self.n = n
        self.board = ['-'] * n * n
        self.p1, self.p2 = p1, p2
        self.p1_turn = random.choice([True, False])
        self.tie_reward = tie_reward

        # Generate win_sets
        self.win_sets = []
        for i in range(0, n * n, n): # rows
            self.win_sets.append([j for j in range(i, i + n)])
        for i in range(n): # columns
            self.win_sets.append([j for j in range(i, n * n, n)])
        self.win_sets.append([i for i in range(0, n * n, n + 1)]) # diagonal
        self.win_sets.append([i for i in range(n - 1, (n * n) - 1, n - 1)]) # anti-diagonal

    def print_board(self):
        print_list = [i for i in range(self.n - 1, self.n * self.n, self.n)]

        for idx, piece in enumerate(self.board):
            print(piece, end=" ")
            if idx in print_list: print()

    def win_test(self, char):
        for win_set in self.win_sets:
            count = 0
            for i in range(len(win_set)):
                if char == self.board[win_set[i]]:
                    count += 1
                else:
                    break
            if count == self.n:
                return True
        return False

    def board_filled(self):
        return '-' not in self.board

    def run(self):
        while True:
            # Set player
            player, char, other = self.p2, 'O', self.p1
            if self.p1_turn:
                player, char, other = self.p1, 'X', self.p2
            
            if player.breed == "Human": self.print_board()

            move = player.move(self.board)

            # Check for invalid move for human player
            if move < 0 or move > ((self.n ** 2) - 1) or self.board[move] != '-':
                player.reward(-1000, self.board)
                break

            self.board[move] = char
            
            # Game ends
            if self.win_test(char):
                player.reward(1, self.board)
                other.reward(-1, self.board)
                break
            if self.board_filled():
                player.reward(self.tie_reward, self.board)
                other.reward(self.tie_reward, self.board)

            self.p1_turn = not self.p1_turn
