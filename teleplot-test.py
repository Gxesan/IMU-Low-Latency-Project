import socket
import math
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

t = 0

while True:
    value = math.sin(t)

    sock.sendto(
        f"Sine:{value}".encode(),
        ("127.0.0.1", 47269)
    )

    t += 0.1
    time.sleep(0.05)