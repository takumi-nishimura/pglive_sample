import pickle
import socket
import time

import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK_ADDRESS = ("127.0.0.1", 9999)

CHUNK_SIZE = 50

chunk_x = []
chunk_y1 = []
chunk_y2 = []
chunk_y3 = []

x = 0
try:
    while True:
        x += 0.01

        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = y1 + y2

        if len(chunk_y1) < CHUNK_SIZE:
            chunk_x.append(x)
            chunk_y1.append(y1)
            chunk_y2.append(y2)
            chunk_y3.append(y3)

        if len(chunk_y1) == CHUNK_SIZE:
            sock.sendto(
                pickle.dumps(
                    {
                        "x": chunk_x,
                        "y1": chunk_y1,
                        "y2": chunk_y2,
                        "y3": chunk_y3,
                    }
                ),
                SOCK_ADDRESS,
            )

            chunk_x = []
            chunk_y1 = []
            chunk_y2 = []
            chunk_y3 = []

        time.sleep(1 / 200)


except KeyboardInterrupt:
    print("KeyboardInterrupt")
