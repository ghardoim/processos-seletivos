from sqlalchemy import String, Column, Integer, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

# CRIAÇÃO DOS MODELOS DAS TABELAS COM AS MESMAS CONFIGURAÇÕES DO ARQUIVO SQL PROVIDO
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(Numeric(10, 2))

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(TIMESTAMP, nullable=False)
    
    product = relationship("Product", backref="sales")
    customer = relationship("Customer", backref="sales")