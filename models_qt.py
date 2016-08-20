import sys
from  datetime import date
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
import sys


Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

# class MyWindow(QWidget):
#     def __init__(self, *args):
#         QWidget.__init__(self, *args)
# 
#         header_names = ['ID', 'Categoria', 'Nombre', 'Precio Compra',
#                         'Precio Venta', 'Stock', 'Detalle']
#         self.tablemodel = MyTableModel(Producto, my_array, header_names, self)
#         self.tableview = QTableView()
#         self.tableview.setModel(self.tablemodel)
# 
#         self.proxy = QtGui.QSortFilterProxyModel(self)
#         self.proxy.setSourceModel(self.tablemodel)
#         line_edit = QtGui.QLineEdit()
#         line_edit.textChanged.connect(self.on_text_changed)
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.tableview)
#         layout.addWidget(line_edit)
#         self.setLayout(layout)
# 
#     def on_text_changed(self, text):
#         self.tablemodel.setFilter('nombre', text)


class MyTableModel(QAbstractTableModel):
    def __init__(self, model_alchemy, header_names, parent = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.model_alchemy = model_alchemy
        self.last_query = (session.query(model_alchemy).limit(20).all())
        self.arraydata = self.last_query
        self.header_names = header_names
        self.columns_name = model_alchemy.__table__.columns.keys()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_names[col])
        return QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.arraydata)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.header_names)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        row = self.arraydata[index.row()]
        return (str(getattr(row, self.columns_name[index.column()])))

    def get_id_object_alchemy(self, row):
        id_product = getattr(self.arraydata[row], self.columns_name[0])
        return id_product

    def setFilter(self, name_column, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        obj_column = getattr(self.model_alchemy, name_column)
        self.arraydata = (session.query(self.model_alchemy)
                          .filter(obj_column.like(text_query)).all())
        self.layoutChanged.emit()

    def refresh_data(self):
        self.arraydata = (session.query(self.model_alchemy).limit(20).all())
        self.layoutChanged.emit()

    def searchBillToday(self, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        today = '%'+str(date.today())+'%'
        self.arraydata = (session.query(Factura)
                        .filter(Factura.id.like(text_query)) \
                        .filter(Factura.fecha.like(today)).all())
        self.layoutChanged.emit()

    def searchBillDay(self, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        self.arraydata = (session.query(Factura)
                        .filter(Factura.fecha.like(text_query)).all())
        self.layoutChanged.emit()