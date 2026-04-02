import asyncio
import os
from discord.ext import commands
import src.main as main

ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID", "0"))
MONITOR_ROLE_ID = int(os.getenv("MONITOR_ROLE_ID", "0"))

def requires_monitor_role():
    async def predicate(ctx):
        if not MONITOR_ROLE_ID:
            await ctx.send("❌ `MONITOR_ROLE_ID` is not set in the .env file. This command is disabled.")
            return False
        if any(role.id == MONITOR_ROLE_ID for role in ctx.author.roles):
            return True
        await ctx.send("❌ You don't have permission to use this command.")
        return False
    return commands.check(predicate)

# Cog to handle the incoming commands and send message to channel
class MonitorCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
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
            print(f"Could not find the alert channel {self.alert_channel_id}, are you sure you typed in the ID right in the .env?")
            return

        if status == 0:
            # Message to send in alert channel
            message = f"🚨 **ALERT:** `{site}` appears to be **DOWN**!"
        else:
            message = f"🥳🎉 **SUCCESS!** `{site}` is back up and running!"
        if status_code:
            message += f" (HTTP {status_code})"
        # Sends the message to the alert channel
        await channel.send(message)

    @commands.command(name="status")
    async def send_status(self, ctx):
        message = main.get_ping_status()
        if not message or not message.strip():
            await ctx.send("No status has been recorded yet. Please wait at least 10 seconds.")
        else:
            await ctx.send(f"```{message}```")

    @commands.command(name="sites")
    async def send_sites(self, ctx):
        addresses = main.get_addresses()
        if not addresses:
            await ctx.send("No sites are being monitored.")
        else:
            formatted = "\n".join(f"{name}: {ip}" for name, ip in addresses.items())
            await ctx.send(f"**Monitored sites:**\n```\n{formatted}\n```")

    @commands.command(name="unreachable")
    async def send_unreachable(self, ctx):
        unreachable = main.get_unreachable_addresses()
        if not unreachable:
            await ctx.send("All sites are currently reachable!")
        else:
            formatted = "\n".join(f"{name} ({ip})" for name, ip in unreachable.items())
            await ctx.send(f"**Unreachable sites:**\n```\n{formatted}\n```")

    @requires_monitor_role()
    @commands.command(name="add")
    async def add_site_command(self, ctx, name: str, ip: str):
        if name in main.get_all_addresses():
            await ctx.send(f"❌ `{name}` already exists. Use `-update` to change its IP or name.")
            return

        await ctx.send(f"Testing ping for `{name}` ({ip})...")
        ping_ms = await main.ping_site(ip)

        if ping_ms is not None:
            main.add_site(name, ip)
            await ctx.send(f"✅ Added!\nSite: {name}\nIP: {ip}\nPing: {ping_ms:.2f}ms")
        else:
            await ctx.send(f"⚠️ Could not reach `{ip}`. Add it anyway? (yes/no)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel \
                       and m.content.lower() in ["yes", "no"]

            try:
                reply = await self.bot.wait_for('message', check=check, timeout=30.0)
                if reply.content.lower() == "yes":
                    main.add_site(name, ip)
                    await ctx.send(f"Added (ping failed)!\nSite: {name}\nIP: {ip}")
                else:
                    await ctx.send("Cancelled.")
            except asyncio.TimeoutError:
                await ctx.send("Timed out. Site was not added.")

    @requires_monitor_role()
    @commands.command(name="update")
    async def update_site_command(self, ctx, identifier: str, new_value: str):
        addresses = main.get_addresses()

        if identifier in addresses:
            old_ip = addresses[identifier]
            main.update_site_ip(identifier, new_value)
            await ctx.send(f"✅ Updated `{identifier}`: `{old_ip}` → `{new_value}`")
        else:
            match = next((n for n, i in addresses.items() if i == identifier), None)
            if not match:
                await ctx.send(f"❌ No site found with name or IP `{identifier}`.")
                return
            main.update_site_name(match, new_value)
            await ctx.send(f"✅ Renamed `{match}` → `{new_value}` ({identifier})")

    @requires_monitor_role()
    @commands.command(name="remove")
    async def remove_site_command(self, ctx, identifier: str):
        addresses = main.get_addresses()

        if identifier in addresses:
            name, ip = identifier, addresses[identifier]
        else:
            match = next((n for n, i in addresses.items() if i == identifier), None)
            if not match:
                await ctx.send(f"❌ No site found with name or IP `{identifier}`.")
                return
            name, ip = match, identifier

        main.remove_site(name)
        await ctx.send(f"🗑️ Removed `{name}` ({ip}) from monitoring.")

    @commands.command(name="help")
    async def help_command(self, ctx):
        await ctx.send(
            "**Site Monitor Commands**\n"
            "```\n"
            "-status               Show ping status of all monitored sites\n"
            "-sites                List all monitored sites and their IPs\n"
            "-unreachable          List all sites currently down\n"
            "-add [name] [ip]      Add a site to monitoring\n"
            "-update [name] [ip]   Update a site's IP (or pass IP then new name to rename)\n"
            "-remove [name/ip]     Remove a site from monitoring\n"
            "-ping                 Check if the bot is responsive\n"
            "```\n"
            "*Note: -add and -remove require the monitor role.*"
        )

    # Test command to ensure commands work
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send("🏓 Pong! Bot is working! :YukinaHyperPog:")


async def setup(bot):
    await bot.add_cog(MonitorCog(bot))
