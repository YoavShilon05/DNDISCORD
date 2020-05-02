class Player:

    def __init__(self, author, nickname):

        self.author = author
        self.nickname = nickname
        self.characters = []
        self.character = None

    def AddCharacter(self, character):
        self.characters.append(character)