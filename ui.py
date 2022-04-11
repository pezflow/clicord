from rich.layout import Layout
from rich.panel import Panel
from pynput import keyboard
import json


allowed_keys = list("1234567890-=/*-!" + '"' + "£$%^&*()_+qwertyuiop[]#QWERTYUIOP{}~asdfghjkl;'ASDFGHJKL:@zxcvbnm,./ZXCVBNM<>? \|")
class UI:
    def __init__(self):
        
        self.settings_file = open("settings.json")
        self.settings = json.loads(self.settings_file.read())

        self.layout = Layout()
        self.layout.split_column(
            Layout(name="top"),
            Layout(name="bottom")
        )
        self.layout["top"].split_row(
            Layout(name="left"),
            Layout(name="main")
        )

        self.layout["bottom"].split_row(
            Layout(name="account"),
            Layout(name="input")
        )
        self.layout["top"]["main"].ratio = 4
        self.layout["top"].ratio = 12
        self.layout["bottom"]["input"].ratio = 4

        self.guild_name = "connecting..."
        self.channel_name = "connecting..."
        self.username = "user#9999"
        self.channels = []
        self.text_log = []

        self.inputted_text = ""
        self.inputkeys = []
        self.send_message = False

        self.username_color = "[" + self.settings["username_color"] + "]" 
        self.panel_title_color = "[" + self.settings["panel_title_color"] + "]"
        self.text_color = "[" + self.settings["text_color"] + "]"

        self.refresh()
    
    def update_typing_box(self,key):
        if key == keyboard.Key.backspace:
            if len(self.inputkeys) > 0:
                self.inputkeys.pop(len(self.inputkeys)-1)
        elif key == keyboard.Key.enter:
            if len(self.inputkeys) > 0:
                self.inputkeys = []
                self.send_message = True
                return
        elif key == keyboard.Key.space:
            self.inputkeys.append(" ")
        else:
            try:
                if key.char in allowed_keys:
                    self.inputkeys.append(key.char)
            except:
                pass

        self.inputted_text = "".join(self.inputkeys)

    def append_text_log(self,author,text):
        self.text_log.append(f"{self.username_color}{author}:{self.text_color} {text}")
        if "\n".join(self.text_log).count("\n") > 25:
            while "\n".join(self.text_log).count("\n") > 25:
                self.text_log.pop(0)
        
    def refresh(self):
        self.layout["top"]["left"].update(Panel("\n".join(self.channels),title=f"{self.panel_title_color}{self.guild_name}",border_style=self.settings["accent_color"]))

        self.layout["bottom"]["input"].update(Panel(
            self.inputted_text,
            title=f"{self.panel_title_color}Talk in #{self.channel_name}",
            border_style=self.settings["accent_color"]))

        self.layout["bottom"]["account"].update(Panel(
            self.username,
            title=f"{self.panel_title_color}Your account",
            border_style=self.settings["accent_color"]))

        self.layout["top"]["main"].update(Panel(
            "\n".join(self.text_log),
            title=f"{self.panel_title_color}#{self.channel_name}",
            border_style=self.settings["accent_color"]))
    
