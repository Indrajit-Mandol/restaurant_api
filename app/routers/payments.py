"""
Payments Router - exposes payment records.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.models import Payment
from app.schemas.schemas import PaymentSchema

router = APIRouter()


@router.get(
    "/payments",
    response_model=List[PaymentSchema],
    summary="List all payment records",
    description="Returns all payment transactions. Filter by payment_status or payment_type.",
)
def list_payments(
    status: Optional[str] = Query(None, description="e.g. Completed, Refunded"),
    payment_type: Optional[str] = Query(None, description="e.g. Card, Cash"),
    db: Session = Depends(get_db),
):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.payment_status == status)
    if payment_type:
        query = query.filter(Payment.payment_type == payment_type)
    return query.all()
