from rich.layout import Layout
from rich.panel import Panel
from pynput import keyboard

allowed_keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!" + '"' + "$%^&*(){}[]-_+='.,:;@#~|")
class UI:
    def __init__(self):
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

        self.server_name = "connecting..."
        self.channel_name = "connecting..."
        self.username = "user#9999"
        self.channels = ["#general","#commands","#help"]
        self.text_log = []

        self.inputted_text = ""
        self.inputkeys = []
        self.send_message = False
        self.i = 0

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
        self.text_log.append(f"[red]{author}:[white] {text}")
        if len(self.text_log) > 25:
            self.text_log.pop(0)
        
    def refresh(self):
        self.layout["top"]["left"].update(Panel("\n".join(self.channels),title=f"[white]{self.server_name}",border_style="purple"))

        self.layout["bottom"]["input"].update(Panel(self.inputted_text,title=f"[white]Talk in #{self.channel_name}",border_style="purple"))
        self.layout["bottom"]["account"].update(Panel(self.username,title="[white]Your account",border_style="purple"))
        self.layout["top"]["main"].update(Panel("\n".join(self.text_log),title=f"[white]#{self.channel_name}",border_style="purple"))
    