################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys, socket, zmq, platform, time
from datetime import datetime
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtCore import (Qt, QSortFilterProxyModel, QSettings, QThread, Signal, QObject, QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject,  QPoint, QRect, QSize, QTime, QUrl, QEvent)
from PySide2.QtWidgets import *
from PySide2.QtSql import *
from os.path import exists


# GUI FILE
from ui_main import Ui_MainWindow

# IMPORT FUNCTIONS
from ui_functions import *

class ZeroMQ_Listener(QObject):
	finished = Signal()
	data = Signal(str, float)
	
	def __init__(self):
		QObject.__init__(self)
		context = zmq.Context()
		self.socket = context.socket(zmq.SUB)

		self.setting_ip = QSettings('GUI Database', 'IP Address')
		if self.setting_ip.value('IP_Address') != None:
			tcp_str = 'tcp://' + self.setting_ip.value('IP_Address') + ':5556'
		else:
			tcp_str = 'tcp://127.0.0.1:5556'
		print('Connecting to IP Address: ' + tcp_str)
		self.socket.connect(tcp_str)

		# Subscribe to topic
		self.socket.setsockopt(zmq.SUBSCRIBE, b'')  # subscribe to topic of all
		
		self.is_running = False
		self.is_killed = False

	def pause(self):
		self.is_running = False
		
	def resume(self):
		self.is_running = True
		
	def kill(self):
		self.is_killed = True

	def loop(self):
		while True:
			# Receive ZMQ data
			while self.is_running:
				event = self.socket.poll(timeout=1000) # Poll socket for event, wait 1 second for timeout.
				if event == 0:
					pass
				else:
					EPC, RSSI = self.socket.recv_multipart()
					EPC = EPC.decode('utf-8')
					RSSI = float(RSSI.decode('utf-8'))
					# print(EPC, RSSI)
					self.data.emit(EPC, RSSI)
			
			# Sleep when paused
			time.sleep(0.1)
			print('sleep')
			
			# Exit when killed
			if self.is_killed:
				break
		
		# self.finished.emit()

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Connect to SQL database
		self.db = QSqlDatabase.addDatabase("QSQLITE")
		self.db.setDatabaseName("projects.db")
		if not exists("projects.db"):
			self.db.open()
			print("File projects.db does not exist. Creating empty table.")
			query = QSqlQuery()
			query.exec_("""
						CREATE TABLE projects
						(EPC TEXT PRIMARY KEY, Category TEXT, Read_Count INTEGER, Last_Read_From TEXT, First_Seen TEXT, Last_Seen TEXT, Time_Since_Last_Seen DECIMAL(9,3), Last_RSSI DECIMAL(6,2), RSSI_Avg DECIMAL(6,2), RSSI_Max DECIMAL(6,2), RSSI_Min DECIMAL(6,2), Power DECIMAL(6,2), Phase_Angle DECIMAL(6,2), Doppler_Freq DECIMAL(6,2))
						""")
			query.exec_("""INSERT INTO projects VALUES 
							('912391239123912391239123', 'Classic', 0, '127.0.0.1', '2022-01-01 12:00:00.001', '2022-01-02 12:00:00.001', 2678400, -50.30, -48.8, -45.2, -54.6, 30.00, NULL, NULL)
							""")
			self.db.close()

		self.db.open()

		# Check host IP Address and set text in host_ip_label.
		self.get_hostip()

		# Setup QSqlTableModel for easy read / write access to db
		self.model = QSqlTableModel(self)
		self.model.setTable("projects")
		self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
		# self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
		self.model.select()
		self.model.setHeaderData(0, Qt.Horizontal, "EPC")
		self.model.setHeaderData(1, Qt.Horizontal, "Category")
		self.model.setHeaderData(2, Qt.Horizontal, "Read Count")
		self.model.setHeaderData(3, Qt.Horizontal, "Last Read From")
		self.model.setHeaderData(4, Qt.Horizontal, "First Seen (Y-M-D H:M:S)")
		self.model.setHeaderData(5, Qt.Horizontal, "Last Seen (Y-M-D H:M:S)")
		self.model.setHeaderData(6, Qt.Horizontal, "Time Since \nLast Seen (Sec)")
		self.model.setHeaderData(7, Qt.Horizontal, "Last RSSI")
		self.model.setHeaderData(8, Qt.Horizontal, "RSSI Avg")
		self.model.setHeaderData(9, Qt.Horizontal, "RSSI Max")
		self.model.setHeaderData(10, Qt.Horizontal, "RSSI Min")
		self.model.setHeaderData(11, Qt.Horizontal, "Power")
		self.model.setHeaderData(12, Qt.Horizontal, "Phase Angle")
		self.model.setHeaderData(13, Qt.Horizontal, "Doppler Frequency")

		# Update tableView as QSqlTableModel
		self.ui.tableView.setModel(self.model)
		self.ui.tableView.resizeColumnsToContents()
		# Set to stretch EPC column so that entire table stays in view regardless of window size
		self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

		# Setup QSortFilterProxyModel to enable search through QSqlTableModel
		self.filter_proxy_model = QSortFilterProxyModel()
		self.filter_proxy_model.setSourceModel(self.model)
		self.filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
		# setFilterKeyColumn default 0, -1 to search all columns
		self.filter_proxy_model.setFilterKeyColumn(-1)
		# Start search when text is entered into the QLineEdit search_db
		self.ui.search_db.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
		self.ui.tableView.setModel(self.filter_proxy_model)

		# Start / Stop program
		self.ui.start_stop_btn.clicked.connect(self.program_status)

		# Trigger db row removal
		self.ui.remove_row.clicked.connect(self.DeleteRow)
		
		# Retrieve Settings from QSettings
		self.getSettingsValues()
		
		# Trigger IP Address change after edit
		self.ui.lineEdit_ip.editingFinished.connect(self.Edit_IP)

		# Setup ZMQ listener workers with QThread
		self.ZMQ_Thread()

		# MOVE WINDOW
		def moveWindow(event):
			# RESTORE BEFORE MOVE
			if UIFunctions.returnStatus() == 1:
				UIFunctions.maximize_restore(self)

			# IF LEFT CLICK MOVE WINDOW
			if event.buttons() == Qt.LeftButton:
				self.move(self.pos() + event.globalPos() - self.dragPos)
				self.dragPos = event.globalPos()
				event.accept()

		# SET TITLE BAR
		self.ui.title_bar.mouseMoveEvent = moveWindow

		## ==> SET UI DEFINITIONS
		UIFunctions.uiDefinitions(self)


		## SHOW ==> MAIN WINDOW
		########################################################################
		self.show()

	## APP EVENTS
	########################################################################
	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()

	def closeEvent(self, event):
		if not self.thread.isFinished():
			self.zeromq_listener.is_running = False
			self.zeromq_listener.is_killed = True
			self.thread.quit()
			self.thread.wait()
		self.db.close()
		return super().closeEvent(event)

	def program_status(self):
		if self.ui.start_stop_btn.isChecked():
			self.ui.start_stop_btn.setStyleSheet("background-color: red")
			self.ui.start_stop_btn.setText("Stop")
			self.zeromq_listener.is_running = True
		else:
			self.ui.start_stop_btn.setStyleSheet("background-color: yellow")
			self.ui.start_stop_btn.setText("Start")
			self.zeromq_listener.is_running = False
			# self.thread.quit()
			# self.thread.wait()
			# if self.thread.isFinished():
			# 	print("Thread Status: Finished")

	def ZMQ_Thread(self):
		# Setup ZMQ listener workers with QThread
		self.thread = QThread()
		self.zeromq_listener = ZeroMQ_Listener()
		self.zeromq_listener.moveToThread(self.thread)
		
		# Connect signals and slots
		self.thread.started.connect(self.zeromq_listener.loop)
		self.zeromq_listener.data.connect(self.ZMQ_simulation) # Connect data from thread to function in main
		# self.zeromq_listener.finished.connect(self.thread.quit)
		# self.zeromq_listener.finished.connect(self.zeromq_listener.deleteLater)
		# self.thread.finished.connect(self.thread.deleteLater)

		# Start thread
		self.thread.start()

	def ZMQ_simulation(self, EPC, RSSI):
		# Append new data to table
		query = QSqlQuery()
		# EPC = '845684568456845684568456'
		# RSSI = -51.00

		# EPC TEXT PRIMARY KEY
		# Category TEXT
		# Read_Count INTEGER
		# Last_Read_From TEXT
		# First_Seen TEXT
		# Last_Seen TEXT
		# Time_Since_Last_Seen DECIMAL(9,3)
		# Last_RSSI DECIMAL(6,2)
		# RSSI_Avg DECIMAL(6,2)
		# RSSI_Max DECIMAL(6,2)
		# RSSI_Min DECIMAL(6,2)
		# Power DECIMAL(6,2)
		# Phase_Angle DECIMAL(6,2)
		# Doppler_Freq DECIMAL(6,2)
		# '912391239123912391239123', 'Classic', 0, '127.0.0.1', '2022-01-01 12:00:00.001', '2022-01-02 12:00:00.001', 2678400, -50.30, -48.8, -45.2, -54.6, 30.00, NULL, NULL

		# Using SQL UPSERT (https://www.sqlite.org/lang_UPSERT.html). Special syntax addition to INSERT that causes the INSERT to behave as an UPDATE or a no-op if the INSERT would violate a uniqueness constraint. UPSERT is not standard SQL.
		query.prepare("""INSERT INTO projects (EPC, Category, Read_Count, Last_Read_From, First_Seen, Last_Seen, Time_Since_Last_Seen, Last_RSSI, RSSI_Avg, RSSI_Max, RSSI_Min, Power, Phase_Angle, Doppler_Freq)
					VALUES(:EPC, :Category, 1, :Last_Read_From, :First_Seen, :Last_Seen, :Time_Since_Last_Seen, :Last_RSSI, :RSSI_Avg, :RSSI_Max, :RSSI_Min, :Power, :Phase_Angle, :Doppler_Freq)
					ON CONFLICT (EPC) DO
					UPDATE SET Read_Count = Read_count + 1,
					Time_Since_Last_Seen = (julianday('now') - julianday(Last_Seen)) * 86400,
					Last_Seen = strftime('%Y-%m-%d %H:%M:%f', 'now'),
					Last_Read_From = :Last_Read_From,
					Last_RSSI = :Last_RSSI,
					RSSI_Avg = (RSSI_Avg * (Read_Count - 1) + :Last_RSSI) / Read_Count,
					RSSI_Max = MAX(RSSI_Max, :Last_RSSI),
					RSSI_Min = MIN(RSSI_Min, :Last_RSSI),
					Power = :Power,
					Phase_Angle = :Phase_Angle,
					Doppler_Freq = :Doppler_Freq
					""")

		# Substitute named bindings in prepared SQL query, prepare because cannot execute directly with string literal.
		First_Seen = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # Drop last 3 digits of microseconds to match SQL precision of 3 digit milliseconds.
		query.bindValue(":EPC", EPC)
		query.bindValue(":Category", 'Class 1')
		query.bindValue(":Last_Read_From", self.ui.lineEdit_ip.text())
		query.bindValue(":First_Seen", First_Seen)
		query.bindValue(":Last_Seen", First_Seen)
		query.bindValue(":Time_Since_Last_Seen", 0.00)
		query.bindValue(":Last_RSSI", RSSI)
		query.bindValue(":RSSI_Avg", RSSI)
		query.bindValue(":RSSI_Max", RSSI)
		query.bindValue(":RSSI_Min", RSSI)
		query.bindValue(":Power", 30.00)
		query.bindValue(":Phase_Angle", None)
		query.bindValue(":Doppler_Freq", None)

		# Substitute positional bind value to ? for Last_Read_From, prepare because cannot execute directly with string literal.
		# query.addBindValue(self.ui.lineEdit_ip.text())

		query.exec_()
		self.model.select()


	def DeleteRow(self):
		self.model.removeRow(self.ui.tableView.currentIndex().row())
		self.model.select()
		# self.model.submitAll()

	def Edit_IP(self):
		error = 0

		# Set to localhost 127.0.0.1 if empty, to prevent app from not starting up if no previous IP address entered in QSettings.
		if self.ui.lineEdit_ip.text() == '':
			self.setting_ip.setValue('IP_address', '127.0.0.1')
		else:
			# check for valid IPv4 Address, check 4 sub-fields, int range 0 to 255 (8 bits).
			ip_split = self.ui.lineEdit_ip.text().split('.')
			if len(ip_split) != 4:
				error = 1
			for i in ip_split:
				if i.isdigit() and int(i) <= 255 and int(i) >= 0:
					pass
				else:
					error = 1
					break
			if error == 1:
				error_dialog = QMessageBox()
				error_dialog.setIcon(QMessageBox.Critical)
				error_dialog.setText("Invalid IPv4 Address")
				error_dialog.setInformativeText('IP Address must follow IPv4 standards, 4 sub-fields, 0-255 values')
				error_dialog.setWindowTitle("Error")
				# error_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				error_dialog.exec_()
				self.ui.lineEdit_ip.clear()
				self.setting_ip.setValue('IP_address', '127.0.0.1')
			else:
				# Set Value of QSettings 'IP_address'
				self.setting_ip.setValue('IP_address', self.ui.lineEdit_ip.text())

		# Restart thread to rebind IP Address in PyZMQ
		self.zeromq_listener.running = False
		self.thread.quit()
		self.thread.wait()
		if self.thread.isFinished():
			print("Thread Status: Finished")
		self.ZMQ_Thread()

		# self.model.select()

	def getSettingsValues(self):
		self.setting_ip = QSettings('GUI Database', 'IP Address')
		# If setup for first time, set as localhost, else load from settings
		if self.setting_ip.value('IP_Address') == '' or self.setting_ip.value('IP_Address') == None:
			self.setting_ip.setValue('IP_address', '127.0.0.1')
		elif self.setting_ip.value('IP_Address') == '127.0.0.1':
			self.ui.lineEdit_ip.clear()
		else:
			self.ui.lineEdit_ip.setText(self.setting_ip.value('IP_Address'))

		# self.setting_window = QSettings('GUI Database', 'Window Size')

	# Works on Linux, Windows, and OSX. Does NOT need routable net access or any connection at all. 
	# Works even if all interfaces are unplugged from the network. No external dependencies.
	def get_hostip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(0)
		try:
			# doesn't even have to be reachable
			s.connect(('10.255.255.255', 1))
			IP = s.getsockname()[0]
		except Exception:
			IP = '127.0.0.1'
		finally:
			s.close()
			self.ui.host_ip_label.setText('Host IP Address: ' + IP)
		return

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())
