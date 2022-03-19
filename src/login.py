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
import global_variable
import datetime
import hashlib
import os
import window

class login(QtWidgets.QDialog):
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi(r"ui\login.ui", self)
        self.setWindowTitle("Asset Manager - Login")
        self.login_btn.clicked.connect(self.login_check)
        self.setWindowIcon(QtGui.QIcon(r"icon\icon.png"))
        self.show()
        
    def login_check(self):
        u = self.user.text()
        p = self.pswd.text()
        try:
            if u == "" or p == "":
                raise Exception()
            else:
                p = hashlib.md5(p.encode('utf-8')).hexdigest()
                global_variable.mycursor.execute("SELECT active FROM user WHERE username = '"+u+"' AND password = '"+p+"' AND active = 1;")
                global_variable.USER = u
                if(global_variable.mycursor.fetchone()[0]):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Login Successful!")
                    msg.setWindowTitle("Message")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.buttonClicked.connect(self.msgbtn)
                    msg.setWindowIcon(QtGui.QIcon('icon.ico'))
                    retval = msg.exec_()
                else:
                    raise Exception()
        except:
            QMessageBox().critical(self, "Error", "Login Failed! Try Again")

    def msgbtn(self, x):
        try:
            if x.text:
                self.w = window.window()
                self.w.show()
                self.close()
        except Exception as e:
            print(e)
