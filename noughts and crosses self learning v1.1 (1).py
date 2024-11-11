import copy
import os
import random

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
                    if coords[0].isdigit and coords[1].isdigit and coords[0] != "" and coords[1] != "":#are they numbers
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
                if column.isdigit and column != "":#are they numbers
                    column = int(column)
                    if column > 0 and column <= len(board):#are they within the board
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
		    options = b[1]#new stuff
		y,x = options[random.randint(0,len(options)-1)]
                board[y][x] = self.playernum
                return board, wincheck(board,winreq,x,y)

def wincheck(board,winreq,x,y):
    boardcopy = copy.deepcopy(board)#makes a copy so not to disrupt original
    for i in range(len(boardcopy)):#adds an extra "" to each column and row in order to prevent out of range list indexing in the wincheck
        boardcopy[i].insert(0,"")
        boardcopy[i].append("")
    boardcopy.insert(0,[""]*len(boardcopy[0]))
    boardcopy.append([""]*len(boardcopy[0]))

    x += 1#adjust for initial added row and column
    y += 1

    winstreak = [[int(y),int(x)]]#the winning streak if it exists, x and y coords are offset by 1

    #only the newly changed cell can cause a win, so only check the surroundings of the new cell
    for yoffset,xoffset in [[1,1],[0,1],[-1,1],[-1,0]]:#four axis that need checking
        pos = True#the positive direction can still be continued
        neg = True#same for negative
        total = 1#number of symbols in a row
        symbol = boardcopy[y][x]
        for streak in range(1,winreq):#if the newly added cell is the start pf the winning chain, it lasts a maximum of the winn req
            if pos == True:
                if boardcopy[y+yoffset*streak][x+xoffset*streak] == symbol:#if the nearby cell is the same symbol add one to the total
                    total += 1
                    winstreak.append([int(y+yoffset*streak),int(x+xoffset*streak)])
                else:
                    pos = False
            if neg == True:
                if boardcopy[y-yoffset*streak][x-xoffset*streak] == symbol:#if the nearby cell is the same symbol add one to the total
                    total += 1
                    winstreak.append([int(y-yoffset*streak),int(x-xoffset*streak)])
                else:
                    neg = False
            if total >= winreq:
                return True, winstreak
            if neg == False and pos == False:
                break
    return False, winstreak

def endcheck(board):#checks if there are any available moves
    for y in board:
        for x in y:
            if x == 0:
                return False
    return True

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
    totaltext.append(bcolours.grey + linetext + bcolours.normal)

    if win:
        for y,x in winstreak:
            indexy = len(totaltext[0])-y-2#flips around the centre of the board as the text is printed in reverse index order and adjusts 2 for the colour codes in the text
            indexx = x#adjusts 1
            totaltext[indexy][indexx] = bcolours.bold + str(totaltext[indexy][indexx]) + bcolours.normal

    printarray(totaltext)#prints the board


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
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            choice = input("Be Sensible!")

def settings():
    debug = input()
    if debug:
        return 3,3,3,2,{0:"-",1:"x",2:"o"},{"-":bcolours.grey,"x":bcolours.red,"o":bcolours.yellow},False,[2]

    w = validatenuminput("How many columns do you want your board to have?\n",1)
    h = validatenuminput("\nHow many rows do you want your board to have?\n",1)
    win = validatenuminput("\nHow long do you want the streak required to win to be?\n",2,highbound=max(w,h)+1,error="The streak cannot be larger than your board! Or you entered a negative number :(")
    p = validatenuminput("\nHow many players do you want?\n",2)
    symbols = []
    symboldict = {0:"-"}
    colours = {"-":bcolours.grey}
    for i in range(p):
        valid = False
        while not valid:
            s = validateinputlen("\nWhat symbol would player " + str(i+1) + " like?\n",1)
            if s not in symbols and s != "-":
                symbols.append(str(s))
                symboldict[i+1] = s
                colours[s] = choosecolour("What colour do you want to be? ")
                valid = True
            else:
                print("That symbol is already in use!")
    grav = input("Do you want to enable gravity?")
    if grav.lower().strip(" ")[0] == "y":
        grav = True
    else:
        grav = False
    ai_input = input("What players (if any) do you want to be played by the computer? Enter as 1,3")
    ai_input = ai_input.strip(" ").split(",")
    ai = []
    for i in ai_input:
        if i.isdigit():
            ai.append(i)

    return w,h,win,p,symboldict,colours,grav,ai

def choosecolour(message):
    listofcolours = ["blue","cyan","green","yellow","red","orange"]
    colour = input(message).strip(" ").lower()
    while True:
        if colour in listofcolours:
            return bcolours.dictionairy[colour]
        else:
            print("Select a colour from: blue, cyan, green, yellow, red or orange")

def get_turn(board):
    turns = 0#number of turns taken
    for y in board:
        for x in y:
            if x != 0:
                turns += 1
    return turns

def add_boardstate(boardstates,board,options,result,turn):
    numturns = get_turn(board)
    boardstates[numturns].append([board,options,result,turn])
    return boardstates

def learn_game(width,height,winreq,numplayers,gravity): #learns the optimal strategy to the current game for each player
    depth = 0
    playerturn = 1
    board = []
    boardstates = []
    for _ in range(width*height):#the maximum number of turns that can be taken before a draw or a win
        boardstates.append([])

    for h in range(height):
        board.append([])
        for w in range(width):
            board[h].append(0)

    #kickstart game
    loss_options = [[],[]]#2D array, each option corresponds to a opponent winner 
    draw_options = []#list of draw options
    win_options = []#list of winning options
    turns = get_turn(board)

    options = find_options(board,gravity)#find the available options
    for choice in options:#loops through each option
        winner,boardstates = play_turn(copy.deepcopy(board),choice,gravity,playerturn,numplayers,winreq,boardstates,depth)
        
        if playerturn in winner:#if the current player can guarantee a win with one of the options, then that choice should always be taken, and there is no need to look at other options
            win_options.append(choice)
        elif 0 in winner:#if there is a draw option
            draw_options.append(choice)
        else:
            #the remaining options must result in an opponent winning
            loss_options[0].append(winner)
            loss_options[1].append(choice)
            
    if win_options:#if there are win options
        boardstates = add_boardstate(boardstates,board,win_options,{playerturn},playerturn)#the only choice worth recording is the winning choice
        winners = {playerturn}
    if draw_options:#if there are draw options after the win option, then take them
        boardstates = add_boardstate(boardstates,board,draw_options,{0},playerturn)
        winners = {0}
    else:
        #this is required to deal with the possibility that there could be multiple other winners (player 2 and player 3)
        winners = set()
        for i in loss_options[0]:
            if type(i) == set:
                for j in i:
                    winners.add(j)
            else:
                winners.add(i)
        boardstates = add_boardstate(boardstates,board,loss_options[1],winners,playerturn)#the player can no longer win, nor force a draw, so it does not matter which opponent they choose to allow to win
  
    if winners == {0}:
	text = "Solved game, forced draw is possible")
    elif len(winners) == 1:
	text = "Solved game, Player " + str(winners) " can force a win.")
    else:
	text = "Not a solved game, Players " + str(winners) + " can all win with perfect play.")
   #new stuff
        
    save_learnt(boardstates,numplayers,width,height,gravity,winreq,text)
    
    return boardstates

def play_turn(board,choice,gravity,playerturn,numplayers,winreq,boardstates,depth):
    #print(boardstates)

    board[choice[0]][choice[1]] = playerturn#enacts the choice
        #win,_ = wincheck(board,winreq,choice)#underscore used as the winstreak returned by the wincheck is useless, I only need to know if the game is over

    if wincheck(board,winreq,choice[1],choice[0])[0]:#if the game has been won
        return {playerturn},boardstates#winner
    elif endcheck(board):
        return {0},boardstates#draw

    #if the current board has already beeen played from, dont continue
    turn = get_turn(board)
    print(turn)
    for i in range(len(boardstates[turn])):
        if boardstates[turn][i][0] == board:
            return boardstates[turn][i][2],boardstates
        

    playerturn = (playerturn%numplayers) + 1

    #if the game has not ended and is a new situation, continue playing
    options = find_options(board,gravity)#find the available options
    loss_options = [[],[]]#2D array, each option corresponds to a opponent winner 
    draw_options = []#list of draw options
    win_options = []#list of winning options
    for choice in options:#loops through each option
        winner,boardstates = play_turn(copy.deepcopy(board),choice,gravity,copy.deepcopy(playerturn),numplayers,winreq,boardstates,depth+1)#plays the game onwards from each choice recursively
        if playerturn in winner:#if the current player can guarantee a win with one of the options, then that choice should always be taken, and there is no need to look at other options
            win_options.append(choice)
        elif 0 in winner:#if there is a draw option
            draw_options.append(choice)
        else:
            #the remaining options must result in an opponent winning
            loss_options[0].append(winner)
            loss_options[1].append(choice)

    if win_options:#if there are win options
        boardstates = add_boardstate(boardstates,board,win_options,{playerturn},playerturn)#the only choice worth recording is the winning choice
        return {playerturn},boardstates
    if draw_options:#if there are draw options after the win option, then take them
        boardstates = add_boardstate(boardstates,board,draw_options,{0},playerturn)
        return {0},boardstates
    else:
        #this is required to deal with the possibility that there could be multiple other winners (player 2 and player 3)
        winners = set()
        for i in loss_options[0]:
            if type(i) == set:
                for j in i:
                    winners.add(j)
            else:
                winners.add(i)
        boardstates = add_boardstate(boardstates,board,loss_options[1],winners,playerturn)#the player can no longer win, nor force a draw, so it does not matter which opponent they choose to allow to win
        return winners,boardstates

def find_options(board,gravity):
    options = []
    if not gravity:#noughts and crosses
        for row in range(len(board)):
            for column in range(len(board[0])):
                if board[row][column] == 0:#finds all empty cells
                    options.append([row,column])#appends the coordinate of the option
    else:#connect-4
        for column in range(len(board)):
            if board[-1][column] == 0:#is the row not full
                for row in range(len(board[0])-1,-1,-1):
                    if board[row][column] != 0:#finds the lowest cell not full
                        options.append([row+1,column])#appends the coordinate of the available cell
                options.append([0,column])
    return options#returns a list of available coordinates

def save_learnt(boardstates,numplayers,width,height,gravity,winreq,solved):
    directory = "Noughts & Crosses|Connect-4: Trained games/"
    if gravity:
        directory += "Connect-4/"
    else:
        directory += "Noughts and Crosses/"
    directory += str(numplayers) + " Players/Streak " + str(winreq)
    filename = directory + "/" + str(width) + "*" + str(height) + ".txt"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file = open(filename,"w")
    for t in boardstates:
        file.write("newturn")#allows for easy reading
        for b in t:
            for i in b:
                file.write(str(i))
                file.write("\n")
            file.write("\n")
    file.close()
    file2 = open("Game Result","w")#new stuff
    file2.write(solved)
    file2.close()

def find_learnt_game(w,h,grav,pnum,winreq):#finds if the current game has already been learnt
        filename = "Noughts & Crosses|Connect-4: Trained games/"
        if grav:
            filename += "Connect-4/"
        else:
            filename += "Noughts and Crosses/"
        filename += str(pnum) + " Players/Streak " + str(winreq) + "/" + str(w) + "*" + str(h) + ".txt"
        if os.path.isfile(filename):
            file = open(filename,'r')
            file_boardstates = file.readlines()
            file.close()
            return interpret_file(file_boardstates)
        else:
            choice = input("These settings have not been learnt yet, do you want to train this game?")
            if choice.lower().strip(" ")[0] == "y":
                boardstates = learn_game(w,h,winreq,pnum,grav)
                return boardstates
            else:
                return False

def interpret_file(file_boardstates):
    boardstates = []
    for line in file_boardstates:
        line = line.strip("\n")
        if line == "newturn":
            boardstates.append([[]])
        elif line == "":
            boardstates[-1].append([])
        else:
            boardstates[-1][-1].append(line)
    return boardstates
            
        
            
            
        

def main():            
    bwidth,bheight,winreq,numplayers,symbols,colours,gravity,ai = settings()#initialise all settings

    if ai:#are there any computer controlled players
        boardstates = find_learnt_game(bwidth,bheight,gravity,numplayers,winreq)

    players = []#list containing player objects
    for i in range(numplayers):
        if i+1 in ai:
            players.append(Player(symbols[i],True,i+1))
        else:
            players.append(Player(symbols[i],False,i+1))

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
            print(players[turn].ai)
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

    high_score = 0#new stuff
    overall_winner = 0
    for i in players:
        if i.score > high_score:
            high_score = i.score
            overall_winner = i.playernum
        print("Player " + i.playenum + " scored " + str(i.score))
    print("Overall winner is Player: " + overall_winner + "!")
    if players[overallwinner-1].ai:
	print("AI wins, THE WORLD IS ENDING")

clearscreen()#removes file text
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

            
Ideas:

    Major:

    Add gravity so 4-in-a-row can be played - implemented
    Self learning algorithm to learn optimal strategy for each game - implemented

    Minor:

    the winning streak becomes coloured - implemented (it becomes bold)
    different players are coloured differently on the board, could be chosen by players - implemented
    calculate and display the overall winner at the end - implemented
    """