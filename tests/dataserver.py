import pickle
import socket
import time

import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK_ADDRESS = ("127.0.0.1", 9999)

x = 0
while True:
    try:
        x += 0.01
        y1 = np.sin(x)
        y2 = np.cos(x)
        sock.sendto(pickle.dumps({"x": x, "y1": y1, "y2": y2}), SOCK_ADDRESS)
        time.sleep(1 / 200)
    except KeyboardInterrupt:
        break
