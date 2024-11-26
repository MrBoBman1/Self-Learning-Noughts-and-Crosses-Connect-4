import pygame_gui.elements.ui_text_box
import Create_game_GUI
import os
import File_functions
import pygame,pygame_gui
import board_methods
import copy

class Player:
    def __init__(self,symbol,ai,playernum,colour):
        self.formatsymbol = "</font><font color='"+str(colour)+"' size=7>"+symbol+"</font>"#symbol that represents the player, such as 'X'
        self.symbol = symbol
        self.score = 0
        self.ai = ai#is this player controlled by the computer
        self.playernum = playernum

class Cell(pygame_gui.elements.UIButton):
    def __init__(self,x,y,xpos,ypos,side_len,manager):
        super().__init__(relative_rect=pygame.Rect((xpos,ypos),(side_len,side_len)),manager=manager,text="")
        self.x = x
        self.y = y
        self.rectangle = pygame.Rect((xpos,ypos),(side_len,side_len))#makes it easy to make a text box to replace the cells position

def validate_cell(y,x,board):#finds the lowest cell in the column for connect-4
    while True:
        if y == len(board)-1:#if the cell is at the bottom
            return y,x
        elif board[y+1][x] != 0:#if the lower cell is full
            return y,x
        y += 1

def make_game_window():
    pygame.init()
    pygame.display.set_caption('Game Window')

    info = pygame.display.Info()#get info about size of the screen
    window_surface = pygame.display.set_mode((info.current_w,info.current_h))
    background = pygame.Surface((info.current_w,info.current_h))
    background.fill(pygame.Color('#000000'))
    manager = pygame_gui.UIManager((info.current_w,info.current_h),'NEA/base_theme.json')
    return manager,window_surface,background

def make_board(w,h,manager):
    info = pygame.display.Info()#get info about size of the screen
    wmax = info.current_w - 100#leaves available space around the edges
    hmax = info.current_h - 200 
    side_len = min(wmax/w,hmax/h)#the largest side length to make all the cells be squares and fit
    xoffset = (wmax-side_len*w)/2 + 50
    yoffset = (hmax-side_len*h)/2
    cells = []
    for y in range(h):
        cells.append([])
        for x in range(w):
            cells[y].append(Cell(x,y,xoffset+side_len*x,yoffset+side_len*y,side_len,manager))
    commbox = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(xoffset,hmax+20,side_len*w,80),manager=manager,visible=0,text="")
    return cells,commbox

def convert_colours(colours):
    new_colours = {}
    for key in colours:
        hex_col = '#{:02x}{:02x}{:02x}'.format(colours[key][0], colours[key][1], colours[key][2])
        new_colours[key] = hex_col
    return new_colours

def stored_board(bwidth,bheight):
    board = []
    for h in range(bheight):
        board.append([])
        for w in range(bwidth):
            board[h].append(0)
    return board

def main_game():
    game_settings = Create_game_GUI.makewindow()#ask for settings
    board_settings = game_settings["board_settings"]
    colours = convert_colours(game_settings["colours"])
    #transfer the dictionairy into individual variables
    pygame.event.Event
    bwidth,bheight,gravity,numplayers,winreq = board_settings["width"],board_settings["height"],board_settings["gravity"],board_settings["players"],board_settings["winstreak"],
    if game_settings["ai"]:#are there any computer controlled players
        boardstates = File_functions.find_learnt_game(bwidth,bheight,gravity,numplayers,winreq)
    print(gravity)
    players = []#list containing player objects
    for i in range(1,numplayers+1):
        if i in game_settings["ai"]:
            players.append(Player(game_settings["player_symbols"][i],True,i,colours[i]))
        else:
            players.append(Player(game_settings["player_symbols"][i],False,i,colours[i]))


    board = stored_board(bwidth,bheight)

    pygame.init()
    pygame.display.set_caption('Game Window')

    manager,window_surface,background = make_game_window()
    cells,commbox= make_board(bwidth,bheight,manager)
    clock = pygame.time.Clock()
    cell_text = []
    is_running = True
    player = 0
    game_running = True
    while is_running:
        time_delta = clock.tick(60)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:#has a button been pressed
                for i in cells:
                    if event.ui_element in i:#is it a 'cell' button
                        
                        if gravity: 
                            y,x = validate_cell(event.ui_element.y,event.ui_element.x,board)
                        else:
                            y,x = event.ui_element.y,event.ui_element.x
                        board[y][x] = players[player].playernum
                        changedcell = cells[y][x]
                        changedcell.hide()
                        cell_text.append(pygame_gui.elements.UITextBox(relative_rect=changedcell.rectangle,html_text=players[player].formatsymbol,manager=manager))

                        won,winstreak = board_methods.wincheck(board,winreq,x,y)
                        if won:#has the player won
                            commbox.visible = 1
                            commbox.set_text("Player " + players[player].symbol + " won! Click to restart.")
                        elif board_methods.endcheck(board):
                            commbox.visible = 1
                            commbox.set_text("It's a draw! Click to restart.")

                        player = (player + 1)%numplayers
                if event.ui_element == commbox:
                    board = stored_board(bwidth,bheight)
                    for i in cell_text:
                        i.kill()
                    for a in cells:
                        for i in a:
                            i.set_text("")
                            i.show()
                    player = 0
                    commbox.set_text("")
                    commbox.visible = 0 

            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()

main_game()

