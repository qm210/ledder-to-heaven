import asyncio
from typing import Tuple, Dict

from mapping import generate_mapping

LedMap = Dict[int, Tuple[int, int, int]]


wled_host = '172.16.13.84'
# ports 21234 and 65506 should be configured to work
wled_port = 21234


def fill_sample_map(result: LedMap):
    base_color = (100, 30, 160)
    logo_color = (191, 99, 45)
    for i in range(64):
        result[i] = base_color
    for i in range(106):
        result[i+64] = logo_color
    # back and floor LEDs have only white, message still needs 3 RGB values
    result[170] = (50, 50, 50)
    result[171] = (210, 210, 210)


debugged = False

def warls_message(led_map: LedMap, timeout: int = 255) -> bytearray:
    global debugged
    # WARLS: [1, timeout, <LED index>, <LED R>, <LED G>, <LED B>, etc. for all LEDs]
    message = [1, timeout]
    for index, rgb in led_map.items():
        message.append(index)
        message.extend(rgb)
    if not debugged:
        print("[DEBUG] Message", message)
        debugged = True
    return bytearray(message)


async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        remote_addr=(wled_host, wled_port),
    )
    led_map = {}
    running = True
    while running:
        try:
            fill_sample_map(led_map)
            message = warls_message(led_map, timeout=5)
            transport.sendto(message)
            await asyncio.sleep(1.)
        except KeyboardInterrupt:
            break
        running = False
    transport.close()
    print("Closed.")


if __name__ == "__main__":
    asyncio.run(main())
