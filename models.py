class User:
    def __init__(self):
        self.answer = []

    def add_answer(self, answer):
        self.answer.append(answer)


class Person(User):
    def __init__(self):
        super().__init__()
        self.rating = 50

    def match(self, madeup, solution):
        if madeup == solution:
            self.rating += 1
        else:
            self.rating -= 1