import sys
from  datetime import date
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


class Detail_Expense(QDialog):
    def __init__(self, action, day, parent = None):
        #QDialog.__init__(self, parent)
        super(Detail_Expense, self).__init__(parent)

        self.control_singleton = False
        self.acceptButton = QPushButton("Aceptar", self)

        self.expenses_group = QtGui.QGroupBox(str("Gastos"), self)

        date_expense = QLabel('Fecha')
        self.edit_date_expense = QDateEdit(datetime.now())
        self.edit_date_expense.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_date_expense.setDisabled(1)

        if action:
            self.set_date = day
            self.edit_date_expense.setDate(self.set_date)
            self.day = '%'+unicode(day.toString("yyyy-MM-dd").toUtf8(), encoding="UTF-8")+'%'
        else:
            self.day = '%'+day+'%'

        self.initializate_expenses_group()

        grid = QGridLayout()
        grid.addWidget(date_expense, 1, 0)
        grid.addWidget(self.edit_date_expense, 1, 1)
        grid.addWidget(self.expenses_group, 2, 0, 2, 2)
        
        grid.addWidget(self.acceptButton, 4, 1)

        self.setLayout(grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Detalle de Gastos')
        self.show()
        self.acceptButton.clicked.connect(self.close)

    def initializate_expenses_group(self):
        self.layout_line = QtGui.QFormLayout()
        #Creating table
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
        self.table_items.setColumnCount(2)
        self.table_items.setHorizontalHeaderLabels(['Detalle', 'Cantidad'])

        header = self.table_items.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)

        self.query = (session.query(Gasto)
                        .filter(Gasto.fecha.like(self.day)).all())

        self.table_items.setRowCount(len(self.query))

        self.stringRow = ''
        for detail in range(len(self.query)):
            self.table_items.setItem(detail, 0,
                                     QtGui.QTableWidgetItem(str(self.query[detail].detalle)))
            self.table_items.setItem(detail, 1,
                                     QtGui.QTableWidgetItem(str(self.query[detail].monto)))
            self.stringRow = self.stringRow + str(detail+1) + ','

        self.table_items.setVerticalHeaderLabels(QString(self.stringRow).split(','))

        self.layout_line.addRow(self.table_items)
        self.expenses_group.setLayout(self.layout_line)