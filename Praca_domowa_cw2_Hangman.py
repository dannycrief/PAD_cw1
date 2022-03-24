class Game:
    PLAYERS = [1, 2]
    LANGUAGES = ["EN", "PL"]
    LEVELS = {
        "low": 8,
        "medium": 5,
        "hard": 3
    }

    def __init__(self, level, language, players_number):
        self.level = level
        self.language = language
        self.players_number = players_number

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        if type(level) is str:
            if level in self.LEVELS.keys():
                self._level = self.LEVELS[level]
            else:
                raise Exception("Invalid level parameter: {0}. Acceptable is: ".format(level, self.LEVELS.keys()))
        elif type(level) is int:
            self._level = level
        else:
            raise Exception("Invalid level parameter: {0}. Acceptable is: ".format(level, self.LEVELS.keys()))

    @property
    def players_number(self):
        return self._players_number

    @players_number.setter
    def players_number(self, players_number):
        if players_number in self.PLAYERS:
            self._players_number = players_number
        else:
            raise Exception("Invalid players_number parameter: {0}".format(players_number))

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        if language in self.LANGUAGES:
            self._language = language
        else:
            raise Exception("Invalid language parameter: {0}. Acceptable is {1}".format(language, self.LANGUAGES))

    def _play(self):
        print(
            "***********************************\n"
            "***********************************\n"
            "*** Welcome to the Game Hangman ***\n"
            "***********************************\n"
            "***********************************\n"
        )
        print(self.level)
        print(self.language)
        print(self.players_number)
        if self.players_number == 2:
            self.GUESS_WORD = input("Player 1, type ques word:\n").lower()


class Hangman(Game):
    GUESS_WORD = ""
    HIDDEN_GUESS_WORD = ""

    def __init__(self, level, language, players_number):
        super().__init__(level, language, players_number)

    def start(self):
        super()._play()
        self.HIDDEN_GUESS_WORD = self.hide_guess_word(self.GUESS_WORD)
        while self.level != 0:
            print(self.HIDDEN_GUESS_WORD)
            user_input = input("Type letter: ").lower()
            if user_input not in self.GUESS_WORD or len(user_input) == 0:
                print("NO. Try again")
                self.level -= 1
            else:
                print("Yep. You did it :) Go ahead!")
        if self.level == 0:
            print("You loose :(")

    @staticmethod
    def hide_guess_word(word):
        return "_" * len(word)


Hangman(level="low", language="EN", players_number=2).start()
