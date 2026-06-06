"""
Pydantic schemas for response serialization and validation.
"""

from __future__ import annotations
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field


# ── Menu / Category ──────────────────────────────────────────────────────────

class MenuItemSchema(BaseModel):
    item_id:   int
    item_name: str
    cat_id:    int
    menu_id:   int
    sizes:     Optional[str] = None
    prices:    str

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    cat_id:        int
    category_name: str
    menu_id:       int

    class Config:
        from_attributes = True


# ── Order Lines ──────────────────────────────────────────────────────────────

class OrderLineSchema(BaseModel):
    id:           int
    item_id:      int
    item_name:    str
    category:     str
    size:         Optional[str] = None
    unit_price:   float = Field(..., description="Price per unit")
    qty:          int
    line_total:   float = Field(..., description="unit_price × qty")
    order_status: str


# ── Payment ──────────────────────────────────────────────────────────────────

class PaymentSchema(BaseModel):
    payment_id:     int
    payment_date:   date
    amount_due:     float
    tips:           float
    discount:       float
    total_paid:     float
    payment_type:   str
    payment_status: str


# ── Full Order Detail ─────────────────────────────────────────────────────────

class OrderDetailSchema(BaseModel):
    order_id:      int
    order_date:    date
    items:         List[OrderLineSchema]
    items_total:   float = Field(..., description="Sum of all line totals")
    payments:      List[PaymentSchema]
    amount_due:    float = Field(..., description="Total amount due (from payment records)")
    total_paid:    float = Field(..., description="Sum of all payments made")
    balance:       float = Field(..., description="amount_due − total_paid (negative = overpaid)")
    total_tips:    float
    total_discount: float
    payment_status: str  = Field(..., description="Completed / Partial / Refunded / Pending")


# ── Paginated Response ────────────────────────────────────────────────────────

class PaginatedOrdersResponse(BaseModel):
    page:        int
    page_size:   int
    total_orders: int
    total_pages: int
    orders:      List[OrderDetailSchema]
