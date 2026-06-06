"""
Orders Router - provides full order details with payment information.
"""

from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from app.database import get_db
from app.models.models import OrderHistory, Payment, MenuItem, Category
from app.schemas.schemas import OrderDetailSchema, PaginatedOrdersResponse, OrderLineSchema, PaymentSchema

router = APIRouter()


def build_order_detail(order_id: int, db: Session) -> Optional[OrderDetailSchema]:
    """
    Build a full OrderDetailSchema for a given order_id.
    Fetches all order lines (with item/category info) and all payment records.
    """

    lines = (
        db.query(OrderHistory, MenuItem, Category)
        .join(MenuItem, OrderHistory.item_id == MenuItem.item_id)
        .join(Category, MenuItem.cat_id == Category.cat_id)
        .filter(OrderHistory.order_id == order_id)
        .all()
    )

    if not lines:
        return None

    order_date = lines[0][0].order_date

    order_items = [
        OrderLineSchema(
            id=oh.id,
            item_id=oh.item_id,
            item_name=mi.item_name,
            category=cat.category_name,
            size=oh.size,
            unit_price=oh.price,
            qty=oh.qty,
            line_total=round(oh.total, 4),
            order_status=oh.order_status,
        )
        for oh, mi, cat in lines
    ]

    items_total = round(sum(i.line_total for i in order_items), 4)

    payments_raw = db.query(Payment).filter(Payment.order_id == order_id).all()

    payment_schemas = [
        PaymentSchema(
            payment_id=p.payment_id,
            payment_date=p.payment_date,
            amount_due=p.amount_due,
            tips=p.tips,
            discount=p.discount,
            total_paid=p.total_paid,
            payment_type=p.payment_type,
            payment_status=p.payment_status,
        )
        for p in payments_raw
    ]

    amount_due     = payments_raw[0].amount_due if payments_raw else items_total
    total_paid     = round(sum(p.total_paid for p in payments_raw), 4)
    total_tips     = round(sum(p.tips for p in payments_raw), 4)
    total_discount = round(sum(p.discount for p in payments_raw), 4)
    balance        = round(amount_due - total_paid, 4)

    statuses = {p.payment_status for p in payments_raw}
    if not statuses:
        pay_status = "Pending"
    elif "Refunded" in statuses:
        pay_status = "Refunded"
    elif balance <= 0:
        pay_status = "Completed"
    else:
        pay_status = "Partial"

    return OrderDetailSchema(
        order_id=order_id,
        order_date=order_date,
        items=order_items,
        items_total=items_total,
        payments=payment_schemas,
        amount_due=amount_due,
        total_paid=total_paid,
        balance=balance,
        total_tips=total_tips,
        total_discount=total_discount,
        payment_status=pay_status,
    )


@router.get(
    "/orders",
    response_model=PaginatedOrdersResponse,
    summary="List all orders with full details",
    description=(
        "Returns a paginated list of all orders, each containing itemised order lines "
        "(item name, category, size, price, qty) and all associated payment records. "
        "Filter by date range or payment status."
    ),
)
def list_orders(
    page: int        = Query(1,    ge=1,  description="Page number (1-indexed)"),
    page_size: int   = Query(10,   ge=1,  le=100, description="Items per page (max 100)"),
    date_from: Optional[date] = Query(None, description="Filter orders on or after this date (YYYY-MM-DD)"),
    date_to:   Optional[date] = Query(None, description="Filter orders on or before this date (YYYY-MM-DD)"),
    status: Optional[str]     = Query(None, description="Filter by order_status e.g. Completed"),
    db: Session = Depends(get_db),
):
    # ── Gather distinct order IDs matching filters ──────────────────────────
    query = db.query(distinct(OrderHistory.order_id))

    if date_from:
        query = query.filter(OrderHistory.order_date >= date_from)
    if date_to:
        query = query.filter(OrderHistory.order_date <= date_to)
    if status:
        query = query.filter(OrderHistory.order_status == status)

    all_order_ids = sorted([row[0] for row in query.all()])
    total_orders  = len(all_order_ids)
    total_pages   = max(1, -(-total_orders // page_size))  # ceil division

    if page > total_pages and total_orders > 0:
        raise HTTPException(status_code=404, detail=f"Page {page} exceeds total pages ({total_pages})")

    # ── Paginate ────────────────────────────────────────────────────────────
    start = (page - 1) * page_size
    paged_ids = all_order_ids[start : start + page_size]

    orders = [build_order_detail(oid, db) for oid in paged_ids]
    orders = [o for o in orders if o is not None]

    return PaginatedOrdersResponse(
        page=page,
        page_size=page_size,
        total_orders=total_orders,
        total_pages=total_pages,
        orders=orders,
    )


@router.get(
    "/orders/{order_id}",
    response_model=OrderDetailSchema,
    summary="Get a single order by ID",
    description="Returns complete order details including all items, sizes, prices, and payment records.",
)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = build_order_detail(order_id, db)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order
