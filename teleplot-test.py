import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto(
        b"Accel_X:1.23",
        ("127.0.0.1", 47269)
    )
    time.sleep(1)