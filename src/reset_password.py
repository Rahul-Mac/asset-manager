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
import hashlib
import datetime
import os

class reset_password(QtWidgets.QDialog):
    def __init__(self):
        super(reset_password, self).__init__()
        uic.loadUi(r'ui\reset_password.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Reset Password")
        self.save_btn.clicked.connect(self.save)
        self.user_id.model().item(0).setEnabled(False)
        self.get_users()
        self.show()

    def get_users(self):
        global_variable.mycursor.execute("SELECT username FROM user;")
        data = global_variable.mycursor.fetchall()
        for d in data:
            self.user_id.addItem(d[0])

    def save(self):
        u = self.user_id.currentText()
        p = self.pswd.text()
        c = self.confirm.text()
        d = str(datetime.datetime.now())
        try:
            if p != c:
                QMessageBox.critical(self, "Error", "Passwords do not match")
            elif u == "" or p == "" or c == "" or d == "" or u == "-- Select --":
                QMessageBox.critical(self, "Error", "Empty field(s) detected")
            elif len(p) < 6:
                QMessageBox.critical(self, "Error", "Password must be 6 characters long")
            else:
                p = hashlib.md5(p.encode('utf-8')).hexdigest()
                sql = "UPDATE user set password = '"+p+"', updated_date_time = '"+d+"', updated_user_id = '"+global_variable.USER+"' Where username = '"+u+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Password changed successfully!")
                self.close()
        except:
            QMessageBox.critical(self, "Error", "Failed to reset password")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = reset_password()
    app.exec_()
