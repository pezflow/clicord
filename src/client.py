from discord.ext import commands
from command_handler import CommandHandler
from rich.live import Live
from ui import UI
from pynput import keyboard
import asyncio 
import json

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/")
        self.settings_file = open("../settings.json")
        self.settings = json.loads(self.settings_file.read())
        self.theme_file = open(self.settings["theme"])
        self.theme = json.loads(self.theme_file.read())

        self.ui = UI()
        self.remove_command("help") 

        self.loop.create_task(self.ui_refresh())
        self.loop.create_task(self.message_loop())
        
        self.kb_listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.kb_listener.start()

        self.channel_id = self.settings["channel_id"]
        
        self.command_handler = CommandHandler(self)
        self.run()

    def on_press(self,key):
        self.ui.update_typing_box(key)
    
    def on_release(self,key):
        pass
    
    async def process_message(self,m):
        txt = "" + m.clean_content
        if len(m.attachments) > 0:
            txt += f"[{len(m.attachments)} attachment(s)]"
        if m.reference:
           async for search in m.channel.history(limit=50):
                if search.id == m.reference.message_id:
                    username_color = self.theme["username_color"]
                    text_color = self.theme["text_color"]
                    txt = f"[{username_color}]reply to {search.author}:{search.clean_content}\n[{text_color}]" + txt 
        
        self.ui.append_text_log(f"{m.author.name}#{m.author.discriminator}",txt)

    async def set_channel(self,channel):
        self.channel = channel
        self.channel_id = channel.id
        self.ui.channel_name = self.channel.name
        self.ui.text_log = []
        try:
            msgs = await self.channel.history(limit=20).flatten()
            msgs.reverse()

            for m in msgs:
                await self.process_message(m)
        except Exception as e:
            self.ui.append_text_log("SYS",f"unable to load messages! {e}")

        await self.set_guild(self.channel.guild,False)

    async def set_guild(self,guild,change_channel):
        self.guild = guild
        self.guild_id = guild.id
        self.ui.guild_name = guild.name
        self.ui.channels = []
        for channel in guild.text_channels:
            self.ui.channels.append(channel.name)
        
        if change_channel:
            await self.set_channel(guild.text_channels[0])

    async def on_ready(self):
        await self.set_channel(await self.fetch_channel(self.channel_id))
        self.ui.username = f"{self.user.name}#{self.user.discriminator}"
        for guild in self.guilds:
            self.ui.guilds.append(guild.name)

    async def on_message(self,message):
        if message.channel.id == self.channel_id:
            async for m in message.channel.history(limit=1):
                await self.process_message(m)

    async def ui_refresh(self):
        await self.wait_until_ready()
        with Live(self.ui.layout,refresh_per_second=30,screen=True) as live:
            while True:
                self.ui.refresh()
                await asyncio.sleep(.04)

    async def message_loop(self):
        await self.wait_until_ready()
        while True:
            if self.ui.send_message:
                self.ui.send_message = False
                if self.ui.inputted_text.startswith("/"):
                    await self.command_handler.run_string(self.ui.inputted_text)
                else:
                    await self.channel.send(self.ui.inputted_text)
                self.ui.inputted_text = ""
            await asyncio.sleep(.04)

    def run(self):
        try:
            super().run(self.settings["token"],bot=self.settings["is_a_bot_token"])
        except Exception as e:
            print(e)
            