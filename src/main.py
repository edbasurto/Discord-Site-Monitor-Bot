import asyncio
from asyncping3 import ping, verbose_ping
import json
import time
import math
from src.bot import bot, start_bot

#async def sitePing():

# Define global variables
unreachable = []

def secToMillisec(seconds: float):
    return seconds * 1000

async def pingSites(sites: dict):
    cog = bot.get_cog("MonitorCog")
    for key, ip in sites.items():
        try:
            pingSeconds = await ping(ip)
            #print(pingSeconds)
            noPingCount = 0
            while(pingSeconds is None and noPingCount < 3):
                print(f"Ping count {noPingCount}")
                pingSeconds = await ping(ip)
                noPingCount += 1
                await asyncio.sleep(0.5)
            print(f"{ip}")
            print(unreachable)
            if ip in unreachable:
                print("in the list")
            else:
                print("not in the list")
            if ip in unreachable:
                if noPingCount == 3:
                    print(f"{ip} is currently down, skipping bot command")
                else:
                    print(f"{ip} is back up! Removing from unreachable list and sending discord message")
                    pingMilliseconds = secToMillisec(float(pingSeconds))
                    pingTimeStr = str(math.floor(pingMilliseconds * 100)/100.0)
                    print(f"{key}: {pingTimeStr}ms")
                    unreachable.remove(ip)
                    if cog:
                        await cog.send_alert(site=key, ip_address=ip, status=1)
            elif noPingCount == 3:
                print(f"{key} at {ip} is unreachable! Adding to unreachable list")
                # ADDED THESE TWO NEW LINES
                unreachable.append(ip)
                #cog = bot.get_cog("MonitorCog")
                if cog:
                    await cog.send_alert(site=key, ip_address=ip, status=0)
                print(f"{key}")
            else:
                pingMilliseconds = secToMillisec(float(pingSeconds))
                pingTimeStr = str(math.floor(pingMilliseconds * 100)/100.0)
                print(f"{key}: {pingTimeStr}ms")
        except Exception as e:
            print(f"{key}: Error occured - {e}")
    print(unreachable)

#async def pingSite(site: str):


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
