
import random
import PySimpleGUI as ps
import option
import os
from pynput import keyboard


def start():
    listDir = os.path.dirname(os.path.realpath(__file__))
    import save

    SAVE_FILE_PATH = listDir+r"\save.py"
    def enemy_pick_randomizer():
        return random.choice([option.Batu, option.Kertas, option.Gunting])


    STRING_CONVERTER = {
        "kertas":"🖐️",
        "batu":"✊",
        "gunting":"✌️"
    }

    COLOR_CONVERTER = {
        "red":"#ff0000",
        "light":"#aaaaaa",
        "dark":"#222222"
    }

    TITLE = "BaGuKer"
    WIDTH = 600
    HEIGHT = 800

    REALWIDTH = WIDTH//4
    REALHEIGHT = HEIGHT//4

    CENTERWIDTH = REALWIDTH//2
    CENTERHEIGHT = REALHEIGHT//2

    ps.set_options(font=("Twentieth Century.ttf", 12), background_color="black")

    winCount = save.WinCount
    lostCount = save.LostCount

    winStreak = save.WinStreak
    loseStreak = save.LoseStreak
    currentWs = save.CurrentWS
    currentLs = save.CurrentLS

    buttonColor = "#222222"
    backgroundColor = "#666666"

    titleSpace = 5
    resultLayout = [
        [ps.Text("", key="PilihanUser", font=20, background_color="#aa0000"), ps.Text("VS",background_color="#550000",key="vs", font=18), ps.Text("", key="PilihanBot", font=20, background_color="#aa0000")],
        [ps.Text("", key="Keterangan", font=20, background_color="#aa0000")],
        [ps.Button("Ulang", button_color=buttonColor), ps.Text("Pencet 'R' untuk ulang")]
    ]

    allColumnKey = ["PilihanUser", "vs", "PilihanBot", "Keterangan", ""]
    allBgKey = ["kertas", "batu", "gunting", "Apply", "Save", "Exit", "random", "Ulang"]
    mainLayout = [ # Sumpah ini berantakan co
        [ps.Text("-"*(CENTERWIDTH-len(TITLE)-titleSpace)+" "*titleSpace+TITLE+" "*titleSpace+"-"*(CENTERWIDTH-len(TITLE)-titleSpace), background_color="#666666")],
        [ps.Text("\n"*10, background_color=backgroundColor)],
        [ps.Text(" "*(CENTERWIDTH-25), key="t1", background_color=backgroundColor), ps.Button("🖐️", size=(5, 2), font=20, key="kertas", disabled_button_color=buttonColor, button_color=buttonColor), ps.Button("✌️", size=(5, 2), font=20, key="gunting", disabled_button_color="gray", button_color=buttonColor), ps.Button("✊", size=(5, 2), font=20, key="batu", disabled_button_color="gray", button_color=buttonColor)],
        [ps.Text(" "*(CENTERWIDTH-6),background_color=backgroundColor), ps.Button("RANDOM", key="random", button_color=buttonColor, size=(5, 1), font=20, disabled_button_color=buttonColor)],
        [ps.Text(" "*(CENTERWIDTH-25), key="t2", background_color=backgroundColor), ps.Text("Win : "+str(winCount), key="winCount", background_color=backgroundColor), ps.Text("Lost : "+str(lostCount), key="lostCount", background_color=backgroundColor)],
        [ps.Text(" "*(CENTERWIDTH-25), key="t3", background_color=backgroundColor), ps.Text("Highest Win Streak : "+str(winStreak), key="ws", background_color=backgroundColor), ps.Text("Highest Lose Streak : "+str(loseStreak), key="ls", background_color=backgroundColor)],
        [ps.Column(resultLayout, visible=False, justification="center", key="ResultContainer", background_color="#222222", size=(300, 150))]
    ]

    validBackground = ["Dark", "Red", "Light"]
    optionLayout = [
        [ps.Text("Button Background : ", background_color=backgroundColor), ps.Spin(validBackground, key="ButtonBackgroundSelect")],
        [ps.Text("Result Background : ", background_color=backgroundColor), ps.Spin(validBackground, key="ResultBackgroundSelect")],
        [ps.Button("Apply", button_color=buttonColor)],
        [ps.Button("Save", button_color=buttonColor)]
    ]

    lastLayout = [
        [ps.Text("\n"*4, background_color=backgroundColor, key="Spaces")],
        [ps.Button('Exit', button_color=buttonColor)]
    ]


    Layout = [[ps.Column(mainLayout+optionLayout+lastLayout, background_color=backgroundColor, key="Body")]]

    window = ps.Window(TITLE, Layout, size=(WIDTH, HEIGHT), background_color=backgroundColor)
    showResult = False
    closeResult = False

    def change_bg(col:str, col2):
        for item in allBgKey:
            window[item].Widget.config(background=col)

        window["ResultContainer"].update(background_color=col2)


    def get_key_down(e):
        global closeResult
        key = ''
        try:
            key = e.char
        except AttributeError:
            key = e

        if key == 'r' and showResult:
            window["Ulang"]._ClickHandler("Ulang")
            closeResult = True


    listener = keyboard.Listener(on_press=get_key_down)
    listener.start()

    opsiPemain = ""
    run = True
    while run:
        event, value = window.read()

        if event == ps.WIN_CLOSED or event == "Exit":
            break

        elif event == "Ulang":
            window["ResultContainer"].update(visible=False)
            window["kertas"].update(disabled=False)
            window["batu"].update(disabled=False)
            window["gunting"].update(disabled=False)

            showResult = False
            closeResult = False

        elif event == "Apply":
            selectedButtonBackground = COLOR_CONVERTER[value["ButtonBackgroundSelect"].lower()]
            selectedResultBackground = COLOR_CONVERTER[value["ResultBackgroundSelect"].lower()]
            change_bg(selectedButtonBackground, selectedResultBackground)

        elif event == "random":
            choice = random.choice(["batu", "gunting", "kertas"])
            window[choice]._ClickHandler(choice)

        elif event == "Save":
            f = open(SAVE_FILE_PATH, 'w+')
            f.write(f'''WinCount = {winCount}
    LostCount = {lostCount}
    WinStreak = {winStreak}
    LoseStreak = {loseStreak}
    CurrentWS = {currentWs}
    CurrentLS = {currentLs}''')
            f.close()

        else:
            window["kertas"].update(disabled=True)
            window["batu"].update(disabled=True)
            window["gunting"].update(disabled=True)
            opsiPemain = event
            if opsiPemain == "kertas":
                opsiPemain = option.Kertas
            elif opsiPemain == "batu":
                opsiPemain = option.Batu
            else:
                opsiPemain = option.Gunting

            enemyPick = enemy_pick_randomizer()
            description = opsiPemain.beats(enemyPick)

            if description is True:
                winCount += 1
                currentWs += 1
                currentLs = 0
                if currentWs > winStreak:
                    winStreak = currentWs
            elif description == -1:
                currentLs = 0
                currentWs = 0
            else:
                lostCount += 1
                currentLs += 1
                currentWs = 0
                if currentLs > loseStreak:
                    loseStreak = currentLs

            description = "Menang Yey" if description is True else "Kalah :(" if description is False else "Seri!"

            window["PilihanUser"].update(STRING_CONVERTER[opsiPemain.__str__().lower()])
            window["PilihanBot"].update(STRING_CONVERTER[enemyPick.__str__().lower()])
            window["Keterangan"].update(description)
            window["Spaces"].update("\n"*6)
            window["ResultContainer"].update(visible=True)
            window["winCount"].update("Win : "+str(winCount))
            window["lostCount"].update("Lost : "+str(lostCount))
            window["ws"].update("Highest Win Streak : "+str(winStreak))
            window["ls"].update("Highest Lose Streak : "+str(loseStreak))

            showResult = True

    window.close()
