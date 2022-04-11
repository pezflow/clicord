from discord.ext import commands
class CommandHandler:
    def __init__(self,client):
        self.list = {
            "channelid": self.switch_channel,
            "serverid": self.switch_guild,
            "channelname": self.switch_channel_by_name,
            "servername": self.switch_server_by_name
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
            await self.client.set_guild(channel.guild)
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid channel: {e}")
        pass

    async def switch_guild(self,args):
        try:
            guild = int(args[1])
            await self.client.set_guild(await self.client.fetch_guild(guild))
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid guild: {e}")
        pass
    
    async def switch_channel_by_name(self,args):
        try:
            name = args[1]
            for channel in self.client.channel.guild.channels:
                if channel.name == name:
                    await self.client.set_channel(channel)
                    self.client.ui.append_text_log("SYS",f"Successfully connected to {name}")
                    return
            self.client.ui.append_text_log("SYS",f"Unable to connect to {name}")
            
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid name! {e}")

    async def switch_server_by_name(self,args):
        try:
            name = args[1]
            for guild in self.client.guilds:
                if guild.name == name:
                    await self.client.set_guild(guild)
                    self.client.ui.append_text_log("SYS",f"Successfully connected to {name}")
                    return
            self.client.ui.append_text_log("SYS",f"Unable to connect to {name}")
            
        except Exception as e:
            self.client.ui.append_text_log("SYS",f"Invalid name! {e}")
