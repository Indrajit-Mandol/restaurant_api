"""
seed.py - Populates the SQLite database with the exact sample data from the assessment PDF.
Run once: python seed.py
"""

from datetime import date
from app.database import engine, SessionLocal, Base
from app.models.models import Menu, Category, MenuItem, OrderHistory, Payment

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── Menus ─────────────────────────────────────────────────────────────────────
menus = [
    Menu(menu_id=1, menu_name="Food"),
    Menu(menu_id=2, menu_name="Drinks"),
]
db.add_all(menus)

# ── Categories ────────────────────────────────────────────────────────────────
categories = [
    Category(cat_id=1, category_name="Starters",   menu_id=1),
    Category(cat_id=2, category_name="Soft Drinks", menu_id=2),
    Category(cat_id=3, category_name="Mains",       menu_id=1),
    Category(cat_id=4, category_name="Desserts",    menu_id=2),
    Category(cat_id=5, category_name="Hot Drinks",  menu_id=2),
]
db.add_all(categories)

# ── Menu Items ────────────────────────────────────────────────────────────────
items = [
    MenuItem(item_id=1,  item_name="Item1",  cat_id=1, menu_id=1, sizes="Small, Large", prices="1.50, 2.50"),
    MenuItem(item_id=2,  item_name="Item2",  cat_id=1, menu_id=1, sizes=None,           prices="3"),
    MenuItem(item_id=3,  item_name="Item3",  cat_id=2, menu_id=2, sizes=None,           prices="2.5"),
    MenuItem(item_id=4,  item_name="Item4",  cat_id=2, menu_id=2, sizes=None,           prices="1.5"),
    MenuItem(item_id=5,  item_name="Item5",  cat_id=2, menu_id=1, sizes=None,           prices="1"),
    MenuItem(item_id=6,  item_name="Item6",  cat_id=3, menu_id=1, sizes="Small, Large", prices="2.50, 3.6"),
    MenuItem(item_id=7,  item_name="Item7",  cat_id=3, menu_id=1, sizes=None,           prices="2.5"),
    MenuItem(item_id=8,  item_name="Item8",  cat_id=4, menu_id=2, sizes="Small, Large", prices="3.75, 6.5"),
    MenuItem(item_id=9,  item_name="Item9",  cat_id=4, menu_id=2, sizes=None,           prices="1.5"),
    MenuItem(item_id=10, item_name="Item10", cat_id=5, menu_id=2, sizes=None,           prices="2"),
]
db.add_all(items)

# ── Order History ─────────────────────────────────────────────────────────────
d1 = date(2025, 10, 1)
d2 = date(2025, 10, 2)
d3 = date(2025, 10, 3)
d5 = date(2025, 10, 5)

order_rows = [
    # Order 10
    OrderHistory(id=1,  order_date=d1, order_id=10, item_id=2,  size=None,    price=2.5,     qty=1, order_status="Completed", total=2.5),
    OrderHistory(id=2,  order_date=d1, order_id=10, item_id=3,  size=None,    price=1.5,     qty=2, order_status="Completed", total=3.0),
    OrderHistory(id=3,  order_date=d1, order_id=10, item_id=1,  size="Small", price=3.75,    qty=1, order_status="Completed", total=3.75),
    # Order 11
    OrderHistory(id=4,  order_date=d1, order_id=11, item_id=5,  size=None,    price=2.75,    qty=1, order_status="Completed", total=2.75),
    OrderHistory(id=5,  order_date=d1, order_id=11, item_id=6,  size=None,    price=1.75,    qty=2, order_status="Completed", total=3.5),
    OrderHistory(id=6,  order_date=d1, order_id=11, item_id=2,  size=None,    price=2.5,     qty=1, order_status="Completed", total=2.5),
    OrderHistory(id=7,  order_date=d1, order_id=11, item_id=3,  size=None,    price=3.5,     qty=1, order_status="Completed", total=3.5),
    OrderHistory(id=8,  order_date=d1, order_id=11, item_id=4,  size=None,    price=3.75,    qty=2, order_status="Completed", total=7.5),
    OrderHistory(id=9,  order_date=d1, order_id=11, item_id=5,  size=None,    price=1.5,     qty=1, order_status="Completed", total=1.5),
    # Order 12
    OrderHistory(id=10, order_date=d1, order_id=12, item_id=6,  size="Large", price=5.5,     qty=2, order_status="Completed", total=11.0),
    OrderHistory(id=11, order_date=d1, order_id=12, item_id=7,  size=None,    price=2.5,     qty=1, order_status="Completed", total=2.5),
    OrderHistory(id=12, order_date=d1, order_id=12, item_id=1,  size="Large", price=3.5,     qty=1, order_status="Completed", total=3.5),
    # Order 13
    OrderHistory(id=13, order_date=d1, order_id=13, item_id=1,  size="Small", price=2.75,    qty=2, order_status="Completed", total=5.5),
    OrderHistory(id=14, order_date=d1, order_id=13, item_id=6,  size="Small", price=1.5,     qty=1, order_status="Completed", total=1.5),
    OrderHistory(id=15, order_date=d1, order_id=13, item_id=8,  size="Small", price=3.5,     qty=1, order_status="Completed", total=3.5),
    OrderHistory(id=16, order_date=d1, order_id=13, item_id=1,  size="Small", price=2.5,     qty=2, order_status="Completed", total=5.0),
    # Order 14
    OrderHistory(id=17, order_date=d1, order_id=14, item_id=6,  size="Large", price=2.75,    qty=1, order_status="Completed", total=2.75),
    OrderHistory(id=18, order_date=d1, order_id=14, item_id=1,  size="Large", price=2.75655, qty=2, order_status="Completed", total=5.5131),
    OrderHistory(id=19, order_date=d1, order_id=14, item_id=8,  size="Large", price=2.75,    qty=2, order_status="Completed", total=5.5),
    OrderHistory(id=20, order_date=d1, order_id=14, item_id=1,  size="Large", price=2.7556,  qty=2, order_status="Completed", total=5.5112),
    OrderHistory(id=21, order_date=d1, order_id=14, item_id=4,  size=None,    price=5.5,     qty=1, order_status="Completed", total=5.5),
    OrderHistory(id=22, order_date=d1, order_id=14, item_id=3,  size=None,    price=2.75,    qty=2, order_status="Completed", total=5.5),
    OrderHistory(id=23, order_date=d1, order_id=14, item_id=2,  size=None,    price=3.5,     qty=1, order_status="Completed", total=3.5),
    OrderHistory(id=24, order_date=d1, order_id=14, item_id=6,  size="Large", price=3.015,   qty=3, order_status="Completed", total=9.045),
    # Order 15
    OrderHistory(id=25, order_date=d2, order_id=15, item_id=2,  size=None,    price=2.568,   qty=2, order_status="Completed", total=5.136),
    # Order 16
    OrderHistory(id=26, order_date=d3, order_id=16, item_id=6,  size="Large", price=6.586,   qty=3, order_status="Completed", total=19.758),
    # Order 17
    OrderHistory(id=27, order_date=d1, order_id=17, item_id=10, size=None,    price=2.5,     qty=1, order_status="Completed", total=2.5),
    OrderHistory(id=28, order_date=d1, order_id=17, item_id=9,  size=None,    price=2.75636, qty=1, order_status="Completed", total=2.75636),
    OrderHistory(id=29, order_date=d1, order_id=17, item_id=7,  size=None,    price=5.63982, qty=1, order_status="Completed", total=5.63982),
    # Order 18
    OrderHistory(id=30, order_date=d5, order_id=18, item_id=1,  size="Small", price=2.5698,  qty=2, order_status="Completed", total=5.1396),
    OrderHistory(id=31, order_date=d5, order_id=18, item_id=6,  size="Small", price=5.36245, qty=2, order_status="Completed", total=10.7249),
    OrderHistory(id=32, order_date=d5, order_id=18, item_id=8,  size="Small", price=5.23569, qty=2, order_status="Completed", total=10.47138),
    # Order 19
    OrderHistory(id=33, order_date=d1, order_id=19, item_id=2,  size=None,    price=2.75698, qty=1, order_status="Completed", total=2.75698),
    OrderHistory(id=34, order_date=d1, order_id=19, item_id=4,  size=None,    price=2.356,   qty=1, order_status="Completed", total=2.356),
    OrderHistory(id=35, order_date=d1, order_id=19, item_id=5,  size=None,    price=2.457,   qty=2, order_status="Completed", total=4.914),
    OrderHistory(id=36, order_date=d1, order_id=19, item_id=7,  size=None,    price=2.6359,  qty=1, order_status="Completed", total=2.6359),
    OrderHistory(id=37, order_date=d1, order_id=19, item_id=9,  size=None,    price=6.523,   qty=1, order_status="Completed", total=6.523),
    OrderHistory(id=38, order_date=d1, order_id=19, item_id=10, size=None,    price=8.5412,  qty=3, order_status="Completed", total=25.6236),
    OrderHistory(id=39, order_date=d1, order_id=19, item_id=6,  size="Large", price=5.683,   qty=2, order_status="Completed", total=11.366),
    OrderHistory(id=41, order_date=d1, order_id=19, item_id=2,  size=None,    price=6.3564,  qty=1, order_status="Completed", total=6.3564),
    OrderHistory(id=42, order_date=d1, order_id=19, item_id=5,  size=None,    price=7.235,   qty=1, order_status="Completed", total=7.235),
    OrderHistory(id=43, order_date=d1, order_id=19, item_id=7,  size=None,    price=2.365,   qty=1, order_status="Completed", total=2.365),
    # Order 20
    OrderHistory(id=44, order_date=d1, order_id=20, item_id=1,  size="Large", price=2.3658,  qty=1, order_status="Completed", total=2.3658),
    OrderHistory(id=45, order_date=d1, order_id=20, item_id=3,  size=None,    price=2.356,   qty=1, order_status="Completed", total=2.356),
    OrderHistory(id=46, order_date=d1, order_id=20, item_id=6,  size="Large", price=1.256,   qty=1, order_status="Completed", total=1.256),
    OrderHistory(id=47, order_date=d1, order_id=20, item_id=4,  size=None,    price=2.635,   qty=1, order_status="Completed", total=2.635),
    OrderHistory(id=48, order_date=d1, order_id=20, item_id=5,  size=None,    price=5.21,    qty=1, order_status="Completed", total=5.21),
    OrderHistory(id=49, order_date=d1, order_id=20, item_id=7,  size=None,    price=6.325,   qty=2, order_status="Completed", total=12.65),
    OrderHistory(id=50, order_date=d1, order_id=20, item_id=8,  size="Small", price=7.2514,  qty=1, order_status="Completed", total=7.2514),
    OrderHistory(id=51, order_date=d1, order_id=20, item_id=9,  size=None,    price=2.3999,  qty=1, order_status="Completed", total=2.3999),
    OrderHistory(id=52, order_date=d1, order_id=20, item_id=4,  size=None,    price=2.356,   qty=3, order_status="Completed", total=7.068),
    OrderHistory(id=53, order_date=d1, order_id=20, item_id=6,  size="Small", price=4.5326,  qty=2, order_status="Completed", total=9.0652),
]
db.add_all(order_rows)

# ── Payments ──────────────────────────────────────────────────────────────────
payments = [
    Payment(id=1,  payment_date=d1, payment_id=100, order_id=10, amount_due=9.25,     tips=0, discount=0, total_paid=9.25,  payment_type="Card", payment_status="Completed"),
    Payment(id=2,  payment_date=d1, payment_id=101, order_id=11, amount_due=21.25,    tips=0, discount=0, total_paid=10.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=3,  payment_date=d1, payment_id=102, order_id=11, amount_due=21.25,    tips=0, discount=0, total_paid=11.25, payment_type="Card", payment_status="Completed"),
    Payment(id=4,  payment_date=d2, payment_id=103, order_id=12, amount_due=17.0,     tips=3, discount=4, total_paid=16.0,  payment_type="Card", payment_status="Completed"),
    Payment(id=5,  payment_date=d3, payment_id=104, order_id=13, amount_due=15.5,     tips=0, discount=2, total_paid=13.5,  payment_type="Card", payment_status="Completed"),
    Payment(id=6,  payment_date=d1, payment_id=105, order_id=14, amount_due=42.8193,  tips=0, discount=0, total_paid=20.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=7,  payment_date=d1, payment_id=106, order_id=14, amount_due=42.8193,  tips=0, discount=0, total_paid=22.82, payment_type="Card", payment_status="Completed"),
    Payment(id=8,  payment_date=d2, payment_id=107, order_id=15, amount_due=5.136,    tips=0, discount=0, total_paid=5.14,  payment_type="Card", payment_status="Refunded"),
    Payment(id=9,  payment_date=d3, payment_id=108, order_id=16, amount_due=19.758,   tips=0, discount=0, total_paid=10.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=10, payment_date=d3, payment_id=109, order_id=16, amount_due=19.758,   tips=0, discount=0, total_paid=9.76,  payment_type="Card", payment_status="Completed"),
    Payment(id=11, payment_date=d1, payment_id=110, order_id=17, amount_due=10.8918,  tips=0, discount=0, total_paid=10.9,  payment_type="Card", payment_status="Completed"),
    Payment(id=12, payment_date=d5, payment_id=111, order_id=18, amount_due=26.33588, tips=2, discount=0, total_paid=25.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=13, payment_date=d5, payment_id=115, order_id=18, amount_due=26.33588, tips=0, discount=0, total_paid=3.34,  payment_type="Card", payment_status="Completed"),
    Payment(id=14, payment_date=d1, payment_id=116, order_id=19, amount_due=72.13188, tips=0, discount=0, total_paid=50.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=15, payment_date=d1, payment_id=119, order_id=19, amount_due=72.13188, tips=0, discount=0, total_paid=22.13, payment_type="Card", payment_status="Completed"),
    Payment(id=16, payment_date=d1, payment_id=120, order_id=20, amount_due=52.2573,  tips=0, discount=0, total_paid=25.0,  payment_type="Cash", payment_status="Completed"),
    Payment(id=17, payment_date=d1, payment_id=121, order_id=20, amount_due=52.2573,  tips=0, discount=0, total_paid=27.28, payment_type="Card", payment_status="Completed"),
]
db.add_all(payments)

db.commit()
db.close()

print("✅ Database seeded successfully with all PDF data.")
