import random


class Game:
    PLAYERS = [1, 2]
    LANGUAGES = ["EN", "PL"]
    LEVELS = {
        "low": 8,
        "medium": 5,
        "hard": 3
    }

    vocabulary = {
        "guess_word": {
            "EN": "Guess a word :)",
            "PL": "Zgadnij słowo :)"
        },
        "get_u1_word": {
            "EN": "Player 1, type a word to guess:\n",
            "PL": "Gracz 1, wpisz słowo, do odgadywania:\n "
        },
        "get_character": {
            "EN": "Type letter:\n",
            "PL": "Podaj literę:\n"
        },
        "try_again": {
            "EN": "NO.Try again",
            "PL": "NIE. Spróbuj ponownie."
        },
        "correct_answer": {
            "EN": "Yep. You did it :) That letter is correct. Go on!",
            "PL": "Yep. Udało Ci się :) Ta litera jest poprawna. Idź dalej!"
        },
        "the_end_won": {
            "EN": "You won :)",
            "PL": "Wygrałeś :)"
        },
        "the_end_lost": {
            "EN": "You lost :(",
            "PL": "Przegrałeś :("
        }
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
            "           {0}".format(self.vocabulary['guess_word'][self.language])
        )


class Hangman(Game):
    GUESS_WORD = ""
    HIDDEN_GUESS_WORD = ""
    GUESS_WORDS_LIST = ["trulala", "secret", "something", "boy"]

    def __init__(self, level, language, players_number):
        super().__init__(level, language, players_number)

    def start(self):
        super()._play()
        if self.players_number == 2:
            self.GUESS_WORD = input(self.vocabulary['get_u1_word'][self.language]).lower()
        else:
            self.GUESS_WORD = random.choice(self.GUESS_WORDS_LIST)

        self.HIDDEN_GUESS_WORD = self.hide_guess_word(self.GUESS_WORD)

        while self.level != 0:
            print(self.HIDDEN_GUESS_WORD)
            user_input = input(self.vocabulary['get_character'][self.language]).lower()
            if user_input not in self.GUESS_WORD or len(user_input) == 0:
                print(self.vocabulary['try_again'][self.language])
                self.level -= 1
            else:
                self.HIDDEN_GUESS_WORD = self.show_letter(user_input)
                print(self.vocabulary['correct_answer'][self.language])
            if self.GUESS_WORD == self.HIDDEN_GUESS_WORD:
                print(self.vocabulary['the_end_won'][self.language])
                break
        if self.level == 0:
            print(self.vocabulary['the_end_lost'][self.language])

    @staticmethod
    def hide_guess_word(word):
        return "_" * len(word)

    def show_letter(self, letter):
        word = self.HIDDEN_GUESS_WORD
        idx_list = [pos for pos, char in enumerate(self.GUESS_WORD) if char == letter]
        for i in idx_list:
            word = word[:i] + letter + word[i + 1:]
        return word


Hangman(level="hard", language="PL", players_number=1).start()
