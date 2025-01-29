"""
Module providing game-related classes.

So far, only one class is available:

- WordGuessingGame: Implements a word-guessing game

"""

from enum import Enum
from random import randint
from random import choice
import string

class Temp(Enum):
    CORRECT = 0
    EXTREMELY_HOT = 1 # within three years
    VERY_HOT = 2 # within four to ten years
    KINDA_HOT = 3 # within eleven to twenty-five years
    LUKEWARM = 4 # within twenty-six to fifty years
    KINDA_COLD = 5 # within fifty-one to one hundred years
    VERY_COLD = 6 # within one hundred to two hundred fifty years
    EXTREMELY_COLD = 7 # beyond two hundred fifty years off

class Question:
    """
    A question for HotOrColdGolf.

    Attributes:
        _par: The par of the question.
        _question: The text of the question itself.
        _answer: The correct year.
    """
    _par: int
    _question: str
    _answer: int

    def __init__(self, par: int, question: str, answer: int):
        """
        Constructor

        Args:
            par: Par of the question
            question: Text of the question
            answer: Answer to the question
        """
        self._par = par
        self._question = question
        self._answer = answer

    @property
    def par(self) -> int:
        """
        Returns: The par of the question
        """
        return self._par
    
    @property
    def question(self) -> str:
        """
        Returns: The text of the question
        """
        return self._question
    
    @property
    def answer(self) -> int:
        """
        Returns: The answer to the question
        """
        return self._answer
    
    def evaluate_guess(self, guess: int) -> int:
        """
        Determines how close a given
        guess is to the correct answer.

        Args:
            guess: the year guessed

        Returns:
            The Temp enum corresponding
            to how close the guess is
        """
        off_by = abs(self.answer - guess)
        if (off_by == 0):
            return Temp.CORRECT
        elif (off_by <= 3):
            return Temp.EXTREMELY_HOT
        elif (off_by <= 10):
            return Temp.VERY_HOT
        elif (off_by <= 25):
            return Temp.KINDA_HOT
        elif (off_by <= 50):
            return Temp.LUKEWARM
        elif (off_by <= 100):
            return Temp.KINDA_COLD
        elif (off_by <= 250):
            return Temp.VERY_COLD
        else:
            return Temp.EXTREMELY_COLD


class Club:
    """
    A club for HotOrColdGolf.

    Attributes:
        _name: The name of the club.
        _range: The range of the club in years.
        _accuracy: The plus/minus accuracy of the club.
    """
    _name: str
    _range: int
    _accuracy: int
    _is_sand_wedge: bool

    def __init__(self, name: str, range: int, accuracy: int,
                 is_sand_wedge: bool = False):
        """
        Constructor

        Args:
            name: The name of the club.
            range: The range of the club in years.
            accuracy: The plus/minus accuracy of the club.
        """
        self._name = name
        self._range = range
        self._accuracy = accuracy
        self._is_sand_wedge = is_sand_wedge

    @property
    def name(self) -> str:
        """
        Returns: The name of the club
        """
        return self._name
    
    @property
    def range(self) -> int:
        """
        Returns: The trange of the club
        """
        return self._range
    
    @property
    def accuracy(self) -> int:
        """
        Returns: The plus/minus accuracy of the club
        """
        return self._accuracy
    
    @property
    def is_sand_wedge(self) -> bool:
        """
        Returns: Whether the club is a sand wedge
        """
        return self._is_sand_wedge
    
    def swing(self, start: int, target: int, in_bunker: bool) -> int:
        """
        Return a year after hitting from
        a start year with this club.

        Args:
            start: the starting year
            target: the target year

        Returns:
            The end year
        """
        if (abs(start - target) > self.range):
            raise ValueError('That target is beyond the range of this club!')
        else:
            if (in_bunker and not self.is_sand_wedge):
                minimum = start - 10
                maximum = start + 10
            else:
                minimum = start - self.range
                maximum = start + self.range

            if target > start:
                return max(start, min(maximum, target +
                                      randint(-self.accuracy,self.accuracy)))
            elif target < start:
                return min(start, max(minimum, target +
                                      randint(-self.accuracy,self.accuracy)))
            else:
                return target
            
    def __str__(self) -> str:
        """
        Returns: A string representation of the club
        """
        str_range = "Range: " + str(self.range)
        str_accuracy = "Accuracy: " + str(self.accuracy)
        return self.name + " - (" + str_range + ", " + str_accuracy + ")"


class HotOrColdGolf:
    """
    Class for a history trivia hot or cold golf game. In this game,
    we ask a question with a certain year in mind as an answer.

    The player starts at the year 0. They can use different
    clubs with a varying degree of ranges and accuracies, such as
    a putter that lands them to exactly the year they guess but only
    within a decade, or a driver that can move them up to a thousand
    years away, but plus or minus two hundred years.

    Each guess, the game tells them how "hot" or "cold" they are from
    the target; it also tells them where they using golf metaphors
    ("on the green", "on the fairway", etc).

    Each hole has a par, and some intervals are bunkers (the Black Death,
    World Wars, etc) that make it hard to get out of once you're in them.

    The game ends when the player reaches the target year, at which point
    they can choose to play again with a different question or to stop.

    Attributes:
        _golf_bag: Set of all the clubs
        _question_bag: Set of all the questions
        _curr_club: Current club used
        _curr_question: Current question used
        _curr_year: Current year
        _num_guesses: Number of guesses so far
    """

    _golf_bag: list[Club]
    _question_bag: set[Question]
    _curr_club: Club
    _curr_question: Question
    _curr_year: int
    _num_guesses: int
    _in_bunker: bool

    def __init__(self):
        """
        Constructor

        Initializes the game with a set of clubs and questions.
        """
        driver = Club("Driver", 1000, 200)
        three_wood = Club("3_Wood", 500, 100)
        five_wood = Club("5_Wood", 250, 50)
        three_iron = Club("3_Iron", 200, 40)
        four_iron = Club("4_Iron", 175, 35)
        five_iron = Club("5_Iron", 150, 30)
        six_iron = Club("6_Iron", 125, 25)
        seven_iron = Club("7_Iron", 100, 20)
        eight_iron = Club("8_Iron", 75, 15)
        nine_iron = Club("9_Iron", 50, 10)
        pitching_wedge = Club("Pitching_Wedge", 25, 5)
        sand_wedge = Club("Sand_Wedge", 50, 25, True)
        putter = Club("Putter", 10, 1)
        self._golf_bag = [driver, three_wood, five_wood, three_iron, four_iron,
                          five_iron, six_iron, seven_iron, eight_iron,
                          nine_iron, pitching_wedge, sand_wedge, putter]
        
        henry_vii = Question(11, "This year saw the coronation of the king who would divorce, behead, and eventually... die!", 1509)
        charles_ii = Question(7, "This year saw the restoration of the 'one hundred percent party animal', also known as the King of Bling.", 1660)
        george_iv = Question(13, "This year saw the coronation of 'the fat one.'", 1820)
        world_war_one = Question(9, "This year, František and Stanislav flew sortie after sortie!", 1940)
        owen_glyndwr = Question(8, "This year, a Welsh noble rose up against England! (Also, Baron Grey De Ruthen spread untrue things about him.)", 1400)
        self._question_bag = {henry_vii, charles_ii, george_iv, world_war_one, owen_glyndwr}

        self._curr_club = driver
        self._curr_question = choice(list(self._question_bag))
        self._curr_year = 0
        self._num_guesses = 0
        self._in_bunker = False
    
    @property
    def curr_club(self) -> Club:
        """
        Returns: The current club
        """
        return self._curr_club
    
    @property
    def curr_question(self) -> Question:
        """
        Returns: The current question
        """
        return self._curr_question
    
    @property
    def curr_year(self) -> int:
        """
        Returns: The current year
        """
        return self._curr_year
    
    @property
    def num_guesses(self) -> int:
        """
        Returns: The number of guesses
        """
        return self._num_guesses
    
    @property
    def in_bunker(self) -> bool:
        """
        Returns: Whether the player is in a bunker
        """
        return self._in_bunker
    
    def change_club(self, club: Club) -> None:
        """
        Changes the current club.

        Args:
            club: The new club
        """
        self._curr_club = club

    def help(self) -> None:
        """
        Prints help menu and commands for the game
        """
        print("Welcome to Hot or Cold Golf!")
        print("The goal of this game is to guess the year of a historical event.")
        print("You start at year 0 and must use different clubs to get to the target year.")
        print("Each club has a range and accuracy, and some clubs are better in certain situations.")
        print("You can use the following commands:")
        print("help: Print this help menu")
        print("clubs: Print the clubs in your bag")
        print("question: Print the current question")
        print("year: Print the current year")
        print("target <year>: Target a year")
        print("club <club>: Change your current club (remember to include underscores!)")
        print("quit: Quit the game")
        print("\n\n")

    def print_clubs(self) -> None:
        """
        Prints the clubs in the player's bag
        """
        print("Clubs in your bag:")
        for club in self._golf_bag:
            print(club)

    def print_question(self) -> None:
        """
        Prints the current question
        """
        print(self.curr_question.question)

    def print_year(self) -> None:
        """
        Prints the current year
        """
        print("Current year:", self.curr_year)

    def guess(self, target: int) -> None:
        """
        Guesses a year and evaluates the guess

        Args:
            target: The year guessed
        """
        self._num_guesses += 1
        try:
            actual = self.curr_club.swing(self.curr_year, target, self.in_bunker)
        except ValueError as e:
            print(e)
            return
        result = self.curr_question.evaluate_guess(actual)
        bunker_intervals = {(1347, 1351), (1914, 1918), (1939, 1945)}
        for bunker in bunker_intervals:
            if (bunker[0] <= actual <= bunker[1]):
                self._in_bunker = True
                print("Oh no, you're in a bunker! Use a sand wedge to escape!")
                break
            else:
                self._in_bunker = False
        print("You swung with the", self.curr_club.name, "and landed in the year", actual)
        self._curr_year = actual
        if (result == Temp.CORRECT):
            print("Correct! You guessed the year in", self.num_guesses, "guesses!")
            print("The par for this question was", self.curr_question.par)
            print("You scored", self.curr_question.par - self.num_guesses, "points!")
            print("See you next time!")
            exit(0)
        elif (result == Temp.EXTREMELY_HOT):
            print("HOT HOT HOT!")
        elif (result == Temp.VERY_HOT):
            print("Burning hot!")
        elif (result == Temp.KINDA_HOT):
            print("Hot!")
        elif (result == Temp.LUKEWARM):
            print("Warm!")
        elif (result == Temp.KINDA_COLD):
            print("Cold...")
        elif (result == Temp.VERY_COLD):
            print("Freezing cold...")
        elif (result == Temp.EXTREMELY_COLD):
            print("We're going to freeze to death...")

def main():
    """
    Main function for HotOrColdGolf
    """
    game = HotOrColdGolf()
    game.help()
    print("Your current club is: ", str(game.curr_club), "\n")
    print("Your question is: ", game.curr_question.question)
    print("Par for this question is: ", game.curr_question.par, "\n")
    print("The current year is: ", game.curr_year, "\n")
    print("Good luck!")
    while True:
        command = input("Enter a command: ")
        if (command == "help"):
            game.help()
        elif (command == "clubs"):
            game.print_clubs()
        elif (command == "question"):
            game.print_question()
        elif (command == "year"):
            game.print_year()
        elif (command.startswith("target ")):
            try:
                year = int(command.split(" ")[1])
                game.guess(year)
            except ValueError:
                print("Invalid year!")
        elif (command.startswith("club ")):
            club_name = command.split(" ")[1]
            found = False
            for club in game._golf_bag:
                if (club.name.lower() == club_name.lower()):
                    game.change_club(club)
                    print("Changed club to", club.name)
                    found = True
                    break
            if (not found):
                print("Club not found!")
        elif (command == "quit"):
            print("Thanks for playing!")
            break
        else:
            print("Invalid command!")

if __name__ == "__main__":
    main()