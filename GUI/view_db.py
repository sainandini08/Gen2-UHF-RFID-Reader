from os.path import exists
from PySide6.QtWidgets import *
from PySide6.QtSql import *

import sys

if not exists("projects.db"):
    print("File projects.db does not exist. Please run initdb.py.")
    sys.exit()

app = QApplication([])
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("projects.db")
db.open()
model = QSqlTableModel(None, db)
model.setTable("projects")
model.select()
view = QTableView()
view.setModel(model)
view.show()
app.exec_()