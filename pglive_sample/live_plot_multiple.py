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


def udp_thr():
    while True:
        try:
            mes, cli_addr = sock.recvfrom(4096)
            if mes:
                mes = pickle.loads(mes)
                que.put(mes)
        except:
            pass


def live_serial_plot(connector, number):
    while True:
        try:
            data = que.get(block=False)
            if number == 1:
                connector.cb_append_data_point(data["y1"], data["x"])
            elif number == 2:
                connector.cb_append_data_point(data["y2"], data["x"])
            elif number == 3:
                connector.cb_append_data_point(data["y2"]*2, data["x"])
            time.sleep(0.01)
        except:
            pass


SOCK_ADDRESS = ("127.0.0.1", 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCK_ADDRESS)
Thread(name="UDP_thread", target=udp_thr, daemon=True).start()

que = queue.Queue()

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

data_connector1 = DataConnector(plot_curve1, max_points=600, update_rate=1000)
data_connector2 = DataConnector(plot_curve2, max_points=600, update_rate=1000)
data_connector3 = DataConnector(plot_curve3, max_points=600, update_rate=1000)

Thread(
    name="plot1_thr", target=live_serial_plot, args=(data_connector1, 1), daemon=True
).start()
Thread(
    name="plot2_thr", target=live_serial_plot, args=(data_connector2, 2), daemon=True
).start()
Thread(
    name="plot3_thr", target=live_serial_plot, args=(data_connector3, 3), daemon=True
).start()

main_win.setCentralWidget(panel)
main_win.show()
app.exec()
