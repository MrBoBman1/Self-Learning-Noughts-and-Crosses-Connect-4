"""
Program over-view

This program allows the user to play either Noughts and Crosses or Connect-4 while changing most variables that define the game such as:

1. The dimensions of the board
2. The length of the required streak to win
3. The number of players
4. The symbols of the players

It also allows you to train the computer on your rules so that it will play perfectly, it will also determine whether your game is
a forced win or draw.

The program is able to save the strategy for any game and then read in the file if it exists in order to play the given game.

WARNING: The AI learning algorithm is currently INCREDIBLY slow for boards larger than around 4*4, it may take several hours to learn
larger games and it scales incredibly fast. The resulting file  may also be incredibly large. BE WARNED

"""
import Textgame_methods
import GUI_game_methods

def main():
    Textbased = False#change to change the game
    if Textbased:
        Textgame_methods.main_game()
    else:
        GUI_game_methods.main_game()

            
main()
"""
Documented issues post version 1: fixed and unfixed
©lucafrey

        Issue:
            On board sizes with dimensions larger than 9, the printing becomes misaligned due to column and/or row numbering being 
            greater than 1 digit
        Fix:
            For the row numbering, add as many zeros to the front of all numbers as needed to match lengths,
            For column, either do the same as rows, but this will cause the board to be much wider as each column takes uo more room,
            another solution is to only use the unit digit and use a colour code for readability
        Status:
            Fixed

        Issue:
            It does not mention whos turn it is
        Fix:
            Simple print statement at the start of the turn function
        Status: 
            Fixed

        Issue:
            If the same symbol is entered, the game recognises this and prevents it, but does not ask for another input
        Fix:
            Add a validation loop that only breaks if the new symbol is not in the set of symbols
        Status: 
            Fixed

        Issue:
            New board printing does not function at all
        Fix:
            Issue where the linetext would be a nonetype so nothing would print, I simply rewrote the lines and now it functions
        Status:
            Fixed

        Issue:
            When the bottom right corner cell is filled, the column numbering becomes coloured
        Fix:
            Add a colour print to the column numbering themselves, instead on relying that the most recent colour would be grey
        Status:
            Fixed

        Issue:
            When a draw occurs, the board is printed twice
        Fix:
            Add a clearscreen function in the when the end check is true as it would otherwise skip the clearscreen at the end of the loop
        Status:
            Fixed

        Issue:
            With more than 2 players, the 3rd player starts instead of the first        
        Fix: 
            Initialise turn as -1 not 1 as I had assumed that it would reset to 0, but this is only true for two players.
        Status:
            Fixed

        Issue:
            When the winning board is printed, there is a string item assignment error
        Fix:
            This was due to the x,y coords being offset by 1 due to the extra row and column at in the boardcopy which led to the wrong cell being assigned
        Status:
            Fixed

        Issue:
            When reading in stored games, it is unable to recognise the board in the file
        Fix:
            This was due to the board being a list and the file being a string so it compared wrong
        Status:
            Fixed
        
        Issue:
            When playing against the ai, since the ai's turn completes almost instantaneously, the clearscreen command does not have time 
            to executre fully, so some of the board is not deleted until the new board is printed, so it never fully clears the screen

        Issue:
            If the number of wins per player are tied, or all games a draws, the overall winner does not function as intended
        
        Issue:
            self learning connect 4 fails due to extra options being present due to the loop not exiting when it has found the lowest option leads it to replacing cells
                        
        Issue:
            winstreak of length 1 doesnt work

        Issue:
            in the GUI, gravity can be deselected and no error is flagged
Ideas:

    Major:

    Add gravity so 4-in-a-row can be played - implemented
    Self learning algorithm to learn optimal strategy for each game - implemented

    Minor:

    the winning streak becomes coloured - implemented (it becomes bold)
    different players are coloured differently on the board, could be chosen by players - implemented
    calculate and display the overall winner at the end - implemented
    """