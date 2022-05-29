
import json

from typing import Union

import PySimpleGUI as ps
from pynput import keyboard

import option


class SimpleNamespace(dict):
    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return super().__getitem__(name)

    def __setattr__(self, name, value) -> None:
        return super().__setitem__(name, value)


class Config(SimpleNamespace):
    pass


class GUI:
    INSTANCE = None # Singleton
    LAYOUT_NAME_SEPERATORS = [' ', '+', ', ', ',']
    
    def __new__(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = super().__new__(cls)
        return cls.INSTANCE

    def __setitem__(self, name, value):
        return self.add_layout(name, value)
    def __getitem__(self, name):
        return self.get_layout(name) if all([not name.__contains__(sep) for sep in self.LAYOUT_NAME_SEPERATORS]) else self.get_layouts(name)
    
    def __init__(self, **kwargs):
        self.window_kwargs = kwargs
        self.layouts = {}
        self.window = None
    
    def set_options(**kw):
        return ps.set_options(**kw)
    
    def add_layout(self, name, component_lists):
        self.layouts[name] = component_lists
        return self
    
    def get_layout(self, name):
        return self.layouts.get(name, [])
    
    def get_layouts(self, names: Union[str, list], string_sep=None):
        if isinstance(names, str):
            if string_sep is None:
                for sep in self.LAYOUT_NAME_SEPERATORS:
                    if names.split(sep) > 1:
                        string_sep = sep
                        break
            names = names.split(string_sep)
        return [self.get_layout(name) for name in names]
    
    def init_window(self, *args, **kwargs):
        window_kw = self.window_kwargs.copy()
        window_kw.update(kwargs)
        self.window = ps.Window(*args, **window_kw)
        self.window.element_list
        return self


class Game:
    def __init__(self, config: Config):
        self.config = config
        self.data_passthrough = SimpleNamespace(showResult=False, 
                                                closeResult=False,
                                                COLOR_CONVERTER={"red":"#ff0000",
                                                                 "light":"#aaaaaa",
                                                                 "dark":"#222222"
                                                                 })
        self.game_state = SimpleNamespace({name:0 for name in ['WinCount', 'lostCount', 'winStreak', 'loseStreak', 'currentWs', 'currentLs']})
        self.gui = GUI()
        
        self._init()
    
    @property
    def window(self):
        return self.gui.window

    @property
    def data(self):
        return self.data_passthrough
    
    def _init(self):
        self.create_gui()
        
        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_key_down_listener)
        self.keyboard_listener.start()
        
        self.load_save_state()
        
        return self
    
    def save_game_state(self):
        with open(self.config.save_filename, 'w') as f:
            json.dump(self.game_state, f, indent=2)
        return self
    
    def load_save_state(self):
        with open(self.config.save_filename, 'r') as f:
            self.game_state.update(json.load(f))
        return self
    
    def create_gui(self):
        TITLE = "BaGuKer"
        
        WIDTH = 600
        HEIGHT = 800

        REAL_WIDTH = WIDTH//4
        CENTER_WIDTH = REAL_WIDTH//2
        
        buttonColor = "#222222"
        backgroundColor = "#666666"
        
        titleSpace = 5
        
        self.gui.set_options(font=("Twentieth Century.ttf", 12), background_color="black")
        
        resultLayout = [
            [ps.Text("", key="PilihanUser", font=20, background_color="#aa0000"), ps.Text("VS",background_color="#550000",key="vs", font=18), ps.Text("", key="PilihanBot", font=20, background_color="#aa0000")],
            [ps.Text("", key="Keterangan", font=20, background_color="#aa0000")],
            [ps.Button("Ulang", button_color=buttonColor), ps.Text("Pencet 'R' untuk ulang")]
        ]

        self.data.allColumnKey = ["PilihanUser", "vs", "PilihanBot", "Keterangan", ""]
        self.data.allBgKey = ["kertas", "batu", "gunting", "Apply", "Save", "Exit", "random", "Ulang"]
        mainLayout = [ # Sumpah ini berantakan co
            [ps.Text("-"*(CENTER_WIDTH-len(TITLE)-titleSpace)+" "*titleSpace+TITLE+" "*titleSpace+"-"*(CENTER_WIDTH-len(TITLE)-titleSpace), background_color="#666666")],
            [ps.Text("\n"*10, background_color=backgroundColor)],
            [ps.Text(" "*(CENTER_WIDTH-25), key="t1", background_color=backgroundColor), ps.Button("🖐️", size=(5, 2), font=20, key="kertas", disabled_button_color=buttonColor, button_color=buttonColor), ps.Button("✌️", size=(5, 2), font=20, key="gunting", disabled_button_color="gray", button_color=buttonColor), ps.Button("✊", size=(5, 2), font=20, key="batu", disabled_button_color="gray", button_color=buttonColor)],
            [ps.Text(" "*(CENTER_WIDTH-6),background_color=backgroundColor), ps.Button("RANDOM", key="random", button_color=buttonColor, size=(5, 1), font=20, disabled_button_color=buttonColor)],
            [ps.Text(" "*(CENTER_WIDTH-25), key="t2", background_color=backgroundColor), ps.Text("Win : "+str(self.game_state.winCount), key="winCount", background_color=backgroundColor), ps.Text("Lost : "+str(self.game_state.lostCount), key="lostCount", background_color=backgroundColor)],
            [ps.Text(" "*(CENTER_WIDTH-25), key="t3", background_color=backgroundColor), ps.Text("Highest Win Streak : "+str(self.game_state.winStreak), key="ws", background_color=backgroundColor), ps.Text("Highest Lose Streak : "+str(self.game_state.loseStreak), key="ls", background_color=backgroundColor)],
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
        
        layout = [[ps.Column(mainLayout+optionLayout+lastLayout, background_color=backgroundColor, key="Body")]]
        
        self.gui.init_window(TITLE, layout, size=(WIDTH, HEIGHT), background_color=backgroundColor)
        return self
    
    def keyboard_key_down_listener(self, event):
        key = ''
        try:
            key = event.char
        except AttributeError:
            key = event

        if key == 'r' and self.data.showResult:
            self.window["Ulang"]._ClickHandler("Ulang")
            self.data.closeResult = True
    
    def run(self):
        while True:
            event, value = self.window.read()

            if event == ps.WIN_CLOSED or event == "Exit":
                break

            elif event == "Ulang":
                self.window["ResultContainer"].update(visible=False)
                self.window["kertas"].update(disabled=False)
                self.window["batu"].update(disabled=False)
                self.window["gunting"].update(disabled=False)

                self.data.showResult = False
                self.data.closeResult = False

            elif event == "Apply":
                selectedButtonBackground = self.data.COLOR_CONVERTER[value["ButtonBackgroundSelect"].lower()]
                selectedResultBackground = self.data.COLOR_CONVERTER[value["ResultBackgroundSelect"].lower()]
                [self.window[item].Widget.config(background=selectedButtonBackground) for item in self.data.allBgKey]
                self.window["ResultContainer"].update(background_color=selectedResultBackground)

            elif event == "random":
                choice = str(option.Option.random()).lower()
                self.window[choice]._ClickHandler(choice)

            elif event == "Save":
                self.save_game_state()

            else:
                self.window["kertas"].update(disabled=True)
                self.window["batu"].update(disabled=True)
                self.window["gunting"].update(disabled=True)
                opsiPemain = event
                if opsiPemain == "kertas":
                    opsiPemain = option.Kertas
                elif opsiPemain == "batu":
                    opsiPemain = option.Batu
                else:
                    opsiPemain = option.Gunting

                enemyPick = option.Option.random()
                result = opsiPemain.beats(enemyPick)

                if result is True:
                    self.game_state.winCount += 1
                    self.game_state.currentWs += 1
                    self.game_state.currentLs = 0
                    if self.game_state.currentWs > self.game_state.winStreak:
                        self.game_state.winStreak = self.game_state.currentWs
                elif result == -1:
                    self.game_state.currentLs = 0
                    self.game_state.currentWs = 0
                else:
                    self.game_state.lostCount += 1
                    self.game_state.currentLs += 1
                    self.game_state.currentWs = 0
                    if self.game_state.currentLs > self.game_state.loseStreak:
                        self.game_state.loseStreak = self.game_state.currentLs

                description = "Menang Yey" if description is True else "Kalah :(" if description is False else "Seri!"

                self.window["PilihanUser"].update(opsiPemain.display_char)
                self.window["PilihanBot"].update(enemyPick.display_char)
                self.window["Keterangan"].update(description)
                self.window["Spaces"].update("\n"*6)
                self.window["ResultContainer"].update(visible=True)
                self.window["winCount"].update("Win : "+str(self.game_state.winCount))
                self.window["lostCount"].update("Lost : "+str(self.game_state.lostCount))
                self.window["ws"].update("Highest Win Streak : "+str(self.game_state.winStreak))
                self.window["ls"].update("Highest Lose Streak : "+str(self.game_state.loseStreak))

                self.data_passthrough.showResult = True
        self.window.close()


config = Config(save_filename='save.json')


if __name__ == '__main__':
    game = Game(config)
    game.run()
