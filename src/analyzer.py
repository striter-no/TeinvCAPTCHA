import src.gpt_source as gpt

class Person:
    def __init__(
            self
    ):
        pass

class Analysier:
    def __init__(self, gpt_chat: gpt.Chat):
        self.gpt_chat = gpt_chat

    def load_info(self, path: str):
        pass

    def analysie_all(self):
        pass

    def analysie_person(self, data):
        pass