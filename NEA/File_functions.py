import os
from Learning_methods import learn_game

def get_directory(w,h,grav,pnum,winreq):#returns the directory that the game should be saved in/found in
    directory = "NEA/Noughts & Crosses|Connect-4: Trained games"
    if grav:
        directory = os.path.join(directory,"Connect-4")
    else:
        directory = os.path.join(directory,"Noughts and Crosses")
    directory = os.path.join(directory,str(pnum) + " Players","Streak " + str(winreq),str(w) + "*" + str(h))
    return directory

def save_learnt(boardstates,numplayers,width,height,gravity,winreq,solved):
    directory = get_directory(width,height,gravity,numplayers,winreq)
    filename = os.path.join(directory,"Boardstates.txt")

    if not os.path.exists(directory):#checks if the directory exists
        os.makedirs(directory)#if not make it
    file = open(filename,"w")#makes the file
    for t in boardstates:
        file.write("newturn")#allows for easy reading
        for b in t:
            file.write("\n")
            for i in b:
                file.write(str(i))
                file.write("\n")
    file.close()
    file.close()
    file2 = open(os.path.join(directory,"Game Result.txt"),"w")#creates the file that stores the games result
    file2.write(solved)
    file2.close()

def find_learnt_game(w,h,grav,pnum,winreq):#finds if the current game has already been learnt
    filename = os.path.join(get_directory(w,h,grav,pnum,winreq),"Boardstates.txt")
    if os.path.isfile(filename):
        file = open(filename,'r')
        file_boardstates = file.readlines()
        file.close()
        return interpret_file(file_boardstates)
    else:
        choice = input("These settings have not been learnt yet, do you want to train this game?")
        if choice.lower().strip(" ")[0] == "y":
            boardstates,text = learn_game(w,h,winreq,pnum,grav)
            save_learnt(boardstates,pnum,w,h,grav,winreq,text)
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