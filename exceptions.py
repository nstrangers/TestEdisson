class InvalidAnswer(Exception):
    def __init__(self, error_massage):
        self.error_message = error_massage

    def __str__(self):
        return self.error_message
