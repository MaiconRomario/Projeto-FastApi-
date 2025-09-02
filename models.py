from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy_utils.types import ChoiceType

#Cria a conexão com seu banco
db = create_engine("sqlite:///database.db")

#cria a base do banco de dados 
Base = declarative_base()

# Criar as classes/tabelas do banco 

#Usuario
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = bool(active)
        self.admin = bool(admin)

#pedido
class Order(Base):
    __tablename__ = 'orders'

    # ORDER_STATUS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    #     )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String) #pendente, cancelado, finalizado
    user_id = Column('user_id', ForeignKey('users.id') ) 
    price = Column('price', Float)
    #items =

    def __init__(self, user_id, status="PENDENTE", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price


#ItensPedido

class OrderItems(Base):
    __tablename__ = "OrderItems"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantity = Column('quantity', Integer)
    flavor = Column('flavor', String)
    size = Column('size', String)
    unit_price = Column('unit_price', Float)
    order = Column('order', ForeignKey('orders.id'))

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order


# executa a criação dos metadados do seu banco 
# (cria efetivamente o banco de dados )



