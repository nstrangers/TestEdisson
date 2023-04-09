from random import randint

class User:
    def __init__(self, answer=None):
        if answer is None:
            answer = []
        self.answer = answer

    def add_answer(self, answer):
        self.answer.append(answer)

class Person:
    def __init__(self, rating=50,  guess=None):
        if guess is None:
            guess = []
        self.guess = guess
        self.rating = rating

    def add_guess(self):
        guess = randint(10, 99)
        self.guess.append(guess)

    def change_rating(self, answer):
        if answer == self.guess[-1]:
            self.rating += 1
        else:
            self.rating -= 1

