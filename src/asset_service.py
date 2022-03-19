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
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QDate
import mysql.connector
import datetime
import global_variable
import os
from datetime import date
from datetime import timedelta

class asset_service(QtWidgets.QDialog):
    def __init__(self):
        super(asset_service, self).__init__()
        uic.loadUi(r'ui\asset_service.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Asset Service")
        self.date = date.today()
        self.type.model().item(0).setEnabled(False)
        self.save_btn.clicked.connect(self.save)
        self.box.setTitle(global_variable.ASSET)
        self.service_date.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.show()

    def save(self):
        t  = self.type.currentText()
        c = str(self.service_date.date().toPyDate())
        u = global_variable.USER
        d = str(datetime.datetime.now())
        a = global_variable.ASSET
        s = self.ser.text()
        r = self.remark.toPlainText()
        try:
            if t == "" or t == "-- Select --" or d == "" or c == "" or u == ""  or a == "" or r == "":
                QMessageBox.critical(self, "Error", "Compulsory fields cannot be empty")
            else:
                global_variable.mycursor.execute("SELECT asset_id from asset_service where asset_no = '"+a+"';")
                data = global_variable.mycursor.fetchone()
                if data is None:
                    sql = "INSERT INTO asset_service (date_time, user_id, asset_no, type, service_date, serviced_by, remark) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    val = (d, u, a, t, c, s, r)
                    global_variable.mycursor.execute(sql, val)
                    global_variable.mydb.commit()
                    global_variable.mycursor.execute("update asset set status = '"+t+"' where asset_no = '"+a+"';")
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully")
                    self.close()
                else:
                    QMessageBox.critical(self, "Error", "Asset already in service")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
