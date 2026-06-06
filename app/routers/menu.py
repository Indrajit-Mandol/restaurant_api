"""
Menu Router - exposes menu items and categories.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import MenuItem, Category, Menu
from app.schemas.schemas import MenuItemSchema, CategorySchema

router = APIRouter()


@router.get(
    "/menu",
    response_model=List[MenuItemSchema],
    summary="List all menu items",
    description="Returns every menu item with its category, available sizes, and price(s).",
)
def list_menu(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()


@router.get(
    "/categories",
    response_model=List[CategorySchema],
    summary="List all categories",
)
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
