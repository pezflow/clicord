from discord.ext import commands
from rich.live import Live
from ui import UI
from pynput import keyboard
import asyncio 

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/")

        self.ui = UI()
        self.remove_command("help") 
        self.loop.create_task(self.ui_refresh())
        self.kb_listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.kb_listener.start()
        self.guild_id = 0
        self.channel_id = 0
        self.run()

    def on_press(self,key):
        self.ui.update_typing_box(key)
    
    def on_release(self,key):
        pass
    
    async def on_ready(self):
        self.guild = await self.fetch_guild(self.guild_id)
        self.channel = await self.fetch_channel(self.channel_id)
        self.ui.server_name = self.guild.name
        self.ui.channel_name = self.channel.name
        self.ui.username = f"{self.user.name}#{self.user.discriminator}"

        msgs = await self.channel.history(limit=20).flatten()
        msgs.reverse()

        for channel in self.guild.text_channels:
            print(channel)
        for m in msgs:
            self.ui.append_text_log(f"{m.author.name}#{m.author.discriminator}",m.clean_content)

    async def on_message(self,message):
        if message.channel.id == self.channel_id:
            async for m in message.channel.history(limit=1):
                self.ui.append_text_log(f"{m.author.name}#{m.author.discriminator}",m.clean_content)

    async def ui_refresh(self):
        await self.wait_until_ready()
        with Live(self.ui.layout,refresh_per_second=30,screen=True) as live:
            while True:
                self.ui.refresh()
                if self.ui.send_message:
                    self.ui.send_message = False
                    await self.channel.send(self.ui.inputted_text)
                await asyncio.sleep(.04)

    def run(self):
        token = "YOUR TOKEN HERE"
        try:
            super().run(token,bot=False)
        except Exception as e:
            print(e)