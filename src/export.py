'''
This file is part of Asset Manager.

Asset Manager is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.
Hardware Service Manager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Asset Manager.
If not, see <https://www.gnu.org/licenses/>.
'''

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QFileDialog
from PyQt5.QtCore import QDateTime
import mysql.connector
import datetime
import global_variable
import os
from datetime import date, datetime
from datetime import timedelta
import pandas as pd

class export(QtWidgets.QDialog):
    def __init__(self):
        super(export, self).__init__()
        uic.loadUi(r'ui\export.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.date = date.today()
        self.time = datetime.now()
        self.setWindowTitle("Export")
        self.folder.clicked.connect(self.select_directory)
        self.exp_btn.clicked.connect(self.export)
        self.rst_btn.clicked.connect(self.reset)
        self.start.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 0, 0, 0))
        self.end.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 23, 59, 59))
        self.show()

    def list_to_excel(self, n):
        fields = ['Asset No.', 'Created By', 'Date & Time', 'Description', 'Type', 'Model', 'Status', 'Condition', 'Asset Name', 'Allocated To']
        df = pd.DataFrame(list(self.data), columns = fields)
        writer = pd.ExcelWriter(n)
        df.to_excel(writer)
        writer.save()
        QMessageBox.information(self, "Message", "File exported")
    
    def select_directory(self):
        self.folder.setText(str(QFileDialog.getExistingDirectory(self, "Select Folder")))

    def get_type(self, index, i):
        try:
            global_variable.mycursor.execute("SELECT type FROM asset_type where asset_type_id = "+str(index)+";")
            typ = global_variable.mycursor.fetchone()
            self.data[i][4] = typ[0]
        except Exception as e:
            print(e)
                
    def convert(self):
        for i in range(len(self.data)):
            self.data.insert(i, list(self.data.pop(i)))
            self.data[i][2] = str(self.data[i][2])
            self.get_type(self.data[i][4], i)

    def export(self):
        n = self.file_name.text()
        f = self.folder.text()
        s = self.start.dateTime().toPyDateTime()
        e = self.end.dateTime().toPyDateTime()
        try:
            if n == "" or f == "" or s == "" or e == "" or f == "Select Folder":
                QMessageBox.critical(self, "Error", "All the fields are compulsory")
            else:
                sql = "SELECT asset_no, created_user_id, created_date_time, description, type, model, status, cndtn, name, allocated_to FROM asset WHERE created_date_time BETWEEN '"+str(s)+"' AND '"+str(e)+"'"
                global_variable.mycursor.execute(sql)
                self.data = global_variable.mycursor.fetchall()
                self.convert()
                self.list_to_excel(f+"/"+n+".xlsx")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def reset(self):
        self.file_name.clear()
        self.folder.setText("Select Folder")
        self.start.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 0, 0, 0))
        self.end.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 23, 59, 59))
