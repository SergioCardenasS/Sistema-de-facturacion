#!/usr/bin/env python
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

'''
client = Cliente('user1', 'apellido', 'av alto', date(1995,4,12), 986141682)
print(client.id_cliente, client.nombre)
session.add(client)
session.commit()

qr = session.query(Cliente).filter(Cliente.id_cliente == 2)
for column in qr:
	print column.id_cliente


factura = Factura(7,1,datetime.utcnow())
session.add(factura)
session.commit()


print 'Factura'
qr = session.query(Factura).filter(Factura.id_cliente ==7)
print qr 
'''

''' Agregando clientes ''' 

session.add(Cliente('cliente1', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente2', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente3', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente4', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente5', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente6', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente7', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.add(Cliente('cliente8', 'apellido', 'av alto', date(1995,4,12), 986141682))
session.commit()


''' Agregando Categorias ''' 

session.add(Categoria('Categoria1','Categoria de tipo1'))
session.add(Categoria('Categoria2','Categoria de tipo2'))
session.add(Categoria('Categoria3','Categoria de tipo3'))
session.add(Categoria('Categoria4','Categoria de tipo4'))
session.add(Categoria('Categoria5','Categoria de tipo5'))
session.commit()

''' Agregando Productos '''


session.add(Producto('1', 'Producto1', 10.00, 11.00, 5, 'Producto numero 1'))
session.add(Producto('1', 'Producto2', 10.00, 11.00, 5, 'Producto numero 2'))
session.add(Producto('2', 'Producto3', 10.00, 11.00, 5, 'Producto numero 3'))
session.add(Producto('2', 'Producto4', 10.00, 11.00, 5, 'Producto numero 4'))
session.add(Producto('3', 'Producto5', 10.00, 11.00, 5, 'Producto numero 5'))
session.add(Producto('3', 'Producto6', 10.00, 11.00, 5, 'Producto numero 6'))
session.add(Producto('4', 'Producto7', 10.00, 11.00, 5, 'Producto numero 7'))
session.add(Producto('4', 'Producto8', 10.00, 11.00, 5, 'Producto numero 8'))
session.add(Producto('5', 'Producto9', 10.00, 11.00, 5, 'Producto numero 9'))
session.add(Producto('5', 'Producto10', 10.00, 11.00, 5, 'Producto numero 10'))
session.commit()

''' Agregando Facturas '''

session.add(Factura(1,datetime.utcnow()))
session.add(Factura(2,datetime.utcnow()))
session.add(Factura(3,datetime.utcnow()))
session.add(Factura(4,datetime.utcnow()))
session.add(Factura(5,datetime.utcnow()))
session.add(Factura(6,datetime.utcnow()))
session.add(Factura(7,datetime.utcnow()))
session.add(Factura(8,datetime.utcnow()))
session.commit()

''' Agregando detalles '''
session.add(Detalle(1,1,11.00,111.00))
session.add(Detalle(1,2,11.00,111.00))
session.add(Detalle(1,3,11.00,111.00))
session.add(Detalle(1,4,11.00,111.00))
session.add(Detalle(1,5,11.00,111.00))
session.add(Detalle(2,2,11.00,111.00))
session.add(Detalle(2,3,11.00,111.00))
session.add(Detalle(2,4,11.00,111.00))
session.add(Detalle(2,5,11.00,111.00))
session.add(Detalle(2,6,11.00,111.00))
session.add(Detalle(2,7,11.00,111.00))
session.add(Detalle(3,1,11.00,111.00))
session.add(Detalle(3,6,11.00,111.00))
session.add(Detalle(4,7,11.00,111.00))
session.add(Detalle(5,4,11.00,111.00))
session.add(Detalle(5,5,11.00,111.00))
session.commit()



'''Agregando gastos'''
session.add(Gasto('Gasto1',11.00,date(2016,4,1)))
session.add(Gasto('Gasto2',12.00,date(2016,4,2)))
session.add(Gasto('Gasto3',13.00,date(2016,4,3)))
session.add(Gasto('Gasto4',14.00,date(2016,4,4)))
session.add(Gasto('Gasto5',15.00,date(2016,4,4)))
session.add(Gasto('Gasto6',16.00,date(2016,4,5)))
session.add(Gasto('Gasto7',17.00,date(2016,4,5)))
session.add(Gasto('Gasto8',18.00,date(2016,4,6)))
session.commit()


'''Agregando Caja'''

session.add(Caja(11.00,100.00,50.00,50.00,date(2016,4,1)))
session.add(Caja(11.00,110.00,50.00,60.00,date(2016,4,2)))
session.add(Caja(11.00,120.00,50.00,70.00,date(2016,4,3)))
session.add(Caja(11.00,130.00,50.00,80.00,date(2016,4,4)))
session.add(Caja(11.00,140.00,50.00,90.00,date(2016,4,5)))
session.add(Caja(11.00,150.00,50.00,100.00,date(2016,4,6)))
session.commit()