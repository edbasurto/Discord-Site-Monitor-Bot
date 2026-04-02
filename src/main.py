import asyncio
from asyncping3 import ping
import json
import os
from src.bot import start_bot
import src.globalvars as globalvars

SITES_FILE = os.getenv("SITES_FILE", "sites.json")
STATUS_FILE = os.getenv("STATUS_FILE", "status.txt")

def secToMillisec(seconds: float):
    return seconds * 1000

async def pingSites(sites: dict):
    from src.bot import bot
    lines = []
    cog = bot.get_cog("MonitorCog")
    with open(STATUS_FILE, 'w') as file:
        for key, ip in sites.items():
            try:
                pingSeconds = await ping(ip)
                noPingCount = 0
                while pingSeconds is None and noPingCount < 3:
                    print(f"Ping count {noPingCount}")
                    pingSeconds = await ping(ip)
                    noPingCount += 1
                    await asyncio.sleep(0.5)
                if key in globalvars.unreachable:
                    if noPingCount == 3:
                        print(f"{ip} is currently down, skipping bot command")
                        lines.append(f"{key}: unreachable")
                        file.write(f"{key}: unreachable\n")
                    else:
                        print(f"{ip} is back up! Removing from unreachable list and sending discord message")
                        pingMilliseconds = secToMillisec(float(pingSeconds))
                        pingTimeStr = f"{pingMilliseconds:.2f}"
                        print(f"{key}: {pingTimeStr}ms")
                        lines.append(f"{key}: {pingTimeStr}ms")
                        file.write(f"{key}: {pingTimeStr}ms\n")
                        del globalvars.unreachable[key]
                        if cog:
                            await cog.send_alert(site=key, ip_address=ip, status=1)
                elif noPingCount == 3:
                    print(f"{key} at {ip} is unreachable! Adding to unreachable list")
                    globalvars.unreachable[key] = ip
                    if cog:
                        await cog.send_alert(site=key, ip_address=ip, status=0)
                    lines.append(f"{key}: unreachable")
                    file.write(f"{key}: unreachable\n")
                else:
                    pingMilliseconds = secToMillisec(float(pingSeconds))
                    pingTimeStr = f"{pingMilliseconds:.2f}"
                    print(f"{key}: {pingTimeStr}ms")
                    lines.append(f"{key}: {pingTimeStr}ms")
                    file.write(f"{key}: {pingTimeStr}ms\n")
            except Exception as e:
                print(f"{key}: Error occurred - {e}")
    globalvars.status_message = "\n".join(lines)
    return globalvars.unreachable

def get_all_addresses():
    with open(SITES_FILE) as f:
        return json.load(f)

def get_addresses():
    return globalvars.addresses

def get_unreachable_addresses():
    return globalvars.unreachable

def get_ping_status():
    return globalvars.status_message

async def ping_site(ip: str) -> float | None:
    result = await ping(ip)
    retries = 0
    while result is None and retries < 3:
        await asyncio.sleep(0.5)
        result = await ping(ip)
        retries += 1
    if result is None:
        return None
    return secToMillisec(float(result))

def add_site(name: str, ip: str):
    globalvars.addresses[name] = ip
    with open(SITES_FILE, 'w') as f:
        json.dump(globalvars.addresses, f, indent=2)

def update_site_ip(name: str, new_ip: str):
    globalvars.addresses[name] = new_ip
    globalvars.unreachable.pop(name, None)
    with open(SITES_FILE, 'w') as f:
        json.dump(globalvars.addresses, f, indent=2)

def update_site_name(old_name: str, new_name: str):
    ip = globalvars.addresses.pop(old_name)
    globalvars.addresses[new_name] = ip
    if old_name in globalvars.unreachable:
        globalvars.unreachable[new_name] = globalvars.unreachable.pop(old_name)
    with open(SITES_FILE, 'w') as f:
        json.dump(globalvars.addresses, f, indent=2)

def remove_site(name: str):
    del globalvars.addresses[name]
    globalvars.unreachable.pop(name, None)
    with open(SITES_FILE, 'w') as f:
        json.dump(globalvars.addresses, f, indent=2)

async def monitor_loop():
    globalvars.addresses = get_all_addresses()
    while True:
        await pingSites(globalvars.addresses)
        print()
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(
        start_bot(),
        monitor_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
