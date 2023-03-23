import random

# Game class
class TicTacToe:
    def __init__(self, p1, p2):
        self.board = ['-'] * 9
        self.p1, self.p2 = p1, p2
        self.p1_turn = random.choice([True, False])

    def print_board(self):
        for idx, piece in enumerate(self.board):
            print(piece, end=" ")
            if idx in [2, 5, 8]: print()

    def get_board_state(self):
        pass

    def is_board_filled(self):
        return '-' not in self.board

    def run(self):
        pass

# Players
class Player:
    def __init__(self):
        self.breed = "Random"
    
    def start(self):
        pass

    def move(self, board):
        pass

class HumanPlayer(Player):
    def __init__(self):
        self.breed = "Human"

class QLearningPlayer(Player):
    def __init__(self):
        self.breed = "Q"

    def update(self):
        pass


game = TicTacToe(Player(), Player())
game.print_board()
print(game.is_board_filled())