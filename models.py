class Person():
    def __init__(self):
        self.answer = []
        self.rating = 50

    def add_answer(self, answer):
        self.answer.append(answer)

    def match(self, made_up, solution):
        if made_up == solution:
            self.rating += 1
        else:
            self.rating -= 1