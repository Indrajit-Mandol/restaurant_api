"""
SQLAlchemy ORM models mapping to the restaurant database tables.
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Menu(Base):
    __tablename__ = "menus"

    menu_id   = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String(100), nullable=False)

    categories = relationship("Category", back_populates="menu")


class Category(Base):
    __tablename__ = "categories"

    cat_id        = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    menu_id       = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)

    menu  = relationship("Menu", back_populates="categories")
    items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"

    item_id   = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(200), nullable=False)
    cat_id    = Column(Integer, ForeignKey("categories.cat_id"), nullable=False)
    menu_id   = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    sizes     = Column(String(200), nullable=True)   # e.g. "Small, Large"
    prices    = Column(String(200), nullable=False)  # e.g. "1.50, 2.50"

    category     = relationship("Category", back_populates="items")
    order_lines  = relationship("OrderHistory", back_populates="item")


class OrderHistory(Base):
    __tablename__ = "order_history"

    id           = Column(Integer, primary_key=True, index=True)
    order_date   = Column(Date, nullable=False)
    order_id     = Column(Integer, index=True, nullable=False)
    item_id      = Column(Integer, ForeignKey("menu_items.item_id"), nullable=False)
    size         = Column(String(50), nullable=True)
    price        = Column(Float, nullable=False)
    qty          = Column(Integer, nullable=False)
    order_status = Column(String(50), nullable=False, default="Completed")
    total        = Column(Float, nullable=False)

    item = relationship("MenuItem", back_populates="order_lines")


class Payment(Base):
    __tablename__ = "payments"

    id             = Column(Integer, primary_key=True, index=True)
    payment_date   = Column(Date, nullable=False)
    payment_id     = Column(Integer, unique=True, index=True, nullable=False)
    order_id       = Column(Integer, index=True, nullable=False)
    amount_due     = Column(Float, nullable=False)
    tips           = Column(Float, default=0)
    discount       = Column(Float, default=0)
    total_paid     = Column(Float, nullable=False)
    payment_type   = Column(String(50), nullable=False)
    payment_status = Column(String(50), nullable=False, default="Completed")
