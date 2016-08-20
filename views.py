from PyQt4 import QtGui
from PyQt4 import QtCore
from collections import namedtuple
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from plugins.models_qt import MyTableModel
from tab_views.SaleTab import Sale_Tab
from tab_views.FastSaleTab import Fast_Sale_Tab
from tab_views.InventoryTab import Inventory_Tab
from tab_views.AdministratorTab import Administrator_Tab

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.setMinimumSize(1000, 800)
        self.setWindowTitle("Sistema Pagos")

        central_layout = QtGui.QVBoxLayout()
        tabs = QtGui.QTabWidget(self)

        tab_sells = Sale_Tab()
        tab_rapid_sell = Fast_Sale_Tab()
        tab_invontary = Inventory_Tab()
        tab_administrator = Administrator_Tab()

        tabs.addTab(tab_sells, 'Ventas')
        tabs.addTab(tab_rapid_sell, 'Venta Rapida')
        tabs.addTab(tab_invontary, 'Inventario')
        tabs.addTab(tab_administrator, 'Administrador de Ventas')

        central_layout.addWidget(tabs)
        self.setLayout(central_layout)

    def closeEvent(self, event):
        event.ignore()
        ok = QtGui.QMessageBox.question(self, u'Salir',
                                        "Seguro?",
                                        QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
        if ok:
            event.accept()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    mw = MainWindow()
    screenGeometry = QtGui.QApplication.desktop().availableGeometry()
    mw.resize(screenGeometry.width(), screenGeometry.height())
    mw.showMaximized()
    app.exec_()
