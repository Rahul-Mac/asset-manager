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
import mysql.connector
import datetime
import global_variable
import os

class add_asset_type(QtWidgets.QDialog):
    def __init__(self):
        super(add_asset_type, self).__init__()
        uic.loadUi(r'ui\add_asset_type.ui', self)
        self.setWindowTitle("Asset Manager - Add Asset Type")
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.brd_reset_btn.clicked.connect(self.reset)
        self.brd_save_btn.clicked.connect(self.save)
        self.show()

    def reset(self):
        self.brd_entry.clear()
        self.active.setChecked(True)

    def save(self):
        u = global_variable.USER
        if self.active.isChecked():
            a = '1'
        else:
            a = '0'
        b = self.brd_entry.text()
        d = str(datetime.datetime.now())
        try:
            if u == "" or b == "" or d == "":
                raise Exception()
            else:
                global_variable.mycursor.execute("SELECT asset_type_id FROM asset_type WHERE type = '"+b+"'")
                x = global_variable.mycursor.fetchone()
                if x is None:
                    sql = "INSERT INTO asset_type (type, active, created_date_time, created_user_id, updated_user_id, updated_date_time) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (b, a, d, u, u, d)
                    global_variable.mycursor.execute(sql, val)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()

                else:
                    QMessageBox.critical(self, "Error", "Asset Type already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")

