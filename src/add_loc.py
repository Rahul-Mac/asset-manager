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

class add_loc(QtWidgets.QDialog):
    def __init__(self):
        super(add_loc, self).__init__()
        uic.loadUi(r"ui\add_loc.ui", self)
        self.setWindowTitle("Asset Manager - Add Location")
        self.setWindowIcon(QtGui.QIcon(r"icon\icon.png"))
        self.flr_combo.model().item(0).setEnabled(False)
        self.wing_combo.model().item(0).setEnabled(False)
        self.loc_reset_btn.clicked.connect(self.reset_loc)
        self.loc_save_btn.clicked.connect(self.save_loc)
        self.show()

    def save_loc(self):
        l = self.loc_entry.text()
        f = self.flr_combo.currentText()
        w = self.wing_combo.currentText()
        d = str(datetime.datetime.now())
        u = global_variable.USER
        if self.loc_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if l == "" or f == "" or d == "" or u == "" or  f == "-- Select --" or a == "":
                raise Exception()
            else:
                if w == "-- Select --":
                    w = ''
                global_variable.mycursor.execute("SELECT location_id FROM location WHERE name = '"+l+"'")
                x = global_variable.mycursor.fetchone()
                if x is None:
                    sql = "INSERT INTO location (name, floor, wing, created_date_time, created_user_id, updated_date_time, updated_user_id, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (l, f, w, d, u, d, u, a)
                    global_variable.mycursor.execute(sql, val)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset_loc()
                else:
                    QMessageBox.critical(self, "Error", "Location already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")

    def reset_loc(self):
        self.loc_entry.clear()
        self.flr_combo.setCurrentText("-- Select --")
        self.wing_combo.setCurrentText("-- Select --")
        self.loc_active.setChecked(True)
