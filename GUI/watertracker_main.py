from PyQt6 import QtWidgets
from watertrackerapp import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        #self.epc_received.connect(self.handle_epc_received)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

# class Window(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
# #     def __init__(self):
# #         super().__init__()
# #         #self.pushButton.clicked.connect(self.clickHandler)
# #
# # # app = QApplication([])
# # #
# # window = Window()
# # window.show()
# # app.exec()
#
# if __name__ == "__main__":
# 	app = QApplication(sys.argv)
# 	window = Window()
# 	sys.exit(app.exec())