import random
import PySimpleGUI as ps
from option import Option
import option

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
    [ps.Button("Ulang")]
]

mainLayout = [ # Sumpah ini berantakan co
    [ps.Text("-"*(CENTERWIDTH-len(TITLE)-titleSpace)+" "*titleSpace+TITLE+" "*titleSpace+"-"*(CENTERWIDTH-len(TITLE)-titleSpace))],
    [ps.Text("\n"*10)],
    [ps.Text(" "*(CENTERWIDTH-25)), ps.Button("🖐️", size=(5, 2), font=20, key="kertas", disabled_button_color="gray"), ps.Button("✌️", size=(5, 2), font=20, key="gunting", disabled_button_color="gray"), ps.Button("✊", size=(5, 2), font=20, key="batu", disabled_button_color="gray")],
    [ps.Column(resultLayout, visible=False, justification="center", key="ResultContainer", background_color="#aa0000", size=(300, 150))]
]

lastLayout = [
    [ps.Text("\n"*15, key="Spaces")],
    [ps.Button('Exit')]
]

layout = mainLayout+lastLayout
window = ps.Window(title=TITLE, layout=layout, size=(WIDTH, HEIGHT))

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
        description = "Menang Yeyy" if description else "Kalah :("

        window["PilihanUser"].update(STRING_CONVERTER[opsiPemain.__str__().lower()])
        window["PilihanBot"].update(STRING_CONVERTER[enemyPick.__str__().lower()])
        window["Keterangan"].update(description)
        window["Spaces"].update("\n"*6)
        window["ResultContainer"].update(visible=True)

window.close()
