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
from datetime import date
import service_box

class service(QtWidgets.QDialog):
    def __init__(self):
        super(service, self).__init__()
        uic.loadUi(r'ui\service.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Service")
        self.log.doubleClicked.connect(self.table_click)
        self.generate()
        self.search.textChanged.connect(self.get_search)
        self.show()

    def table_click(self, item):
        global_variable.ASSET = self.log.item(self.log.currentRow(), 0).text()
        self.pop = service_box.service_box()
        self.pop.show()
        self.close()

    def fetch(self, text):
        global_variable.mycursor.execute("SELECT asset_no, date_time, user_id, type, remark from asset_service where asset_no like '%"+text+"%';")
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
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
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
        global_variable.mycursor.execute("SELECT asset_no, date_time, user_id, type, remark from asset_service;")
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
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")
