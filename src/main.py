import asyncio
from asyncping3 import ping, verbose_ping
import json
import time
import math

'''
Dependencies needed to run this

asyncping3
anyio
'''

'''
maybe make a function that checks if the format of the ip is right? might not be needed
def validIP(textEntry: str):
    sec1 = textEntry[:3]
    sec2 = textEntry[4:7]
    sec3 = textEntry[8]
'''

#async def sitePing():

def secToMillisec(seconds: float):
    return seconds * 1000

async def pingSites(sites: dict):
    for key in sites:
        try:
            pingSeconds = await ping(sites[key])
            #print(pingSeconds)
            if pingSeconds is None:
                print(f"{sites[key]}: Unreachable!")
            else:
                pingMilliseconds = secToMillisec(float(pingSeconds))
                pingTimeStr = str(math.floor(pingMilliseconds * 100)/100.0)
                print(key, ": " + pingTimeStr + " ms")
        except Exception as e:
            print(f"{key}: Error occured - {e}")

async def main():
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

asyncio.run(main())
