import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.sql import text
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from models_qt import MyTableModel
from AddExpense import Add_Expense
from DetailExpense import Detail_Expense
from DetailBill import Detail_Bill
from Generic_forms import GenericFormDialog
from ShowBox import Show_Box


Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Administrator_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()

    def __init__(self):
        super(Administrator_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        self.last_query = (session.query(Producto).limit(12).all())
        self.central_layout = QtGui.QGridLayout()
        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)
        self.control_singleton = False
        self.central_layout.addWidget(self.search_group, 0, 0)
        self.initialize_search_group()
        self.setLayout(self.central_layout)
        
    def initialize_search_group(self):
        self.layout_line_main = QtGui.QGridLayout()
        self.layout_line_radio = QtGui.QHBoxLayout()
        self.layout_line_search = QtGui.QHBoxLayout()
        self.layout_line_table = QtGui.QVBoxLayout()
        self.layout_line_gain = QtGui.QHBoxLayout()
        self.layout_line_expenses = QtGui.QHBoxLayout()

        self.search_bill_today = QRadioButton("Ver Facturas de Hoy")
        self.search_bill_name = QRadioButton("Buscar Factura por Nombre")
        self.search_bill_day = QRadioButton("Buscar Factura por Dia")
        self.edit_search = QtGui.QLineEdit(self)
        self.edit_date = QDateEdit(datetime.now())
        self.edit_date.setCalendarPopup(True)
        self.edit_date.setMaximumWidth(self.screenGeometry.width() / 8)
        self.edit_date.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_search_name = QtGui.QLineEdit(self)
        self.edit_search_name.hide()
        self.edit_date.hide()

        self.search_bill_today.setChecked(True)

        self.search_bill_today.toggled.connect(self.add_searcher)
        self.search_bill_day.toggled.connect(self.add_date_searcher)
        self.search_bill_name.toggled.connect(self.add_searcher_name)

        self.day_gain = QtGui.QLabel("Ganancia del Dia ", self)
        self.day_expenses = QtGui.QLabel("Gastos del Dia ", self)
        self.edit_day_gain = QtGui.QLineEdit(self)
        self.edit_day_gain.setDisabled(True)
        self.edit_day_expenses = QtGui.QLineEdit(self)
        self.edit_day_expenses.setDisabled(True)
        
        self.button_add_table = QtGui.QPushButton('Ver Detalle de Factura')
        self.button_add_table.clicked.connect(self.view_detail_product)

        self.button_add_expense = QtGui.QPushButton("Agregar Gasto", self)
        self.button_add_expense.clicked.connect(self.add_expense)

        self.button_detail_expense = QtGui.QPushButton("Detalles de Gastos", self)
        self.button_detail_expense.clicked.connect(self.detail_expense)

        self.button_close_box = QtGui.QPushButton("Cerrar Caja de Hoy", self)
        self.button_close_box.clicked.connect(self.close_box)

        self.button_show_box = QtGui.QPushButton("Ver Caja del Dia", self)
        self.button_show_box.clicked.connect(self.show_box)
        self.button_show_box.hide()
        
        header_names = ['ID', 'Factura', 'Fecha']
        self.tablemodel = MyTableModel(Factura, header_names, self)
        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.tablemodel)
        self.tableview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for row in xrange(self.tablemodel.rowCount()):
            self.tableview.openPersistentEditor(self.tablemodel.index(row, 3))

        self.layout_line_radio.addWidget(self.search_bill_today)
        self.layout_line_radio.addWidget(self.search_bill_day)
        self.layout_line_radio.addWidget(self.search_bill_name)
        self.layout_line_search.addWidget(self.edit_search)
        self.layout_line_search.addWidget(self.edit_date)
        self.layout_line_search.addWidget(self.edit_search_name)
        self.layout_line_gain.addWidget(self.day_gain)
        self.layout_line_gain.addWidget(self.edit_day_gain)
        self.layout_line_expenses.addWidget(self.day_expenses)
        self.layout_line_expenses.addWidget(self.edit_day_expenses)
        self.layout_line_expenses.addWidget(self.button_add_expense)
        self.layout_line_expenses.addWidget(self.button_detail_expense)
        self.layout_line_table.addWidget(self.tableview)
        self.layout_line_main.addLayout(self.layout_line_radio, 1, 1)
        self.layout_line_main.addLayout(self.layout_line_search, 2, 1)
        self.layout_line_main.addLayout(self.layout_line_table, 3, 1)
        self.layout_line_main.addWidget(self.button_add_table, 4, 1)
        self.layout_line_main.addLayout(self.layout_line_gain, 5, 1)
        self.layout_line_main.addLayout(self.layout_line_expenses, 6, 1)
        self.layout_line_main.addWidget(self.button_close_box, 7, 1)
        self.layout_line_main.addWidget(self.button_show_box, 7, 1)

        self.refresh_box_today()
        self.search_group.setLayout(self.layout_line_main)
        self.edit_search.textChanged.connect(self.on_search_table_edit_changed)
        self.edit_search_name.textChanged.connect(self.on_search_table_by_name_changed)
        self.edit_date.dateChanged.connect(self.on_search_table_by_date_changed)

    def refresh_box_today(self):
        self.day = '%' + str(date.today()) + '%'

        self.query_expenses = (session.query(func.sum(Gasto.monto))
                                .filter(Gasto.fecha.like(self.day)).scalar())

        self.query_gain = (session.query(Detalle, func.sum(Detalle.precio_total))
                            .join(Factura).\
                            filter(Factura.fecha.like(self.day)).first())

        if(self.query_expenses is None):
            self.edit_day_expenses.setText("0.00")
        else:
            self.edit_day_expenses.setText(str(self.query_expenses))

        if(self.query_gain[1] is None):
            self.edit_day_gain.setText('0.00')
        else:
            self.edit_day_gain.setText(str(self.query_gain[1]))
        

    def refresh_box_day(self):
        string = self.edit_date.date()
        self.day = '%'+unicode(string.toString("yyyy-MM-dd").toUtf8(), encoding="UTF-8")+'%'

        #SELECT sum(Detalle.precio_total) FROM Detalle INNER JOIN Factura On Factura.id=Detalle.factura where Factura.fecha LIKE '%2016-08-12%'

        self.query_gain = (session.query(Detalle, func.sum(Detalle.precio_total))
                            .join(Factura).\
                            filter(Factura.fecha.like(self.day)).first())
        self.query_expenses = (session.query(func.sum(Gasto.monto))
                                .filter(Gasto.fecha.like(self.day)).scalar())

        if(self.query_expenses is None):
            self.edit_day_expenses.setText("0.00")
        else:
            self.edit_day_expenses.setText(str(self.query_expenses))

        if(self.query_gain[1] is None):
            self.edit_day_gain.setText('0.00')
        else:
            self.edit_day_gain.setText(str(self.query_gain[1]))
        

    def on_search_table_edit_changed(self, string):
        if self.search_bill_today.isChecked():
            self.tablemodel.searchBillToday(string)

    def on_search_table_by_name_changed(self, string):
        if self.search_bill_name.isChecked():
            self.tablemodel.setFilter('id', string)

    def on_search_table_by_date_changed(self, string):
        if self.search_bill_day.isChecked():
            string = string.toString("yyyy-MM-dd")
            self.tablemodel.searchBillDay(string)
            self.refresh_box_day()
        
    def add_searcher(self):
        self.edit_date.hide()
        self.edit_search_name.hide()
        self.edit_search.show()
        self.button_close_box.show()
        self.button_show_box.hide()
        self.button_add_expense.show()
        self.button_detail_expense.show()
        self.edit_day_gain.show()
        self.edit_day_expenses.show()
        self.day_expenses.show()
        self.day_gain.show()
        self.refresh_box_today()

    def add_date_searcher(self):
        self.edit_search.hide()
        self.edit_search_name.hide()
        self.edit_date.show()
        self.button_close_box.hide()
        self.button_show_box.show()
        self.button_add_expense.hide()
        self.button_detail_expense.show()
        self.edit_day_gain.show()
        self.edit_day_expenses.show()
        self.day_expenses.show()
        self.day_gain.show()

    def add_searcher_name(self):
        self.edit_date.hide()
        self.edit_search_name.show()
        self.edit_search.hide()
        self.button_close_box.hide()
        self.button_show_box.hide()
        self.button_add_expense.hide()
        self.button_detail_expense.hide()
        self.edit_day_gain.hide()
        self.edit_day_expenses.hide()
        self.day_expenses.hide()
        self.day_gain.hide()

    def add_expense(self):
        window, data = GenericFormDialog.get_data(Gasto, self)
        
    def detail_expense(self):
        if self.search_bill_today.isChecked():
            today = str(date.today())
            Detail_Expense(False,today).exec_()
        if self.search_bill_day.isChecked():
            string = self.edit_date.date()
            Detail_Expense(True,string).exec_()

    def view_detail_product(self):
        try:
            indexes = self.tableview.selectedIndexes()
            for index in indexes:
                product_id = self.tablemodel.get_id_object_alchemy(index.row())
            Detail_Bill(product_id, self).exec_()
        except:
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Por favor seleccione una fila')
            msgBox.addButton(QtGui.QPushButton('Aceptar'), QtGui.QMessageBox.YesRole)
            msgBox.setWindowTitle("No Selecciono una fila")
            msgBox.exec_()

    def close_box(self):
        ok = QtGui.QMessageBox.question(self, u'Cerrar Caja',
                                            "Solo podra cerrar Caja una sola vez, desea cerrar la Caja de hoy?",
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if ok == QtGui.QMessageBox.Yes:
            self.refresh_box_today()
            self.last_query = (session.query(Caja)
                                .order_by(desc(Caja.id)).all())
            previous_balance = self.last_query[0].saldo_actual
            gains = self.edit_day_gain.text()
            expenses = self.edit_day_expenses.text()
            current_balance = float(previous_balance) + float(gains) - float(expenses)
            today = date.today()
            session.add(Caja(previous_balance,gains,expenses,current_balance,today))
            session.commit()
        else:
            return

    def show_box(self):
        string = self.edit_date.date()
        Show_Box(string ,self).exec_()