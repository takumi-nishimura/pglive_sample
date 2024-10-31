import pickle
import queue
import socket
import sys
from threading import Thread

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget
from PyQt6.QtWidgets import QApplication


class ReplaceQueue(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)

    def put(self, item):
        if self.full():
            self.get()
        super().put(item)


### UDPでデータを受け取り，キューでプロットスレッドにデータを投げるループ
def udp_thr():
    while True:
        try:
            mes, cli_addr = sock.recvfrom(4096)
            if mes:
                mes = pickle.loads(mes)
                que.put(mes)
        except:
            pass


### キューでUDPスレッドからデータを受け取り，プロットするループ
def live_serial_plot(connector):
    while True:
        data = que.get()
        x = data["x"]
        y = data["y1"]
        if type(y) == list:
            connector.cb_append_data_array(y, x)
        else:
            connector.cb_append_data_point(y, x)


### UDPスレッドのスタート
SOCK_ADDRESS = ("127.0.0.1", 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCK_ADDRESS)
Thread(target=udp_thr, daemon=True).start()

### スレッド間（UDP，プロット）データ受け渡し用キュー
que = ReplaceQueue(maxsize=1)

### プロットスレッドのスタート
app = QApplication(sys.argv)
plot_widget = LivePlotWidget(title="Live Plot")
plot_curve = LiveLinePlot()
plot_widget.addItem(plot_curve)
data_connector = DataConnector(plot_curve, max_points=1000, update_rate=200)
plot_widget.show()
Thread(target=live_serial_plot, args=(data_connector,), daemon=True).start()
app.exec()
