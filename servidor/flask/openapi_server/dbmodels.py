from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Client(Base):
    __tablename__ = 'client'
    name = Column(String, nullable=False)
    email = Column(String, unique=True, primary_key=True)
    password = Column(String, nullable=False)
    purchase = relationship("Purchase", back_populates="client")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return '<User %r>' % (self.name)


class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, unique=True, primary_key=True)
    client_email = Column(String, ForeignKey('client.email'), nullable=False,)
    cart = Column(Integer, nullable=True, unique=True)
    vest_type = Column(String, nullable=False)
    client = relationship("Client", back_populates="purchase")
    item = relationship("ItemPurchase")

    def __init__(self, client, cart, vest_type):
        self.client = client
        self.cart = cart
        self.vest_type = vest_type


class Item(Base):
    __tablename__ = 'item'
    rfid_code = Column(Integer, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, rfid_code, name, weight, price):
        self.rfid_code = rfid_code
        self.name = name
        self.weight = weight
        self.price = price

class ItemPurchase(Base):
    __tablename__ = "itempurchase"
    item_rfid_code = Column(Integer, ForeignKey('item.rfid_code'), nullable=False, primary_key=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False)

