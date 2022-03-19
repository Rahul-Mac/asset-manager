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

class edit_asset_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_asset_box, self).__init__()
        uic.loadUi(r'ui\edit_asset_box.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Asset Edit")
        self.box.setTitle(global_variable.AST)
        self.status.model().item(0).setEnabled(False)
        self.cndtn.model().item(0).setEnabled(False)
        self.update_btn.clicked.connect(self.update)
        self.reset_btn.clicked.connect(self.reset)
        global_variable.mycursor.execute("select complete from asset_service where asset_no = '"+global_variable.AST+"'")
        data = global_variable.mycursor.fetchone()
        if data is None:
            pass
        elif (data[0]) == 0:
            self.status.setEnabled(False)
        else:
            pass
        self.generate()
        self.show()

    def generate(self):
        global_variable.mycursor.execute("SELECT status, cndtn, description, model from asset where asset_no = '"+global_variable.AST+"'")
        data = global_variable.mycursor.fetchone()
        self.status.setCurrentText(data[0])
        self.cndtn.setCurrentText(data[1])
        self.desc.setText(data[2])
        self.model.setText(data[3])
    
    def update(self):
        s = self.status.currentText()
        c = self.cndtn.currentText()
        x = self.desc.text()
        m = self.model.text()
        d = str(datetime.datetime.now())
        u = global_variable.USER
        try:
            if s == "" or s == "-- Select --" or c == "-- Select --" or  c == "" or x == "" or m == "" or d == "" or u == "": 
                 QMessageBox.critical(self, "Error", "All fields are compulsory")
            else:
                sql = "UPDATE asset set status = '"+s+"', cndtn = '"+c+"', description = '"+x+"', model = '"+m+"', updated_date_time = '"+d+"', updated_user_id = '"+u+"' Where  asset_no = '"+global_variable.AST+"';"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data updated successfully!")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def reset(self):
        self.status.setCurrentText("-- Select --")
        self.cndtn.setCurrentText("-- Select --")
        self.desc.clear()
        self.model.clear()
