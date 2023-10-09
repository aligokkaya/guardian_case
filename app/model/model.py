from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd



SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

engine = create_engine("sqlite:///mydatabase.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DataCreate(BaseModel):
    segment: str
    country: str
    product: str
    discount_band: str
    units_sold: int
    manufacturing_price: float
    sale_price: float
    gross_sales: float
    discounts: float
    sales: float
    cogs: float
    profit: float
    date: str
    month_number: int
    month_name: str
    year: int

class DataUpdate(BaseModel):
    segment: str
    country: str
    product: str
    discount_band: str
    units_sold: int
    manufacturing_price: float
    sale_price: float
    gross_sales: float
    discounts: float
    sales: float
    cogs: float
    profit: float
    date: str
    month_number: int
    month_name: str
    year: int

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50))
    surname = Column(String(50))
    token = Column(String(500))
    data = relationship("Data", back_populates="user")
    def __repr__(self):
        return f"<User(username={self.username}, surname={self.surname}, token={self.token})>"

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    segment = Column(String(50))
    country = Column(String(50))
    product = Column(String(50))
    discount_band = Column(String(50))
    units_sold = Column(String(50))
    manufacturing_price = Column(String(50))
    sale_price = Column(String(50))
    gross_sales = Column(String(50))
    discounts = Column(String(50))
    sales = Column(String(50))
    cogs = Column(String(50))
    profit = Column(String(50))
    date = Column(String(50))
    month_number = Column(String(50))
    month_name = Column(String(50))
    year = Column(String(50))

    user = relationship("User", back_populates="data")

    def __repr__(self):
        return f"<Data(user_id={self.user_id})>"


class UserCreate(BaseModel):
    username: str
    surname: str

class Token(BaseModel):
    access_token: str
    token_type: str


Base.metadata.create_all(bind=engine)