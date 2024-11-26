import os
import random
import File_functions

from board_methods import wincheck,get_turn,endcheck,format_read_options

class bcolours:
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    orange = '\033[38:5:208m'
    normal = '\033[0m'
    bold = '\033[1m'
    nobold = '\033[22m'
    underline = '\033[4m'
    grey = "[90m"
    dictionairy = {"purple" : '\033[95m'
        ,"blue" : '\033[94m'
        ,"cyan" : '\033[96m'
        ,"green" : '\033[92m'
        ,"yellow" : '\033[93m'
        ,"red" : '\033[91m'
        ,"orange" : '\033[38:5:208m'
        ,"normal" : '\033[0m'
        ,"bold" : '\033[1m'
        ,"nobold" : '\033[22m'
        ,"underline" : '\033[4m'
        ,"grey" : "[90m"}

def clearscreen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

#inclusive lower, exclusive higher
def validatenuminput(question,lowbound,highbound=1000,colour=bcolours.normal,error = "That choice doesn't make sense!"):
    while True:
        answer = input(colour + question)
        if answer.isdigit() == True:
            if int(answer) < highbound and int(answer) >= lowbound:
                return int(answer)
        print(bcolours.bold + bcolours.red + error + bcolours.normal) 

#checks the length of inputed string, can be changed from exact length, <= length, >= length
def validateinputlen(question,length,colour=bcolours.normal,exactlen=True,lowlen=True):
    while True:
        answer = input(colour + question).strip(" ")
        if exactlen:
            if len(answer) == length:
                return answer
        elif lowlen:
            if len(answer) <= length:
                return answer
        elif not lowlen:
            if len(answer) >= length:
                return answer
        print(bcolours.bold + bcolours.red + "That is not the right length!" + bcolours.normal) 

class Player:
    def __init__(self,symbol,ai,playernum):
        self.symbol = symbol#symbol that represents the player, such as 'X'
        self.score = 0
        self.ai = ai#is this player controlled by the computer
        self.playernum = playernum

    def Take_Turn(self,board,winreq,gravity):
        print("\nPlayer " + self.symbol + " it is your turn to play.\n")#player symbol (name)

        if not gravity:
            coords = input("Enter the co-ordinates of the cell 'x,y': ")
            while True:    
                coords = coords.strip(" ")
                coords = coords.split(",")#should split input into 2 numbers
                if len(coords) == 2:#are there two co-ords
                    if coords[0].isdigit() and coords[1].isdigit() and coords[0] != "" and coords[1] != "":#are they numbers
                        ux = int(coords[0])#user x value
                        uy = int(coords[1])#user y value
                        if ux > 0 and ux <= len(board[0]) and uy > 0 and uy <= len(board):#are they within the board
                            xcoord = ux - 1#adjust for indexing
                            ycoord = uy - 1
                            if board[ycoord][xcoord] == 0:#checks if the cell is empty
                                board[ycoord][xcoord] = self.playernum#sets the cell to player symbol
                                return board, wincheck(board,winreq,xcoord,ycoord)#returns the new board and a win check
                            else:
                                coords = input("That cell is full!")
                        else:
                            coords = input("Enter something in the grid!")
                    else:
                        coords = input("Enter something valid!")
                else:
                    coords = input("Enter something valid!")
        else:
            column = input("Enter the column you would like: ")
            while True:    
                column = column.strip(" ")
                if column.isdigit() and column != "":#are they numbers
                    column = int(column)
                    if column > 0 and column <= len(board[0]):#are they within the board
                        column -= 1#adjust for indexing
                        if board[-1][column] == 0:#is the row not full
                            for row in range(len(board)-1,-1,-1):
                                if board[row][column] != 0:#finds the lowest cell not full
                                    board[row+1][column] = self.playernum#sets the cell to player symbol
                                    return board, wincheck(board,winreq,column,row+1)#returns the new board and a win check
                        
                            board[0][column] = self.playernum#since the column is not full, if the program runs to this point, the column must be empty
                            return board, wincheck(board,winreq,column,0)#returns the new board and a win check

                        else:
                            column = input("That column is full!")
                    else:
                        column = input("Enter something in the grid!")
                else:
                    column = input("Enter something valid!")

    def play_ai_turn(self,boardstates,board,winreq):
        turns = get_turn(board)
        for b in boardstates[turns]:
            if str(board) == str(b[0]):
                if type(b[1]) == str:
                    options = format_read_options(b[1])
                else:
                    options = b[1]
                y,x = options[random.randint(0,len(options)-1)]
                board[y][x] = self.playernum
                return board, wincheck(board,winreq,x,y)


def printarray(array):
    for i in array:
        if type(i) == list:
            printarray(i)
        else:
            print(i,end="")
                
def askcontinue():
    choice = input("\nRematch?")
    while True:
        choice = choice.strip(" ").lower()
        if choice == "yes" or choice == "y":
            return True
        elif choice == "no":
            return False
        else:
            choice = input("Be Sensible!")

def settings():
    debug = input("Debug?")#returns set settings below to save time
    if debug:
        return 3,3,3,2,{0:"-",1:"x",2:"o"},{"-":bcolours.grey,"x":bcolours.red,"o":bcolours.yellow},False,[1]
    #clearscreen()
    w = validatenuminput("How many columns do you want your board to have?\n",1)
    clearscreen()
    h = validatenuminput("How many rows do you want your board to have?\n",1)
    clearscreen()
    win = validatenuminput("How long do you want the streak required to win to be?\n",1,highbound=max(w,h)+1,error="The streak cannot be larger than your board! Or you entered a negative number :(")
    clearscreen()
    p = validatenuminput("How many players do you want?\n",2)
    clearscreen()
    symbols = []
    symboldict = {0:"-"}
    colours = {"-":bcolours.grey}
    for i in range(p):
        valid = False
        while not valid:
            s = validateinputlen("What symbol would player " + str(i+1) + " like?\n",1)
            if s not in symbols and s != "-":
                symbols.append(str(s))
                symboldict[i+1] = s
                colours[s] = choosecolour("What colour do you want to be? ")
                valid = True
            else:
                print("That symbol is already in use!")
    clearscreen()
    grav = input("Do you want to enable gravity?")
    clearscreen()
    if grav.lower().strip(" ")[0] == "y":
        grav = True
    else:
        grav = False
    ai_input = input("What players (if any) do you want to be played by the computer? Enter as 1,3")
    ai_input = ai_input.strip(" ").split(",")
    ai = []
    for i in ai_input:
        if i.isdigit():
            ai.append(int(i))

    return w,h,win,p,symboldict,colours,grav,ai

def choosecolour(message):
    listofcolours = ["blue","cyan","green","yellow","red","orange"]
    colour = input(message).strip(" ").lower()
    while True:
        if colour in listofcolours:
            return bcolours.dictionairy[colour]
        else:
            print("Select a colour from: blue, cyan, green, yellow, red or orange")
            colour = input()

def displayboard(board,colours,symbols,winstreak=[],win=False):
    totaltext = [] #the overall board to be printed
    ylen = len(str(len(board)))#the length that the numbering off the rows need to be in order to preserve alignment
    for y in range(len(board)-1,-1,-1):#print rows in reverse order as it is more intuitive for users
        linetext = []
        for x in board[y]:
            t = symbols[x]
            #colour formatting
            linetext.append(colours[t] + t + " ")#adds a space for easy reading
        numbering = str(y+1)#the enumeration on the left of the row
        for i in range(ylen-len(numbering)):
            numbering = "0" + numbering
        linetext.insert(0,bcolours.grey + numbering + "|")
        linetext.append("\n")
        totaltext.append(linetext)#adds the whole line to the total text along with the numbering and a newline at the end
    linetext = " " + " "*ylen#start with 1 space to account for the |
    for n in range(len(board[0])):#adds the column numbering on the bottom
        linetext += str(n+1)[-1] + " "
    totaltext.append(bcolours.grey + linetext + bcolours.normal + "\n")

    if win:
        for y,x in winstreak:
            indexy = len(totaltext)-y-2#flips around the centre of the board as the text is printed in reverse index order and adjusts 2 for the colour codes in the text
            indexx = x+1
            totaltext[indexy][indexx] = bcolours.bold + str(totaltext[indexy][indexx]) + bcolours.normal

    printarray(totaltext)#prints the board

def winnerinfo(players,numplayers):
    scores = []
    for i in players:
        print("Player " + str(i.playernum) + " scored " + str(i.score))
        scores.append(i.score)
    high_score = max(scores)
    overall_winner = []
    for i in players:
        if i.score == high_score:
            overall_winner.append(i.playernum)
        
    if len(overall_winner) == 1:
        print("Overall winner is Player "+bcolours.green + str(overall_winner[0])+bcolours.normal + "!")
        if players[overall_winner[0]-1].ai:
            print(bcolours.red + "AI wins, THE WORLD IS ENDING")
    elif len(overall_winner) == numplayers:
        print("All Players tied!")
    else:
        text = ""
        for i in overall_winner:
            text += ", " + str(i)
        text = text[1:]
        print("Overall winners are Players" + text + "!")

def main_game():            
    bwidth,bheight,winreq,numplayers,symbols,colours,gravity,ai = settings()#initialise all settings

    if ai:#are there any computer controlled players
        boardstates = File_functions.find_learnt_game(bwidth,bheight,gravity,numplayers,winreq)

    players = []#list containing player objects
    for i in range(1,numplayers+1):
        if i in ai:
            players.append(Player(symbols[i],True,i))
        else:
            players.append(Player(symbols[i],False,i))

    play = True
    while play:
        clearscreen()
        board = []
        for h in range(bheight):
            board.append([])
            for w in range(bwidth):
                board[h].append(0)

        #game variables
        won = False
        turn = -1#accounts for the turn being incremented before the first turn is taken

        while not won:
            displayboard(board,colours,symbols)
            turn = (turn + 1)%numplayers#cycles through the turns
            if endcheck(board):#if there are no more spaces, end in a draw
                clearscreen()
                break
            if players[turn].ai:#is this player controlled by the ai 
                board,[won,winning_streak] = players[turn].play_ai_turn(boardstates,board,winreq)#take the ai turn
            else:
                board,[won,winning_streak] = players[turn].Take_Turn(board,winreq,gravity)#take the turn
            clearscreen()


        if won == True:#prints results
            displayboard(board,colours,symbols,winstreak = winning_streak,win=True)#shows final board
            print("Player " + str((turn+1))+ " won!")
            players[turn].score += 1
        else:
            displayboard(board,colours,symbols)#shows final board
            print("It's a draw!")
        
        play = askcontinue()#checks if the player wants to continue playing


    winnerinfo(players,numplayers)
