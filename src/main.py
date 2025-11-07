import asyncio
from asyncping3 import ping, verbose_ping
import json
import time
import math
from src.bot import start_bot
from src.status import unreachable

#async def sitePing():

def secToMillisec(seconds: float):
    return seconds * 1000

async def pingSites(sites: dict):
    from src.bot import bot
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
            if key in unreachable:
                print("in the list")
            else:
                print("not in the list")
            if key in unreachable:
                if noPingCount == 3:
                    print(f"{ip} is currently down, skipping bot command")
                else:
                    print(f"{ip} is back up! Removing from unreachable list and sending discord message")
                    pingMilliseconds = secToMillisec(float(pingSeconds))
                    pingTimeStr = str(math.floor(pingMilliseconds * 100)/100.0)
                    print(f"{key}: {pingTimeStr}ms")
                    del unreachable[key]
                    if cog:
                        await cog.send_alert(site=key, ip_address=ip, status=1)
            elif noPingCount == 3:
                print(f"{key} at {ip} is unreachable! Adding to unreachable list")
                # ADDED THESE TWO NEW LINES
                unreachable[key] = ip
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
    import sys
    print("main module id in pingSites:", id(sys.modules[__name__]))
    return unreachable

#async def pingSite(site: str):
def get_unreachable_addresses():
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
