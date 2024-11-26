import copy

def wincheck(board,winreq,x,y):

    if winreq == 1:
        return True,[[y,x]]

    boardcopy = copy.deepcopy(board)#makes a copy so not to disrupt original
    for i in range(len(boardcopy)):#adds an extra "" to each column and row in order to prevent out of range list indexing in the wincheck
        boardcopy[i].insert(0,"")
        boardcopy[i].append("")
    boardcopy.insert(0,[""]*len(boardcopy[0]))
    boardcopy.append([""]*len(boardcopy[0]))

    x += 1#adjust for initial added row and column
    y += 1
    
    #only the newly changed cell can cause a win, so only check the surroundings of the new cell
    for yoffset,xoffset in [[1,1],[0,1],[-1,1],[-1,0]]:#four axis that need checking
        winstreak = [[int(y)-1,int(x)-1]]#the winning streak if it exists, x and y coords are offset by 1
        pos = True#the positive direction can still be continued
        neg = True#same for negative
        total = 1#number of symbols in a row
        symbol = boardcopy[y][x]
        for streak in range(1,winreq):#if the newly added cell is the start of the winning chain, it lasts a maximum of the winn req
            if pos == True:
                if boardcopy[y+yoffset*streak][x+xoffset*streak] == symbol:#if the nearby cell is the same symbol add one to the total
                    total += 1
                    winstreak.append([int(y+yoffset*streak)-1,int(x+xoffset*streak)-1])
                else:
                    pos = False
            if neg == True:
                if boardcopy[y-yoffset*streak][x-xoffset*streak] == symbol:#if the nearby cell is the same symbol add one to the total
                    total += 1
                    winstreak.append([int(y-yoffset*streak)-1,int(x-xoffset*streak)-1])
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

def get_turn(board):
    turns = 0#number of turns taken
    for y in board:
        for x in y:
            if x != 0:
                turns += 1
    return turns

def format_read_options(read_options):
    options = []
    ordinates = []
    for char in read_options:
        if char.isdigit() or char == "0":
            ordinates.append(int(char))
    for pair in range(0,int(len(ordinates)),2):
        options.append([ordinates[pair],ordinates[pair+1]])
    return options