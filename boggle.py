##############################################################################
#                                   Imports                                  #
##############################################################################
import tkinter as tk
import tkinter.messagebox
import pygame
from boggle_utils import *
from boggle_board_randomizer import randomize_board

##############################################################################
#                                  Typing                                    #
##############################################################################
from typing import Dict, Any, Tuple, List, Union
StrVar = Any
Cube = Any
Board = List[List[str]]
Path = List[Tuple[int, int]]

##############################################################################
#                                  Constants                                 #
##############################################################################
GAME_TIME = "03:00"
BOARD_SIZE = 4

##############################################################################
#                                  Functions                                 #
##############################################################################


class GUI:
    """ This class will run the gui of the game "boggle".
    The game has a board, a time countdown, a point counter and
    a list of words that were already found.
    The player chooses words nby dragging the mouse on cells in the board. """

    def __init__(self) -> None:
        """ This will create all the instances of the game,
        including all GUI objects and their graphics.
        when program is ran this will appear, and pressing the start button
        will activate a game.
        game can be activated as many times as we want. """

        # create window:
        self.__root = tk.Tk()
        self.__root.title("Boggle")
        self.__root.geometry("1000x700")

        # create start button
        self.__start_button = tk.Button(self.__root, text="Start",
                                        font=("Courier", 30), bg="red",
                                        width=10, height=1)
        self.__start_button.place(x=400, y=500)

        # quit button:
        self.__quit_button = tk.Button(self.__root, text="I Quit",
                                       font=("Courier", 15), bg="black",
                                       fg="white", height=1, width=5)
        self.__quit_button.place(x=900, y=650)

        # create game objects:
        self.__board = tk.Frame(self.__root, height=200, width=300,)
        self.__board.place(x=350, y=125)
        self.__board_list: Board = [[""]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.__var_dict: Dict[Cube, Tuple[Tuple[int, int], StrVar]] = {}
        self.__path: List[Tuple[int, int]] = []
        for i in range(len(self.__board_list)):
            for j in range(len(self.__board_list[0])):
                self._var: StrVar = tk.StringVar()  # create string var
                cube_tup: Tuple[int, int] = (i, j)  # create identifier (key)
                self._btn: Cube = tk.Button(self.__board, textvar=self._var,
                                            height=5, width=10, bg="black",
                                            font=("Courier", 10),
                                            fg="yellow")  # create button
                self._btn.grid(row=i, column=j)  # place button
                # save button and string var to dict with a key (location y,x):
                self.__var_dict[self._btn] = (cube_tup, self._var)
        for cube in self.__var_dict:
            cube.configure(command=lambda cube=cube:
                           self.update_path_word(cube))

        # countdown timer
        self.__timer = tk.Label(self.__root, width=8, height=3, bg="white",
                                fg="black")
        self.__timevar = tk.StringVar()
        self.__timevar.set(GAME_TIME)
        self.__timevar.trace("w", self._end_of_game)
        self.__timer.configure(textvar=self.__timevar)
        self.__timer.place(x=20, y=20)
        pygame.mixer.init()

        # score board
        self.__score_title = tk.StringVar()
        self.__score_title.set("Your Current Score: 0")
        self.__score = 0
        self.__previous_words: List[str] = []
        self.__prev_words_str = tk.StringVar()
        self.__prev_words_str.set("Already found: \n")
        self.__word_board = tk.Label(font=("Courier", 10),
                                     textvariable=self.__prev_words_str)
        self.__score_board = tk.Label(textvariable=self.__score_title,
                                      bg="gray", font=("Courier", 25))
        self.__score_board.place(x=275, y=50)
        self.__word_board.place(x=100, y=120)

        # current words:
        self.__current_word = tk.StringVar()
        self.__current_word_label = tk.Label(self.__root,
                                             bg="yellow", width=20,
                                             textvariable=self.__current_word)
        self.__current_word_label.place(x=440, y=100)
        self.__check_word = tk.Button(self.__root, text="Check answer",
                                      command=self._test_word,
                                      font=("Courier", 20), bg="yellow")
        self.__check_word.place(x=750, y=300)
        with open('boggle_dict.txt', 'r') as words:
            self.__all_words: Union[str, List[str]] = words.read()
            self.__all_words = sorted(self.__all_words.replace('\n',
                                                               ' ').split(' '))

        # game status identifiers:
        self.__game = False  # is false when user can start new game, else True
        self.__mouse_clicked = False  # this is used for the "drag" method

        # bind actions:
        self.__start_button.configure(command=self.start_game)
        self.__quit_button.configure(command=self._quit)

    def update_path_word(self, cube: Cube) -> None:
        """ Updates the current path and current word for further logic use """
        if self.__game:
            self.__path.append(self.__var_dict[cube][0])  # update path
            cur_word = self.__current_word.get()
            cur_word += self.__var_dict[cube][1].get()
            self.__current_word.set(cur_word)  # update word
    def play_sound(self, success: bool, *args: Any):
        """This function play sounds acording to success or loss of the player."""
        if success:
            pygame.mixer.music.load("success.mp3")
            pygame.mixer.music.play(loops=0)
        else:
            pygame.mixer.music.load("loss.mp3")
            pygame.mixer.music.play(loops=0)

    def _test_word(self, *args: Any) -> None:
        """ This function tests the path
        after the user decides it is complete """
        new_word = is_valid_path(self.__board_list, self.__path,
                                 self.__all_words)
        if new_word is not None and new_word not in self.__previous_words:
            # the word is legal and not find until now.
            # add the word to the list of the words already found:
            self.play_sound(True)
            self.__previous_words.append(new_word)
            current_score = self.__score + (len(self.__path)**2)
            self.update_score(current_score)
            self.update_prev_words()
        else:
            self.play_sound(False)
        self.__path = []  # update path to be empty for user to chose new word
        self.__current_word.set("")  # update word - same as path

    def timer(self) -> None:
        """ Starts a timer at 3 minutes and runs in until it hits 0.
        Writing will become red at the last 20 seconds.
        after 3 minutes the current game will start running. """
        if self.__game:
            time = self.__timevar.get()
            minutes: int = int(time[0:2])
            seconds: Union[int, str] = int(time[3:5])
            if seconds > 0:
                seconds -= 1
            else:
                minutes -= 1
                seconds = 59
            if seconds < 10:
                seconds = "0" + str(seconds)
            time = "0" + str(minutes) + ":" + str(seconds)
            self.__timevar.set(time)

            if minutes > -1:
                self.__root.after(1000, self.timer)
    
    def play_beep(self) -> None:
        """ Plays music at the last 10 seconds of the game """
        pygame.mixer.music.load("beep.mp3")
        pygame.mixer.music.play(loops=0)

    def _end_of_game(self, *args: Any) -> None:
        """ This function happens every time that the game timer value changes.
        at 40 seconds the digits turn red,
        and at 10 seconds there is a "beep" played. """
        last_10_sec: List[str] = ['00:10', '00:09', '00:08', '00:07', '00:06',
                                  '00:05', '00:04', '00:03', '00:02', '00:01']
        if self.__timevar.get() <= "00:40":
            self.__timer.configure(fg="red")
        if self.__timevar.get() in last_10_sec:
            self.play_beep()
        if self.__timevar.get() == "00:00":
            self.__game = False
            score_title: str = "Your Final Score: " + str(self.__score)
            self.__score_title.set(score_title)
            self.__timevar.set(GAME_TIME)
            self.__start_button.configure(bg="red")

    def _quit(self) -> None:
        """ quits the app. makes the user guilty for doing so. """
        result = tkinter.messagebox.askquestion("Don't quit",
                                                "Are you sure? We will miss you")
        if result == "yes":
            exit()
        else:
            pass

    def start_game(self) -> None:
        """ Starts running a Boggle game.
        Is the button is pressed while a game is running,
        the game will start over, with a new board. """
        if not self.__game:
            self.__game = True
            self.timer()
        else:
            self.__timevar.set(GAME_TIME)
        self.__timer.configure(fg="black")
        # configure the text to be "Game is On"
        self.__start_button.configure(text="Restart?", bg="white",
                                      font=("Courier", 25))
        self.get_random_board()

        # update score to be 0
        self.__score = 0
        self.update_score(self.__score)
        self.__path = []
        self.__current_word.set("")
        self.__previous_words = []
        self.update_prev_words()

    def get_random_board(self) -> None:
        """ changes the buttons to random letters
        based on the board randomizer """
        # create randomized board for game
        self.__board_list = randomize_board()
        for cube in self.__var_dict:
            i = self.__var_dict[cube][0][0]
            j = self.__var_dict[cube][0][1]
            self.__var_dict[cube][1].set(self.__board_list[i][j])

    def update_prev_words(self) -> None:
        """ updates the list of previous found words that is shown on board """
        text = "Already found: \n"
        for word in self.__previous_words:
            text += word
            text += "\n"
        self.__prev_words_str.set(text)

    def update_score(self, new_score: int) -> None:
        """ updates the current score to the new score so it will show
         on the GUI board"""
        self.__score = new_score
        score_str = "Your Current Score: " + str(self.__score)
        self.__score_title.set(score_str)

    def play(self) -> None:
        """ runs the main loop od the game """
        self.__root.mainloop()


if __name__ == "__main__":
    boggle = GUI()
    boggle.play()
