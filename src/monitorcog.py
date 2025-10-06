import os
from discord.ext import commands

ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID", "0"))

# Cog to handle the incoming commands and send message to channel
class MonitorCog(commands.Cog):
    
    def __init__(self, bot: commands.Cog):
        self.bot = bot
        self.alert_channel_id = ALERT_CHANNEL_ID
    
    # Sends a message to the designated alert channel with the site name that is down. passing ip in case you want to display ip as well
    async def send_alert(self, site: str, ip_address: str, status_code: int = None):
        # Checking if alert channel id was set in .env
        if not self.alert_channel_id:
            print("Channel to send alerts is not set! Make sure to set the ID in the .env file!")
            return
        
        channel = self.bot.get_channel(self.alert_channel_id)
        # Checking if channel can be found
        if not channel:
            print("Could not find the alert channel {self.alert_channel_id}, are you sure you typed in the ID right in the .env?")
            return
        
        # Message to send in alert channel
        message = f"🚨 **ALERT:** `{site}` appears to be **DOWN**! Please head out to site ASAP!"
        if status_code:
            message += f" (HTTP {status_code})"
        # Sends the message to the alert channel
        await channel.send(message)
    
    # Test command to ensure commands work
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send("🏓 Pong! Bot is working! :YukinaHyperPog:")


async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
