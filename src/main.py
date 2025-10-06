import asyncio
from asyncping3 import ping, verbose_ping
import json
import time
import math
from src.bot import bot, start_bot

#async def sitePing():

def secToMillisec(seconds: float):
    return seconds * 1000

async def pingSites(sites: dict):
    unreachable = []
    for key, ip in sites.items():
        try:
            pingSeconds = await ping(ip)
            #print(pingSeconds)
            if pingSeconds is None:
                print(f"{key} at {ip} is unreachable!")
                # ADDED THESE TWO NEW LINES
                unreachable.append(ip)
                cog = bot.get_cog("MonitorCog")
                if cog:
                    await cog.send_alert(site=key, ip_address=ip)
                print("{key}")
            else:
                pingMilliseconds = secToMillisec(float(pingSeconds))
                pingTimeStr = str(math.floor(pingMilliseconds * 100)/100.0)
                print(key, ": " + pingTimeStr + " ms")
        except Exception as e:
            print(f"{key}: Error occured - {e}")
    return unreachable

async def monitor_loop():
    # Read from teh JSON file
    f = open("sites.json")
    jsonString = f.read()
    f.close()

    # Convert the loaded JSON file to dict
    addresses = json.loads(jsonString)

    # Have this always running so it always pings
    while True:
        await pingSites(addresses)
        print("\n")
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        start_bot(),
        monitor_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
