import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Add_Expense(QDialog):
    def __init__(self, parent = None):
        #QDialog.__init__(self, parent)
        super(Add_Expense, self).__init__(parent)

        self.acceptButton = QPushButton("Guardar Gasto", self)
        self.cancelButton = QPushButton("Cancelar")

        detail_expense = QLabel('Detalle de Gasto')
        mount_expense = QLabel('Monto de Gasto')
        date_expense = QLabel('Fecha')

        self.edit_detail_expense = QTextEdit()
        self.edit_mount_expense = QDoubleSpinBox(self)
        self.edit_mount_expense.setSingleStep(00.01)
        self.edit_mount_expense.setMaximum(10000.00)
        self.edit_mount_expense.setMinimum(00.00)
        self.edit_date_expense = QDateEdit(datetime.now())

        grid = QGridLayout()
        grid.addWidget(detail_expense, 1, 0)
        grid.addWidget(self.edit_detail_expense, 1, 1)
        grid.addWidget(mount_expense, 2, 0)
        grid.addWidget(self.edit_mount_expense, 2, 1)
        grid.addWidget(date_expense, 3, 0)
        grid.addWidget(self.edit_date_expense, 3, 1)
        grid.addWidget(self.acceptButton, 4, 1)
        grid.addWidget(self.cancelButton, 4, 2)

        self.setLayout(grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Agregar Gasto')
        self.show()
        self.exec_()
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
        if (self.control_singleton):
            QMessageBox.warning(self, 'Error', ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
        else:
            self.control_singleton = True
            window = Add_Category().exec_()
            self.control_singleton = False