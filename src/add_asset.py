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

class add_asset(QtWidgets.QDialog):
    def __init__(self):
        super(add_asset, self).__init__()
        uic.loadUi(r'ui\add_asset.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Add Asset")
        self.date = date.today()
        self.ast_typ.model().item(0).setEnabled(False)
        self.loc.model().item(0).setEnabled(False)
        self.status.model().item(0).setEnabled(False)
        self.cndtn.model().item(0).setEnabled(False)
        self.save_btn.clicked.connect(self.save)
        self.reset_btn.clicked.connect(self.reset)
        self.get_location_types()
        self.get_asset_types()
        self.generate_asset_no()
        self.wrnty.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.purdate.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.instdate.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.show()

    def generate_asset_no(self):
        yesterday = (date.today() - timedelta(days = 1)).year
        today = date.today().year            
        try:
            global_variable.mycursor.execute("SELECT count(asset_id) FROM asset;")
            x = global_variable.mycursor.fetchall()
            cnt = x[0][0]
            if cnt == 0 or yesterday == today:
                self.asset_no.setTitle("AST-"+str(today)+"-"+str(cnt))
            else:
                self.asset_no.setTitle("AST-"+str(today)+"-"+str(0))
        except Exception as e:
            print(e)

    def get_location_types(self):
        global_variable.mycursor.execute("SELECT location_id, name FROM location where active = 1;")
        self.locations = global_variable.mycursor.fetchall()
        for loc in self.locations:
            self.loc.addItem(loc[1])

    def get_asset_types(self):
        global_variable.mycursor.execute("SELECT asset_type_id, type FROM asset_type where active = 1;")
        self.asset_types = global_variable.mycursor.fetchall()
        for ast in self.asset_types:
            self.ast_typ.addItem(ast[1])
            
    def save(self):
        try:
            name = self.name.text()
            u = global_variable.USER
            d = str(datetime.datetime.now())
            asset_no = self.asset_no.title()
            description = self.desc.text()
            asset_type = self.ast_typ.currentText()
            for ast in self.asset_types:
                if asset_type == ast[1]:
                    asset_type = ast[0]
            location = self.loc.currentText()
            for loc in self.locations:
                if location == loc[1]:
                    location = loc[0]
            manufacturer = self.man.text()
            brand = self.brd.text()
            model = self.model.text()
            serial_no = self.srno.text()
            status = self.status.currentText()
            condition = self.cndtn.currentText()
            pono = self.pono.text()
            vendor = self.vendor.text()
            warranty_expire = str(self.wrnty.date().toPyDate())
            purchase_date = str(self.purdate.date().toPyDate())
            install_date = str(self.instdate.date().toPyDate())
            allocated = self.alloc.text()
        
            if asset_no == "" or description == "" or asset_type == "" or asset_type == "-- Select --" or location == "" or location == "-- Select --" or manufacturer == "" or brand == "" or brand == "-- Select --" or model == "" \
            or serial_no == "" or status == "" or status == "-- Select --" or condition == "" or condition == "-- Select --" or purchase_date == "" or install_date == "" or warranty_expire == "" or allocated == "" or name == "":
                QMessageBox.critical(self, "Error", "Compulsory fields cannot be empty")
            else:
                sql = "INSERT INTO asset (name, allocated_to, created_date_time, updated_date_time, created_user_id, updated_user_id, asset_no,\
                description, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, warranty) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (name, allocated, d, d, u, u, asset_no, description, asset_type, location, manufacturer, brand, model, serial_no, status, condition, pono, vendor, purchase_date, install_date, warranty_expire)
                global_variable.mycursor.execute(sql, val)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data registered successfully")
                self.reset()
                self.generate_asset_no()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def reset(self):
        self.desc.clear()
        self.ast_typ.setCurrentText("-- Select --")
        self.loc.setCurrentText("-- Select --")
        self.man.clear()
        self.brd.clear()
        self.model.clear()
        self.srno.clear()
        self.status.setCurrentText("-- Select --")
        self.cndtn.setCurrentText("-- Select --")
        self.pono.clear()
        self.vendor.clear()
        self.alloc.clear()
        self.name.clear()
        self.wrnty.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.purdate.setDate(QDate(self.date.year, self.date.month, self.date.day))
        self.instdate.setDate(QDate(self.date.year, self.date.month, self.date.day))

