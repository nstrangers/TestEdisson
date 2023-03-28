class User:
    def __init__(self, answer=None):
        if answer is None:
            answer=[]
        self.answer = answer

    def add_answer(self, answer):
        self.answer.append(answer)


class Person(User):
    def __init__(self, rating=50):
        super().__init__()
        self.rating = rating

    def match(self, madeup, solution):
        if madeup == solution:
            self.rating += 1
        else:
            self.rating -= 1