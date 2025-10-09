# Site Monitor
This is a Discor Bot that will monitor given IP addresses. If one of them is unreachable, the bot will send a message in the given channel alerting that one of the addresses is down.

I have included a file called sites.json.example that you can modify to look something like the following:

{
  "Gaming PC": "192.168.255.57",
  "NAS": "192.168.255.5",
  "Home Server": "192.168.255.75"
}

I have also included a file called .env.example where you will need to add the discord token and alert channel id.

The bot will not working without these two!

**IMPORTANT!** Make sure to also remove the ".example" from the files so they are sites.json and .env, or just create the two files separately.

Default time is set to every 10 seconds. If you want to change this, go to src/main.py and on line 48, change the number inside asyncio.sleep() to however many seconds you want.
