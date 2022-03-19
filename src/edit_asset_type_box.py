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
import edit_asset_type
import os

class edit_asset_type_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_asset_type_box, self).__init__()
        uic.loadUi(r'ui\edit_asset_type_box.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Asset Type Edit")
        self.brd_update_btn.clicked.connect(self.update)
        self.brd_reset_btn.clicked.connect(self.reset)
        self.generate()
        self.show()

    def generate(self):
        global_variable.mycursor.execute("SELECT active, asset_type_id from asset_type where type = '"+global_variable.AST+"'")
        data = global_variable.mycursor.fetchone()
        if data[0]:
            self.active.setChecked(True)
        else:
            self.active.setChecked(False)
        self.brd_entry.setText(global_variable.AST)
        self.ids = data[1]
    
    def update(self):
        b = self.brd_entry.text()
        if self.active.isChecked():
            a = '1'
        else:
            a = '0'
        d = str(datetime.datetime.now())
        u = global_variable.USER
        try:
            if b == "" or d == "" or u == "" or  a == "": 
                raise Exception()
            else:
                global_variable.mycursor.execute("SELECT type FROM asset_type WHERE asset_type_id = "+str(self.ids))
                x = global_variable.mycursor.fetchone()
                global_variable.mycursor.execute("SELECT asset_type_id FROM asset_type WHERE type = '"+b+"'")
                y = global_variable.mycursor.fetchone()
                if x[0] == b or y is None:
                    sql = "UPDATE asset_type set type = '"+b+"', active = '"+a+"', updated_date_time = '"+d+"', updated_user_id = '"+u+"' Where  asset_type_id = "+str(self.ids)
                    global_variable.mycursor.execute(sql)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data updated successfully!")
                    self.close()
                else:
                    QMessageBox.critical(self, "Error", "Update Failed! Asset Type already exists")
        except:
            QMessageBox.critical(self, "Error", "An error has occured while updating data. \nTry again.")

    def reset(self):
        self.brd_entry.clear()
        self.active.setChecked(True)

    def closeEvent(self, event):
        self.ed = edit_asset_type.edit_asset_type()
        self.ed.show()
        self.close()
