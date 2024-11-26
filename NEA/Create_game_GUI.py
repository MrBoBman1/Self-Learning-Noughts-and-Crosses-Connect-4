import pygame
import pygame_gui
import copy

def validateresponse1(response,errorbar):
    response = response["Enter the settings for your game:"]
    columns = response["How many columns do you want?"]
    rows = response["How many rows do you want?"]
    streak = response["How long do you want the win streak to be?"]
    players = response["How many players do you want?"]
    gravity = response["Do you want to enable gravity?"]
    if columns > 0 and rows > 0:
        if streak > 0:
            if streak <= columns or streak <= rows:
                if players > 1:
                    if gravity != None:

                        if gravity == "Gravity Off":
                            gravity = False
                        else:
                            gravity = True

                        return {"width":columns,"height":rows,"winstreak":streak,"players":players,"gravity":gravity}
                    else:
                        errorbar.set_text("You must select a gravity option")
                else:
                    errorbar.set_text("You must have at least 2 players!")
            else:
                errorbar.set_text("The win streak cannot be longer than the board!")
        else:
            errorbar.set_text("Input a win streak!")
    else:
        errorbar.set_text("You must have at least one row and column!")
    return False

def validateresponse2(response,errorbar):
    response = response["Enter your player settings:"]
    symbols = []
    symboldict = {}
    for i in response:
        if response[i] == "" or response[i] == " ":
            errorbar.set_text("You must provide a character for all players!")
            return False
        elif response[i] in symbols:
            
            errorbar.set_text("You cannot have the same symbol for multiple players!")
            return False
        else:
            symbols.append(response[i])
            symboldict[int(i[-1])] = response[i] 
    return symboldict
        

def makesecondquestions(players):
    questions_dict = {}
    for i in range(1,1+players):
        questions_dict["What character do you want to represent player " + str(i)] = "character"
    totalquestions = {}
    totalquestions["Enter your player settings:"] = questions_dict
    secondary_questions = pygame_gui.elements.UIForm(relative_rect=pygame.Rect((0, 0), (400, 430)),anchors={"center":"center"},questionnaire=totalquestions)
    return secondary_questions

def getplayercolours(numpicked,manager):
    colourpicker = pygame_gui.windows.UIColourPickerDialog(rect=pygame.Rect((200,50),(400,400)),manager=manager,window_title="Select the colour for player " + str(numpicked+1))
    return colourpicker

def askaiquestion(players,manager):
    options = ["None"]
    for i in range(1,players+1):
        options.append(str(i))
    selection = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((0,0),(300,100)),manager=manager,anchors={"center":"center"},allow_multi_select=True,item_list=options,default_selection="None")
    return selection

def makewindow():

    pygame.init()

    pygame.display.set_caption('Game Settings')
    window_surface = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color('#000000'))
    manager = pygame_gui.UIManager((800, 600),'NEA/base_theme.json')
    initial_questions = pygame_gui.elements.UIForm(relative_rect=pygame.Rect((0, 0), (400, 430)),anchors={"center":"center"},questionnaire={
        "Enter the settings for your game:": {"How many columns do you want?":"integer",
                    "How many rows do you want?":"integer",
                    "How long do you want the win streak to be?":"integer",
                    "How many players do you want?":"integer",
                    "Do you want to enable gravity?":pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((0,0),(300,50)),manager=manager,item_list=["Gravity On","Gravity Off"],default_selection="Gravity Off")}})
    errorbar = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0,0),(400,35)),anchors={"top_target":initial_questions,"centerx_target":initial_questions,"centerx":"centerx"},html_text="",visible=False)
    clock = pygame.time.Clock()
    is_running = True
    checkyet = False
    while is_running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame_gui.UI_FORM_SUBMITTED:
                if event.ui_element == initial_questions:
                    response = initial_questions.get_current_values()
                    response = validateresponse1(response,errorbar)
                    if response == False:
                        errorbar.visible = 1
                    else:
                        initial_questions.kill()
                        secondary_questions = makesecondquestions(response["players"])
                        errorbar.visible = 0
                        errorbar.set_anchors({"top_target":secondary_questions,"centerx_target":secondary_questions,"centerx":"centerx"})
                elif event.ui_element == secondary_questions:
                    response2 = secondary_questions.get_current_values()
                    response2 = validateresponse2(response2,errorbar)
                    if response2 == False:
                        errorbar.visible = 1
                    else:
                        errorbar.visible = 0
                        secondary_questions.kill()
                        numcolourspicked = 0
                        colours = {}
                        colourpicker = getplayercolours(numcolourspicked,manager)
            elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                colours[numcolourspicked+1] = copy.deepcopy(colourpicker.get_colour())
                print(colours)
                numcolourspicked += 1
                if numcolourspicked == response["players"]:
                    checkyet = True
                    aiquestion = askaiquestion(response["players"],manager)
                    submit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0),(300,30)),manager=manager,text="Submit",anchors={"top_target":aiquestion,"centerx":"centerx"})
                    questions = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0,-70),(300,70)),manager=manager,html_text="Which players, if any, do you want to be played by an AI?",anchors={"bottom_target":aiquestion,"bottom":"bottom","centerx":"centerx"})
                    errorbar.kill()
                    errorbar = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0,0),(300,35)),anchors={"top_target":submit,"centerx_target":submit,"centerx":"centerx"},html_text="",visible=False)
                else:
                    colourpicker = getplayercolours(numcolourspicked,manager)
            
            elif event.type == pygame_gui.UI_WINDOW_CLOSE:
                if event.ui_element == colourpicker:
                    if numcolourspicked < response["players"]:
                        colourpicker = getplayercolours(numcolourspicked,errorbar)

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if checkyet:
                    if event.ui_element == submit:
                        aianswer = aiquestion.get_multi_selection()
                        if len(aianswer) == 0:
                            errorbar.set_text("You must select something!")
                            errorbar.visible = 1
                        elif len(aianswer) > 1 and "None" in aianswer:
                            errorbar.set_text("These options do not make sense!")
                            errorbar.visible = 1
                        else:
                            errorbar.visible = 0
                            aiplayers = []
                            if aianswer[0] != "None":
                                for i in aianswer:
                                    aiplayers.append(int(i))
                            settings = {"board_settings":response,"player_symbols":response2,"colours":colours,"ai":aiplayers}
                            pygame.quit()
                            return settings

            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    