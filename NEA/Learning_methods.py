import copy
import time
from board_methods import wincheck,endcheck,get_turn

def flip_board(direction,board,options):
    length = len(board[0]) -1
    height = len(board)-1
    if direction == "horizontally":
        for i in range(len(board)):
            board[i].reverse()#in this case reverse can be used
        for i in range(len(options)):
            options[i][1] = length - options[i][1]
        return board,options
    elif direction == "vertically":
        board.reverse()#just reverse all the rows
        for i in range(len(options)):
            options[i][0] = height - options[i][0]
        return board,options
    #length and height can be used interchangeably now as if the board is being flipped diagonally, it must have equal length and height
    elif direction == "diagonallydown":#from 0,0 to x,x
        for y in range(height):
            for x in range(length,y,-1):#only iterates through half the cells, as otherwise they would be swapped twice
                board[y][x],board[x][y] = board[x][y],board[y][x]
        for i in range(len(options)):
            options[i][0],options[i][1] = options[i][1],options[i][0]
        return board,options
    elif direction == "diagonallyup":#from 0,x to x,0
        for y in range(1,height+1):
            for x in range(length-y+1,length+1):
                board[y][x],board[length-x][length-y] = board[length-x][length-y],board[y][x]
        for i in range(len(options)):
            options[i][0],options[i][1] = length-options[i][1],length-options[i][0]
        return board,options

def rotate_board(degree,board,options):
    centre_x = int((len(board[0])-1)/2)
    centre_y = int((len(board)-1)/2) 

    if degree == 180:
        b,o = flip_board("horizontally",board,options)
        return flip_board("vertically",b,o)
    else:
        if degree == 90:
            m = 1#multiplier, written short for readability
        elif degree == 270:
            m = -1

        for y in range(round(len(board)/2)):
            for x in range(len(board)//2):
                x_dist = centre_x - x
                y_dist = centre_y - y
                temp  = board[y][x]
                board[y][x] = board[int(centre_y+m*x_dist)][int(centre_x-m*y_dist)]
                board[int(centre_y+m*x_dist)][int(centre_x-m*y_dist)] = board[int(centre_y+y_dist)][int(centre_x+x_dist)]
                board[int(centre_y+y_dist)][int(centre_x+x_dist)] = board[int(centre_y-m*x_dist)][int(centre_x+m*y_dist)]
                board[int(centre_y-m*x_dist)][int(centre_x+m*y_dist)] = temp
        for i in range(len(options)):#rotates each option
            temp = options[i][0]
            options[i][0] = centre_y - m*(centre_x - options[i][1])
            options[i][1] = centre_x + m*(centre_y - temp)
        return board,options

def add_boardstate(boardstates,board,options,result,turn,gravity):

    #when any boardstate it added, I am able to flip it and rotate it accordingly as the outcome of a mirrored board is identical
    #this way, not nearly as many boards need to be played to find train the AI

    numturns = get_turn(board)
    newboards = []#some of the flipped boards may be the same, in that case they should not be added
    newboards.append(board)
    boardstates[numturns].append([board,options,result,turn])
    #no matter the game, the board can always be flipped horizontally
    b,o = flip_board("horizontally",copy.deepcopy(board),copy.deepcopy(options))#copy them to be safe
    if b not in newboards:
        newboards.append(copy.copy(b))
        boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])

    if not gravity:#if noughts and crosses
        b,o = flip_board("vertically",copy.deepcopy(board),copy.deepcopy(options))
        if b not in newboards:
            newboards.append(copy.copy(b))
            boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])

        b,o = rotate_board(180,copy.deepcopy(board),copy.deepcopy(options))
        if b not in newboards:
            newboards.append(copy.copy(b))
            boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])
        
        if len(board[0]) == len(board):#is it a sqaure:
            b,o = flip_board("diagonallyup",copy.deepcopy(board),copy.deepcopy(options))
            if b not in newboards:
                newboards.append(copy.copy(b))
                boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])

            b,o = flip_board("diagonallydown",copy.deepcopy(board),copy.deepcopy(options))
            if b not in newboards:
                newboards.append(copy.copy(b))
                boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])

            b,o = rotate_board(90,copy.deepcopy(board),copy.deepcopy(options))
            if b not in newboards:
                newboards.append(copy.copy(b))
                boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])

            b,o = rotate_board(270,copy.deepcopy(board),copy.deepcopy(options))
            if b not in newboards:
                newboards.append(copy.copy(b))
                boardstates[numturns].append([copy.copy(b),copy.copy(o),result,turn])
                    
    return boardstates

def learn_game(width,height,winreq,numplayers,gravity): #learns the optimal strategy to the current game for each player
    starttime = time.perf_counter()
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

    options = find_options(board,gravity)#find the available options
    for choice in options:#loops through each option
        winner,boardstates = play_turn(copy.deepcopy(board),choice,gravity,playerturn,numplayers,winreq,boardstates)
        
        if playerturn in winner:#if the current player can guarantee a win with one of the options, then that choice should always be taken, and there is no need to look at other options
            win_options.append(choice)
        elif 0 in winner:#if there is a draw option
            draw_options.append(choice)
        else:
            #the remaining options must result in an opponent winning
            loss_options[0].append(winner)
            loss_options[1].append(choice)
            
    if win_options:#if there are win options
        boardstates = add_boardstate(boardstates,board,win_options,{playerturn},playerturn,gravity)#the only choice worth recording is the winning choice
        winners = {playerturn}
    elif draw_options:#if there are draw options after the win option, then take them
        boardstates = add_boardstate(boardstates,board,draw_options,{0},playerturn,gravity)
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
        boardstates = add_boardstate(boardstates,board,loss_options[1],winners,playerturn,gravity)#the player can no longer win, nor force a draw, so it does not matter which opponent they choose to allow to win
    if winners == {0}:
        text = "Solved game, forced draw is possible"
    elif len(winners) == 1:
        text = "Solved game, Player " + str(winners) + " can force a win."
    else:
        text = "Not a solved game, Players " + str(winners) + " can all win with perfect play."

    endtime = time.perf_counter()
    timetaken = endtime-starttime
    print(timetaken)
    input()
    return boardstates,text

def play_turn(board,choice,gravity,playerturn,numplayers,winreq,boardstates):
    print(board)

    board[choice[0]][choice[1]] = playerturn#enacts the choice

    if wincheck(board,winreq,choice[1],choice[0])[0]:#if the game has been won
        return {playerturn},boardstates#winner
    elif endcheck(board):
        return {0},boardstates#draw

    #if the current board has already beeen played from, dont continue
    turn = get_turn(board)
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
        winner,boardstates = play_turn(copy.deepcopy(board),choice,gravity,copy.deepcopy(playerturn),numplayers,winreq,boardstates)#plays the game onwards from each choice recursively
        if playerturn in winner:#if the current player can guarantee a win with one of the options, then that choice should always be taken, and there is no need to look at other options
            win_options.append(choice)
        elif 0 in winner:#if there is a draw option
            draw_options.append(choice)
        else:
            #the remaining options must result in an opponent winning
            loss_options[0].append(winner)
            loss_options[1].append(choice)

    if win_options:#if there are win options
        boardstates = add_boardstate(boardstates,board,win_options,{playerturn},playerturn,gravity)#the only choice worth recording is the winning choice
        return {playerturn},boardstates
    if draw_options:#if there are draw options after the win option, then take them
        boardstates = add_boardstate(boardstates,board,draw_options,{0},playerturn,gravity)
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
        boardstates = add_boardstate(boardstates,board,loss_options[1],winners,playerturn,gravity)#the player can no longer win, nor force a draw, so it does not matter which opponent they choose to allow to win
        return winners,boardstates

def find_options(board,gravity):
    options = []
    if not gravity:#noughts and crosses
        for row in range(len(board)):
            for column in range(len(board[0])):
                if board[row][column] == 0:#finds all empty cells
                    options.append([row,column])#appends the coordinate of the option
    else:#connect-4
        for column in range(len(board[0])):
            if board[-1][column] == 0:#is the row not full
                found = False
                for row in range(len(board)-1,-1,-1):
                    if board[row][column] != 0:#finds the lowest cell not full
                        options.append([row+1,column])#appends the coordinate of the available cell
                        found = True
                        break
                if not found:
                    options.append([0,column])
    return options#returns a list of available coordinates
