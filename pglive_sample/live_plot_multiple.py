import pickle
import queue
import socket
import sys
import time
from threading import Thread

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow


class ReplaceQueue(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)

    def put(self, item):
        if self.full():
            self.get()
        super().put(item)


def udp_thr():
    while True:
        mes, cli_addr = sock.recvfrom(4096)
        if mes:
            mes = pickle.loads(mes)
            que.put(mes)


def live_serial_plot(connector, key):
    while True:
        data = que.get()
        connector.cb_append_data_point(data[key], data["x"])


que = ReplaceQueue(maxsize=1)

SOCK_ADDRESS = ("127.0.0.1", 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCK_ADDRESS)
Thread(name="UDP_thread", target=udp_thr, daemon=True).start()

app = QApplication(sys.argv)
main_win = QMainWindow()
panel = QtWidgets.QWidget()
layout = QtWidgets.QGridLayout(parent=panel)
layout.setSpacing(1)

plot_widget1 = LivePlotWidget(title="Live Plot 1", background="w")
plot_curve1 = LiveLinePlot(pen="r")
plot_widget1.addItem(plot_curve1)
layout.addWidget(plot_widget1, 0, 0)

plot_widget2 = LivePlotWidget(title="Live Plot 2", background="w")
plot_curve2 = LiveLinePlot(pen="b")
plot_widget2.addItem(plot_curve2)
plot_curve3 = LiveLinePlot(pen="g")
plot_widget2.addItem(plot_curve3)
layout.addWidget(plot_widget2, 1, 0)

data_connector1 = DataConnector(plot_curve1, max_points=600, update_rate=200)
data_connector2 = DataConnector(plot_curve2, max_points=600, update_rate=200)
data_connector3 = DataConnector(plot_curve3, max_points=600, update_rate=200)

Thread(
    name="plot1_thr",
    target=live_serial_plot,
    args=(data_connector1, "y1"),
    daemon=True,
).start()
Thread(
    name="plot2_thr",
    target=live_serial_plot,
    args=(data_connector2, "y2"),
    daemon=True,
).start()
Thread(
    name="plot3_thr",
    target=live_serial_plot,
    args=(data_connector3, "y3"),
    daemon=True,
).start()

main_win.setCentralWidget(panel)
main_win.show()
app.exec()
