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
from PyQt5.QtWidgets import QMessageBox, QApplication, QToolBar, QAction, QTableWidgetItem
from PyQt5.QtGui import QIcon, QKeySequence
import mysql.connector
import datetime
import os
import global_variable
import login
import add_loc
import edit_loc
import add_asset_type
import edit_asset_type
import add_user
import reset_password
import remove_user
import add_asset
import asset_service
import service
import edit_asset_box
import export
import logs
import manual

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        uic.loadUi(r"ui\window.ui", self)
        self.setWindowTitle("Asset Manager - "+global_variable.USER)
        self.measurement()
        self.rm_usr.setText("User\nActivation")
        self.rst_pass.setText("Change\nPassword")
        self.refresh.setText("Refresh\nTable")
        self.rm_ast.setText("Remove\nAsset(s)")
        self.restore.setText("Restore\nAsset(s)")
        self.service.setText("Add To\nService")
        self.hist.setText("Service\nHistory")
        self.connections()
        self.view_table()
        self.show()

    def get_search(self):
        if self.search.text() == "":
            self.view_table()
        else:
            try:
                if self.ast_no.isChecked() == True:
                    self.fetch(self.search.text(), "asset_no")
                if self.ast_nm.isChecked() == True:
                    self.fetch(self.search.text(), "name")
                if self.alloc.isChecked() == True:
                    self.fetch(self.search.text(), "allocated_to")
                else:
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def measurement(self):
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        height = screenRect.height()
        width = screenRect.width()
        self.ribbon.setGeometry(0, 0, width, 141)
        self.search.setGeometry(0, 150, width, 20)
        self.log_table.setGeometry(0, 240, width, height-340)
        self.setWindowIcon(QtGui.QIcon(r"icon\icon.ico"))
        self.showMaximized()

    def remove_asset(self):
        try:
            if len(self.log_table.selectedIndexes()) == 0:
                QMessageBox.critical(self, "Error", "Asset(s) not selected")
            else:
                reply = QMessageBox.question(self, 'Message', 'Are you sure you want to delete the selected asset(s)?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    rows = sorted(set(index.row() for index in self.log_table.selectedIndexes()))
                    for row in rows:
                        a = self.log_table.item(row, 0).text()
                        sql = "update asset set active = 0 where asset_no = '"+a+"' ;"
                        global_variable.mycursor.execute(sql)
                        global_variable.mydb.commit()
                    self.view_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def restore_asset(self):
        try:
            if len(self.log_table.selectedIndexes()) == 0:
                QMessageBox.critical(self, "Error", "Asset(s) not selected")
            else:
                reply = QMessageBox.question(self, 'Message', 'Are you sure you want to restore the selected asset(s)?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    rows = sorted(set(index.row() for index in self.log_table.selectedIndexes()))
                    for row in rows:
                        a = self.log_table.item(row, 0).text()
                        sql = "update asset set active = 1 where asset_no = '"+a+"' ;"
                        global_variable.mycursor.execute(sql)
                        global_variable.mydb.commit()
                    self.view_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def connections(self):
        self.log_out_btn.clicked.connect(self.log_out)
        self.loc_add.clicked.connect(self.open_add_loc)
        self.loc_edit.clicked.connect(self.open_edit_loc)
        self.asset_type_add.clicked.connect(self.open_add_asset_type)
        self.asset_type_edit.clicked.connect(self.open_edit_asset_type)
        self.user_add.clicked.connect(self.open_add_user)
        self.rst_pass.clicked.connect(self.reset_pswd)
        self.rm_usr.clicked.connect(self.open_rm_usr)
        self.asset_add.clicked.connect(self.add_ast)
        self.refresh.clicked.connect(self.view_table)
        self.rm_ast.clicked.connect(self.remove_asset)
        self.service.clicked.connect(self.add_service)
        self.search.textChanged.connect(self.get_search)
        self.asset_edit.clicked.connect(self.open_edit_asset)
        self.exp.clicked.connect(self.open_export)
        self.ext_btn.clicked.connect(self.close)
        self.log_btn.clicked.connect(self.open_service)
        self.hist.clicked.connect(self.open_log)
        self.abt.clicked.connect(self.about)
        self.lic.clicked.connect(self.lcns)
        self.restore.clicked.connect(self.restore_asset)
        self.all.toggled.connect(self.get_search)
        self.active.toggled.connect(self.get_search)
        self.inactive.toggled.connect(self.get_search)
        self.ast_no.toggled.connect(self.get_search)
        self.ast_nm.toggled.connect(self.get_search)
        self.alloc.toggled.connect(self.get_search)
        self.man.clicked.connect(self.manual)

    def manual(self):
        self.w = manual.manual()
        self.w.show()

    def about(self):
        text = "Asset Manager Version 0.1.0\nis an asset management software.\n\nCopyright (C) 2022 Rahul Mac\nunder GNU GPL v3 License"
        QMessageBox().about(self, "About Asset Manager", text)

    def lcns(self):
        text = "\t\t\tAsset Manager\n\n\n\
        Copyright (C) 2022  Rahul Mac\n\n\
        This program is free software: you can redistribute it and/or modify\n\
        it under the terms of the GNU General Public License as published by\n\
        the Free Software Foundation, either version 3 of the License, or\n\
        (at your option) any later version.\n\n\
        This program is distributed in the hope that it will be useful,\n\
        but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
        GNU General Public License for more details."
        QMessageBox().about(self, "License", text)

    def open_log(self):
        try:
            self.w = logs.logs()
            self.w.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_export(self):
        self.w = export.export()
        self.w.show()
        
    def open_edit_asset(self):
        try:
            i = self.log_table.item(self.log_table.currentRow(), 0)
            if i is not None:
                global_variable.AST = i.text()
                self.w = edit_asset_box.edit_asset_box()
                self.w.show()
            else:
                QMessageBox.critical(self, "Error", "Asset not selected")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        
    def open_service(self):
        self.w = service.service()
        self.w.show()

    def add_ast(self):
        self.w = add_asset.add_asset()
        self.w.show()

    def open_rm_usr(self):
        self.w = remove_user.remove_user()
        self.w.show()

    def open_add_user(self):
        self.w = add_user.add_user()
        self.w.show()

    def open_add_loc(self):
        self.w = add_loc.add_loc()
        self.w.show()

    def open_add_asset_type(self):
        self.w = add_asset_type.add_asset_type()
        self.w.show()

    def open_edit_asset_type(self):
        self.w = edit_asset_type.edit_asset_type()
        self.w.show()

    def open_edit_loc(self):
        self.w = edit_loc.edit_loc()
        self.w.show()

    def reset_pswd(self):
        self.w = reset_password.reset_password()
        self.w.show()

    def get_location(self, i):
        global_variable.mycursor.execute("SELECT name FROM location where location_id = "+str(i))
        x = global_variable.mycursor.fetchone()
        return(x[0])

    def get_type(self, i):
        global_variable.mycursor.execute("SELECT type FROM asset_type where asset_type_id = "+str(i))
        x = global_variable.mycursor.fetchone()
        return(x[0])

    def add_service(self):
        try:
            i = self.log_table.item(self.log_table.currentRow(), 0)
            if i is not None:
                global_variable.mycursor.execute("select asset_id from asset_service where asset_no = '"+i.text()+"' and complete = 0")
                data = global_variable.mycursor.fetchone()
                if data is None:
                    global_variable.ASSET = i.text()
                    self.w = asset_service.asset_service()
                    self.w.show()
                else:
                    QMessageBox.critical(self, "Error", "The selected asset is already in service")
            else:
                QMessageBox.critical(self, "Error", "Asset not selected")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def view_table(self):
        sql = ""
        if self.all.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset;"
        elif self.active.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset where active = 1;"
        elif self.inactive.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset where active = 0;"
        else:
            return
        global_variable.mycursor.execute(sql)
        data = global_variable.mycursor.fetchall()
        self.log_table.setRowCount(0)
        self.log_table.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log_table.setRowCount(0)
            self.log_table.setRowCount(row)
            self.log_table.setColumnCount(col)
            header = self.log_table.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeToContents)
            for r in range(row):
                for c in range(col):
                    d = data[r][c]
                    if c == 3:
                        i = QTableWidgetItem(str(self.get_type(d)))
                    elif c == 4:
                        i = QTableWidgetItem(str(self.get_location(d)))
                    elif c == 15:
                        if d == 1:
                            i = QTableWidgetItem("Yes")
                        else:
                            i = QTableWidgetItem("No")
                    else:
                        i = QTableWidgetItem(str(d))
                    #i.setFlags(QtCore.Qt.ItemIsEnabled)
                    #self.log_setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
                    self.log_table.setItem(r, c, i)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    def fetch(self, text, column):
        if '\'' in text or ';' in text:
            self.log.setRowCount(0)
            return
        sql = ""
        if self.all.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset where "+column+" like '%"+text+"%';"
        elif self.active.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset where active = 1 and "+column+" like '%"+text+"%';"
        elif self.inactive.isChecked() == True:
            sql = "SELECT asset_no, name, warranty, type, location, manufacturer, brand, model, serial_no, status, cndtn, po_no, vendor, purchase_date, install_date, active, allocated_to, description FROM asset where active = 0 and "+column+" like '%"+text+"%';"
        else:
            return
        global_variable.mycursor.execute(sql)
        data = global_variable.mycursor.fetchall()
        self.log_table.setRowCount(0)
        self.log_table.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log_table.setRowCount(0)
            self.log_table.setRowCount(row)
            self.log_table.setColumnCount(col)
            header = self.log_table.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeToContents)
            for r in range(row):
                for c in range(col):
                    d = data[r][c]
                    if c == 3:
                        i = QTableWidgetItem(str(self.get_type(d)))
                    elif c == 4:
                        i = QTableWidgetItem(str(self.get_location(d)))
                    elif c == 15:
                        if d == 1:
                            i = QTableWidgetItem("Yes")
                        else:
                            i = QTableWidgetItem("No")
                    else:
                        i = QTableWidgetItem(str(d))
                    #i.setFlags(QtCore.Qt.ItemIsEnabled)
                    #self.log_setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
                    self.log_table.setItem(r, c, i)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def log_out(self):
        try:
            self.w = login.login()
            self.w.show()
            self.close()
        except Exception as e:
            print(e)
        
