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
import service

class service_box(QtWidgets.QDialog):
    def __init__(self):
        super(service_box, self).__init__()
        uic.loadUi(r'ui\service_box.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Asset Service")
        self.date = date.today()
        self.type.model().item(0).setEnabled(False)
        self.save_btn.clicked.connect(self.save)
        self.box.setTitle(global_variable.ASSET)
        self.service_date.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.generate()
        self.comp.clicked.connect(self.combo)
        self.show()

    def combo(self):
        if self.comp.isChecked():
            self.type.clear()
            self.type.addItem("-- Select --")
            self.type.addItem("In Use")
            self.type.addItem("In Stock")
            self.type.addItem("Beyond Repair")
            self.type.addItem("Sent To Scrap")
        else:
            self.type.clear()
            self.type.addItem("-- Select --")
            self.type.addItem("In Repair")
            self.type.addItem("Out For Repair")
            self.type.addItem("Maintenance")
        self.type.model().item(0).setEnabled(False)

    def generate(self):
        global_variable.mycursor.execute("SELECT type, service_date, serviced_by, remark, complete from asset_service where asset_no = '"+global_variable.ASSET+"'")
        data = global_variable.mycursor.fetchone()
        self.type.setCurrentText(data[0])
        try:
            self.service_date.setDate(data[1])
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        self.ser.setText(data[2])
        self.remark.setPlainText(data[3])
        if data[4]:
            self.comp.setChecked(True)
        else:
            self.comp.setChecked(False)

    def save(self):
        t  = self.type.currentText()
        c = str(self.service_date.date().toPyDate())
        u = global_variable.USER
        d = str(datetime.datetime.now())
        a = global_variable.ASSET
        s = self.ser.text()
        r = self.remark.toPlainText()
        if self.comp.isChecked():
            f = '1'
        else:
            f = '0'
        try:
            if t == "" or t == "-- Select --" or d == "" or c == "" or u == ""  or a == "" or r == "":
                QMessageBox.critical(self, "Error", "Compulsory fields cannot be empty")
            elif f == '1':
                global_variable.mycursor.execute("delete from asset_service where asset_no = '"+a+"';")
                global_variable.mydb.commit()
                global_variable.mycursor.execute("insert into logs (user_id, asset_no, type, service_date, remark, completed_date) values ('"+u+"', '"+a+"', '"+t+"', '"+c+"', '"+r+"', '"+str(date.today())+"');")
                global_variable.mydb.commit()
                global_variable.mycursor.execute("update asset set status = '"+t+"' where asset_no = '"+a+"';")
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "The servicing of '"+a+"' has been completed!")
                self.close()
            else:
                sql = "update asset_service set updated_date_time = '"+d+"', updated_user_id = '"+u+"', type = '"+t+"', service_date = '"+c+"', serviced_by = '"+s+"', remark = '"+r+"', complete = 0 where asset_no = '"+a+"';"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                global_variable.mycursor.execute("update asset set status = '"+t+"' where asset_no = '"+a+"';")
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data updated successfully")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def closeEvent(self, event):
        try:
            self.ed = service.service()
            self.ed.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
