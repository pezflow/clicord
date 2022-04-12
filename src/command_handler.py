class CommandHandler:
    def __init__(self,client):
        self.list = {
            "channelid": self.switch_channel,
            "serverid": self.switch_guild,
            "s": self.switch_guild_by_keyword,
            "c": self.switch_channel_by_keyword
        }
        self.client = client
    
    async def run_string(self,string):
        command = string.replace("/","")
        args = command.split(" ")
        if args[0] in self.list:
            await self.list[args[0]](args)

    async def switch_channel(self,args):
        try:
            channel = await self.client.fetch_channel(int(args[1]))
            await self.client.set_channel(channel)
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid channel: {e}")
        pass

    async def switch_guild(self,args):
        try:
            guild = int(args[1])
            await self.client.set_guild(await self.client.fetch_guild(guild),True)
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid guild: {e}")
        pass
    
    async def switch_channel_by_keyword(self,args):
        try:
            key = args[1].lower()
            for channel in self.client.channel.guild.text_channels:
                if key in channel.name.lower():
                    await self.client.set_channel(channel)
                    self.client.ui.append_text_log("SYS",f"Successfully connected to {self.client.channel.name}")
                    return
            self.client.ui.append_text_log("SYS",f"No channel found with key {key}!")
            
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid name! {e}")

    async def switch_guild_by_keyword(self,args):
        try:
            key = args[1].lower()
            for guild in self.client.guilds:
                if key in guild.name.lower():
                    await self.client.set_guild(guild,True)
                    self.client.ui.append_text_log("SYS",f"Successfully connected to {self.client.guild.name}")
                    return
            self.client.ui.append_text_log("SYS",f"No server found with keyword {key}!")
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid name! {e}")