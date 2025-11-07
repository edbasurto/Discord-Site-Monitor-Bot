import os
from discord.ext import commands
import src.main as main

ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID", "0"))

# Cog to handle the incoming commands and send message to channel
class MonitorCog(commands.Cog):
    
    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.alert_channel_id = ALERT_CHANNEL_ID
    
    # Sends a message to the designated alert channel with the site name that is down. passing ip in case you want to display ip as well
    async def send_alert(self, site: str, ip_address: str, status: int, status_code: int = None):
        # Checking if alert channel id was set in .env
        if not self.alert_channel_id:
            print("Channel to send alerts is not set! Make sure to set the ID in the .env file!")
            return
        
        channel = self.bot.get_channel(self.alert_channel_id)
        # Checking if channel can be found
        if not channel:
            print("Could not find the alert channel {self.alert_channel_id}, are you sure you typed in the ID right in the .env?")
            return
        
        if status == 0:
            # Message to send in alert channel
            message = f"🚨 **ALERT:** `{site}` appears to be **DOWN**! Please head out to site ASAP!"
        else:
            message = f"🥳🎉 **SUCCESS!** `{site}` is back up and running!"
        if status_code:
            message += f" (HTTP {status_code})"
        # Sends the message to the alert channel
        await channel.send(message)

    @commands.command(name="unreachable")
    async def send_unreachable(self, ctx):
        from src import main
        print("main module id in cog:", id(main))
        unreachable = main.get_unreachable_addresses()        
        print(unreachable)
        if not unreachable:
            await ctx.send("All sites are currently reachable!")
        else:
            formatted = "\n".join(f"{name} ({ip})" for name, ip in unreachable.items())
            await ctx.send(f"**Unreachable sites:**\n```\n{formatted}\n```")

    # Test command to ensure commands work
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send("🏓 Pong! Bot is working! :YukinaHyperPog:")


async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
