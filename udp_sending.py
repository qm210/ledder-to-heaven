import asyncio
from typing import Tuple, Dict

from color import hue_to_rgb
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


def fill_rainwbow_map(result: LedMap, step: int):
    # ignore back/floor LED for this
    for i in range(170):
        result[i] = hue_to_rgb(0.05 * (i - step))


def warls_message(led_map: LedMap, timeout: int = 255) -> bytearray:
    # WARLS: [1, timeout, <LED index>, <LED R>, <LED G>, <LED B>, etc. for all LEDs]
    message = [1, timeout]
    for index, rgb in led_map.items():
        message.append(index)
        message.extend(rgb)
    return bytearray(message)


async def main():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        remote_addr=(wled_host, wled_port),
    )
    led_map = {}
    running = True
    step = 0
    while running:
        try:
            fill_rainwbow_map(led_map, step)
            message = warls_message(led_map, timeout=5)
            transport.sendto(message)
            await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            running = False
        step += 1
    transport.close()
    print("Gone.")


if __name__ == "__main__":
    asyncio.run(main())
