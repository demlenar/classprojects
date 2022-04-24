"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

import random
moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Player:

    def __init__(self):
        self.my_move = ""
        self.their_move = ""

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        self.my_move = my_move
        self.their_move = their_move


class RandomPlayer(Player):

    def move(self):
        return random.choice(moves)

    def learn(self):
        pass


class HumanPlayer(Player):

    def move(self):
        move = input("Rock, paper, scissors? > ").lower()
        while move not in moves:
            move = input("Please try again: rock, paper, scissors? > ").lower()
        print(f"You played {move}.")
        return move


class ReflectPlayer(Player):

    def move(self):
        if self.their_move in moves:
            return self.their_move
        else:
            return random.choice(moves)


class CyclePlayer(Player):

    def move(self):
        if self.my_move == "":
            return random.choice(moves)
        elif self.my_move in moves:
            index = moves.index(self.my_move)
            return moves[index-1]
        else:
            print("error")


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.counter1 = 0
        self.counter2 = 0

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        if beats(move1, move2):
            self.counter1 += 1
            print("Player 1 Wins!")
        elif move1 == move2:
            print("It's a draw! No points awarded.")
            pass
        elif not beats(move1, move2):
            self.counter2 += 1
            print("Player 2 Wins!")
        print(f"Current Score: [Player 1 | {self.counter1} - {self.counter2} "
              "| Player 2]\n")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        print("Welcome to Roshambo! First to win 2 rounds is the victor!\n")
        round = 0
        while self.counter1 < 2 and self.counter2 < 2:
            round += 1
            print(f"Round {round}:")
            self.play_round()
        if self.counter1 == 2:
            print("Player 1 wins!")
        elif self.counter2 == 2:
            print("Player 2 wins!")
        print("Game over!")


if __name__ == '__main__':
    game = Game(HumanPlayer(), CyclePlayer())
    game.play_game()
