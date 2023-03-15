from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget
import zmq
import sys


class ZMQThread(QThread):
    
    data_received = pyqtSignal(bytes)

    def __init__(self):
        super().__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.subscribe(b"")

    def run(self):
        while True:
            data = self.socket.recv()
            self.data_received.emit(data)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 200, 100)
        self.setWindowTitle("ZMQ Socket Reader")

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 200, 50)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")
        self.label.setText("No tag present")

        self.zmq_thread = ZMQThread()
        self.zmq_thread.data_received.connect(self.update_label_zmq)
        self.zmq_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(250)

        self.last_updated = QDateTime.currentDateTime()

        self.center_window()
        self.center_label()
        

    def center_window(self):
        screen_geo = QDesktopWidget().screenGeometry()
        window_geo = self.geometry()
        x = (screen_geo.width() - window_geo.width()) // 2
        y = (screen_geo.height() - window_geo.height()) // 2
        self.move(x, y)

    def center_label(self):
        label_geo = self.label.geometry()
        window_geo = self.geometry()
        x = (window_geo.width() - label_geo.width()) // 2
        y = (window_geo.height() - label_geo.height()) // 2
        self.label.move(x, y)

    def update_label_zmq(self, data):
        if data and data == b'\x01':
            self.last_updated = QDateTime.currentDateTime()
            self.label.setText("Tag present")
        elif data:
            print(data)


    def update_label(self):
        elapsed_time = self.last_updated.msecsTo(QDateTime.currentDateTime())

        if elapsed_time > 500:
            self.label.setText("No tag present")


    def closeEvent(self, event):
        self.zmq_thread.quit()
        self.zmq_thread.wait()
        self.zmq_thread.deleteLater()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
