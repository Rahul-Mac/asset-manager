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
import hashlib
import os

class add_user(QtWidgets.QDialog):
    def __init__(self):
        super(add_user, self).__init__()
        uic.loadUi(r'ui\add_user.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Add User")
        self.user_save_btn.clicked.connect(self.save)
        self.user_reset_btn.clicked.connect(self.reset)
        self.show()

    def save(self):
        u = self.user_name.text()
        p = self.user_pass.text()
        d = str(datetime.datetime.now())
        if self.user_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if u == "" or p == "" or a == "":
                raise Exception()
            elif len(u) < 6:
                QMessageBox().critical(self, "Error", "Username must be 6 characters long")
            elif len(p) < 6:
                QMessageBox().critical(self, "Error", "Password must be 6 characters long")
            else:
                global_variable.mycursor.execute("SELECT user_id FROM user WHERE username = '"+u+"'")
                x = global_variable.mycursor.fetchone()
                p = hashlib.md5(p.encode('utf-8')).hexdigest()
                if x is None:
                    sql = "INSERT INTO user (username, created_date_time, password, created_user_id, updated_user_id, updated_date_time, active) VALUES (%s, %s, %s, %s, %s, %s, %s)"    
                    val = (u, d, p, global_variable.USER, global_variable.USER, d, a)
                    global_variable.mycursor.execute(sql, val)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Error", "Username already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")


    def reset(self):
        self.user_name.clear()
        self.user_pass.clear()
        self.user_active.setChecked(True)
