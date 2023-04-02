class User:
    def __init__(self, answer=None):
        if answer is None:
            answer = []
        self.answer = answer

    def add_answer(self, answer):
        self.answer.append(answer)

    def validate_answer(self, answer):
        if not isinstance(answer, int):
            raise TypeError("Answer must be an integer.")
        if answer < 10 or answer > 99:
            raise ValueError("Аnswer must be between 10 and 99")


class Person(User):
    def __init__(self, rating=50):
        super().__init__()
        self.rating = rating

    def match(self, madeup, solution):
        if madeup == solution:
            self.rating += 1
        else:
            self.rating -= 1
