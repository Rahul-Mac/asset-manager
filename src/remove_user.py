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
from PyQt5.QtWidgets import QMessageBox, QApplication, QTableWidgetItem
import mysql.connector
import datetime
import global_variable
import os

class remove_user(QtWidgets.QDialog):
    def __init__(self):
        super(remove_user, self).__init__()
        uic.loadUi(r'ui\remove_user.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Remove User")
        self.log.doubleClicked.connect(self.table_click)
        self.generate()
        self.search.textChanged.connect(self.get_search)
        self.show()

    def table_click(self, item):
        a = self.log.item(self.log.currentRow(), 0).text()
        u = self.log.item(self.log.currentRow(), 1).text()
        if a == "Yes":
            reply = QMessageBox.question(self, 'Message', 'Are you sure you want to disable '+u+'?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.remove(u, a)
            else:
                pass
        else:
            reply = QMessageBox.question(self, 'Message', 'Are you sure you want to enable '+u+'?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.remove(u, a)
            else:
                pass

    def remove(self, u, a):
        d = str(datetime.datetime.now())
        try:
            if u == "" or a == "" or d == "":
                raise Exception()
            else:
                if a == "Yes":
                    sql = "UPDATE user set active = 0, updated_date_time = '"+d+"', updated_user_id = '"+global_variable.USER+"' Where username = '"+u+"'"
                else:
                    sql = "UPDATE user set active = 1, updated_date_time = '"+d+"', updated_user_id = '"+global_variable.USER+"' Where username = '"+u+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                self.generate()
        except:
            QMessageBox.critical(self, "Error", "An error has occured")

    def fetch(self, text):
        global_variable.mycursor.execute("SELECT active, username from user where username like '%"+text+"%';")
        data = global_variable.mycursor.fetchall()
        self.log.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log.setRowCount(0)
            self.log.setRowCount(row)
            self.log.setColumnCount(col)
            header = self.log.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")

    def get_search(self):
        if self.search.text() == "":
            self.generate()
        else:
            self.fetch(self.search.text())

    def generate(self):
        global_variable.mycursor.execute("SELECT active, username from user;")
        data = global_variable.mycursor.fetchall()
        self.log.setRowCount(0)
        try:
            row = len(data)
            col = len(data[0])
            self.log.setRowCount(0)
            self.log.setRowCount(row)
            self.log.setColumnCount(col)
            header = self.log.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = remove_user()
    app.exec_()
