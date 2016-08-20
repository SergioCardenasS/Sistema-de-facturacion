import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from AddCategory import Add_Category
from Generic_forms import GenericFormDialog

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Add_New_Product(QDialog):
    def __init__(self, parent = None):
        #QDialog.__init__(self, parent)
        super(Add_New_Product, self).__init__(parent)

        self.control_singleton = False
        self.acceptButton = QPushButton("Crear Producto", self)
        self.cancelButton = QPushButton("Cancelar")
        self.newCategoryButton = QPushButton("Agregar Nueva Categoria", self)
        self.query = (session.query(Categoria.nombre).all())
        category = QLabel('Categoria')
        name = QLabel('Nombre')
        purchase_price = QLabel('Precio Compra')
        sell_price = QLabel('Precio Venta')
        stock = QLabel('Stock')
        detail = QLabel('Detalle')

        self.edit_category = QComboBox()
        #query
        for categories in range(len(self.query)):
            self.edit_category.addItems(self.query[categories])
        self.edit_name = QLineEdit()
        self.edit_purchase_price = QDoubleSpinBox(self)
        self.edit_purchase_price.setSingleStep(00.01)
        self.edit_purchase_price.setMaximum(10000.00)
        self.edit_purchase_price.setMinimum(00.00)
        #self.edit_purchase_price.setCorrectionMode(0)
        self.edit_sell_price = QDoubleSpinBox(self)
        self.edit_sell_price.setSingleStep(00.01)
        self.edit_sell_price.setMaximum(10000.00)
        self.edit_sell_price.setMinimum(00.00)
        self.edit_stock = QSpinBox(self)
        self.edit_stock.setSingleStep(1)
        self.edit_stock.setMaximum(100000)
        self.edit_detail = QTextEdit()

        grid = QGridLayout()
        grid.addWidget(category, 1, 0)
        grid.addWidget(self.edit_category, 1, 1)
        grid.addWidget(self.newCategoryButton, 1, 4)

        grid.addWidget(name, 2, 0)
        grid.addWidget(self.edit_name, 2, 1)

        grid.addWidget(purchase_price, 3, 0)
        grid.addWidget(self.edit_purchase_price, 3, 1)

        grid.addWidget(sell_price, 4, 0)
        grid.addWidget(self.edit_sell_price, 4, 1)

        grid.addWidget(stock, 5, 0)
        grid.addWidget(self.edit_stock, 5, 1)

        grid.addWidget(detail, 6, 0)
        grid.addWidget(self.edit_detail, 6, 1)

        grid.addWidget(self.acceptButton, 8, 1)
        grid.addWidget(self.cancelButton, 8, 2)

        self.setLayout(grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Agregar Producto')
        self.show()
        self.cancelButton.clicked.connect(self.close)
        self.connect(self.acceptButton, SIGNAL("clicked()"), self.create_Product)
        self.connect(self.newCategoryButton, SIGNAL("clicked()"), self.create_Category)

    def create_Product(self):
        category = str(self.edit_category.currentText())
        name = str(self.edit_name.text())
        purchase_price = self.edit_purchase_price.value()
        sell_price = self.edit_sell_price.value()
        stock = self.edit_stock.value()
        detail = unicode(self.edit_detail.toPlainText())
        #Query insert
        self.close()

    def create_Category(self):
        window, data = GenericFormDialog.get_data(Categoria, self)