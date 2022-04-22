import random
import PySimpleGUI as ps
import option

from pynput import keyboard



def enemy_pick_randomizer():
    return random.choice([option.Batu, option.Kertas, option.Gunting])


STRING_CONVERTER = {
    "kertas":"🖐️",
    "batu":"✊",
    "gunting":"✌️"
}

TITLE = "BaGuKer"
WIDTH = 600
HEIGHT = 800

REALWIDTH = WIDTH//4
REALHEIGHT = HEIGHT//4

CENTERWIDTH = REALWIDTH//2
CENTERHEIGHT = REALHEIGHT//2

titleSpace = 5
resultLayout = [
    [ps.Text("", key="PilihanUser", font=20, background_color="#aa0000"), ps.Text("VS",background_color="#550000", font=18), ps.Text("", key="PilihanBot", font=20, background_color="#aa0000")],
    [ps.Text("", key="Keterangan", font=20, background_color="#aa0000")],
    [ps.Button("Ulang"), ps.Text("Pencet 'R' untuk ulang")]
]

mainLayout = [ # Sumpah ini berantakan co
    [ps.Text("-"*(CENTERWIDTH-len(TITLE)-titleSpace)+" "*titleSpace+TITLE+" "*titleSpace+"-"*(CENTERWIDTH-len(TITLE)-titleSpace))],
    [ps.Text("\n"*10)],
    [ps.Text(" "*(CENTERWIDTH-25)), ps.Button("🖐️", size=(5, 2), font=20, key="kertas", disabled_button_color="gray"), ps.Button("✌️", size=(5, 2), font=20, key="gunting", disabled_button_color="gray"), ps.Button("✊", size=(5, 2), font=20, key="batu", disabled_button_color="gray")],
    [ps.Text(" "*(CENTERWIDTH-25)), ps.Text("Win : ", key="winCount"), ps.Text("Lost : ", key="lostCount")],
    [ps.Column(resultLayout, visible=False, justification="center", key="ResultContainer", background_color="#aa0000", size=(300, 150))]
]

lastLayout = [
    [ps.Text("\n"*15, key="Spaces")],
    [ps.Button('Exit')]
]


layout = mainLayout+lastLayout
window = ps.Window(title=TITLE, layout=layout, size=(WIDTH, HEIGHT))
showResult = False
closeResult = False

winCount = 0
lostCount = 0

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

        if description:
            winCount += 1
        else:
            lostCount += 1

        description = "Menang Yey" if description else "Kalah :("

        window["PilihanUser"].update(STRING_CONVERTER[opsiPemain.__str__().lower()])
        window["PilihanBot"].update(STRING_CONVERTER[enemyPick.__str__().lower()])
        window["Keterangan"].update(description)
        window["Spaces"].update("\n"*6)
        window["ResultContainer"].update(visible=True)
        window["winCount"].update("Win : "+str(winCount))
        window["lostCount"].update("Lost : "+str(lostCount))

        showResult = True

window.close()
