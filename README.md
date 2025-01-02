# Offline boggle game with gui

The aim of this project is to create a fun GUI for playing the [Boggle](https://en.wikipedia.org/wiki/Boggle) game offline.
Online games often include commercials as part of the interface, so a user-frienly offline game would be an improvement to the user experience while playing the game. 

## The rules of the game
The board of the game is a 4x4 board with letters. For each round of the game, a timer of 3 minutes will start. Within the 3 minute timeframe, the player must identify as many words as possible that can be made out of a line connecting the letters. 
The final rank of the game is based on the numer of words found and the length of each of the words. 

## installation
Installation requires downloading the files on this directory. A valid dictionary is provided along with all required code files. 
As this is a proposal for the project, the dependencies of this project will we updated later. 

## running the game
The game will be available as a command line application: 'python Boggle.py' or via a desktop icon. 

### Note:
This project was created as part of the Python course at WIS, 2024. 

<Describe your project's features here>

We have added some features to stress the user as his time is running out:
    1. The timer digits turn red when there are only 40 seconds left
    2. When there are less than 10 seconds left,
       there is a "beep" sound with every second passing.

In addition, we have created a quit button that when pressed,
pops a message box asking whether the user is sure about leaving the game.

moreover, we added a sounds for all success or failure of choosing a word from the board.
