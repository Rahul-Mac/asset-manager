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
import edit_loc
import os

class edit_loc_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_loc_box, self).__init__()
        uic.loadUi(r'ui\edit_loc_box.ui', self)
        self.setWindowIcon(QtGui.QIcon(r'icon\icon.png'))
        self.setWindowTitle("Asset Manager - Location Edit")
        self.loc_update_btn.clicked.connect(self.update)
        self.loc_reset_btn.clicked.connect(self.reset)
        self.details_box.setTitle(global_variable.LOC)
        self.flr_combo.model().item(0).setEnabled(False)
        self.wing_combo.model().item(0).setEnabled(False)
        self.generate()
        self.show()

    def generate(self):
        global_variable.mycursor.execute("SELECT active, floor, wing from location where name = '"+global_variable.LOC+"'")
        data = global_variable.mycursor.fetchone()
        if data[0]:
            self.loc_active.setChecked(True)
        else:
            self.loc_active.setChecked(False)
        self.flr_combo.setCurrentText(data[1])
        self.wing_combo.setCurrentText(data[2])
    
    def update(self):
        l = global_variable.LOC
        f = self.flr_combo.currentText()
        w = self.wing_combo.currentText()
        d = str(datetime.datetime.now())
        u = global_variable.USER
        if self.loc_active.isChecked():
            a = '1'
        else:
            a = '0'
        if w == "-- Select --":
            w = ""
        try:
            if l == "" or f == "" or d == "" or u == "" or  f == "-- Select --" or a == "":
                raise Exception()
            else:
                sql = "UPDATE location set active = '"+a+"', floor = '"+f+"', wing = '"+w+"', updated_date_time = '"+d+"', updated_user_id = '"+u+"' Where name = '"+l+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data updated successfully!")
                self.close()
                
        except:
            QMessageBox.warning(self, "Warning", "Enter the details correctly")

    def reset(self):
        self.flr_combo.setCurrentText("-- Select --")
        self.wing_combo.setCurrentText("-- Select --")
        self.loc_active.setChecked(True)

    def closeEvent(self, event):
        self.ed = edit_loc.edit_loc()
        self.ed.show()
        self.close()


