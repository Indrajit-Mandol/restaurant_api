# 🍽️ Restaurant Orders API

A production-grade **Python REST API** built with **FastAPI** and **SQLAlchemy** that exposes full order details — items, sizes, prices, quantities, and payment breakdowns — from a restaurant database.

---

## 📋 Table of Contents

- [Data Analysis & Findings](#-data-analysis--findings-task-1)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Postman Usage](#-postman-usage)
- [Security](#-security)
- [Performance](#-performance)
- [Design Decisions](#-design-decisions)

---

## 🔍 Data Analysis & Findings (Task 1)

### Schema Overview

| Table          | Key Fields                                                  | Purpose                           |
|----------------|-------------------------------------------------------------|-----------------------------------|
| `menus`        | menu_id, menu_name                                          | Top-level menu grouping (Food / Drinks) |
| `categories`   | cat_id, category_name, menu_id                              | Item categories within a menu     |
| `menu_items`   | item_id, item_name, cat_id, menu_id, sizes, prices          | Master price list                 |
| `order_history`| id, order_id, item_id, size, price, qty, total              | One row per line item per order   |
| `payments`     | payment_id, order_id, amount_due, tips, discount, total_paid| One row per payment transaction   |

### Key Findings

#### 1. Split Payments (Multi-row per Order)
Several orders have **more than one payment record**, indicating split payment behaviour:

| Order ID | Payment Records | Explanation                          |
|----------|-----------------|--------------------------------------|
| 11       | 101, 102        | Cash £10 + Card £11.25 = £21.25      |
| 14       | 105, 106        | Cash £20 + Card £22.82 = £42.82      |
| 16       | 108, 109        | Cash £10 + Card £9.76 = £19.76       |
| 18       | 111, 115        | Cash £25 + Card £3.34 = £28.34       |
| 19       | 116, 119        | Cash £50 + Card £22.13 = £72.13      |
| 20       | 120, 121        | Cash £25 + Card £27.28 = £52.28      |

> **Implication:** To get the total paid for an order you must `SUM(total_paid)` across all payment rows, not just take the first record.

#### 2. Price Inconsistency vs Menu Master
The `menu_items` table defines standard prices, but `order_history` prices often **deviate significantly**:

- **Item1 (menu: Small £1.50 / Large £2.50)** appears in orders at £2.75, £2.7566, £3.75 etc.
- **Item6 (menu: Small £2.50 / Large £3.60)** appears at £1.75, £2.75, £3.015, £5.5, £6.586

> **Possible reasons:** Time-based pricing, manual override at POS, promotional pricing, or data entry errors. This is worth flagging — a pricing audit system would help detect outliers.

#### 3. Floating Point Precision in Prices
Several prices have excessive decimal precision (`2.75655`, `5.63982`, `2.75636`) and `total` values like `25.6236`. This suggests prices were **computed rather than input** (e.g. dynamic pricing, modifiers, or promotions). The DB should store prices as `DECIMAL(10,4)` rather than `FLOAT` to avoid rounding drift.

#### 4. Refunded Order (Order 15)
Order 15 has a single payment (ID 107) with `payment_status = "Refunded"`. It is the only refunded order in the dataset. The full amount (£5.14) was refunded.

#### 5. Row ID Gap (IDs 39 → 41)
In `order_history`, row ID 40 is missing (jumps from 39 to 41). This implies either a **soft-deleted row** or a failed insert that incremented the auto-increment counter. Worth investigating for data integrity.

#### 6. Order 19 Has the Most Items (10 line items)
Order 19 is the largest order by both item count and value (£72.13 amount due). It spans Hot Drinks, Soft Drinks, Mains, and Starters — a full-table order.

#### 7. `amount_due` Is Duplicated Across Payment Rows
For split payments, `amount_due` is repeated on every payment row (e.g. Order 14 has £42.82 on both rows). This is the **total bill**, not per-transaction amount. The API correctly reads it from the first row only.

#### 8. Discount & Tips Are Rare
Only 3 orders have non-zero tips or discounts:
- Order 12: £3 tip, £4 discount
- Order 13: £2 discount
- Order 18: £2 tip

---

## 📁 Project Structure

```
restaurant_api/
├── app/
│   ├── main.py              # FastAPI app, middlewares, router registration
│   ├── database.py          # SQLAlchemy engine & session
│   ├── models/
│   │   └── models.py        # ORM models (Menu, Category, MenuItem, OrderHistory, Payment)
│   ├── schemas/
│   │   └── schemas.py       # Pydantic response schemas
│   └── routers/
│       ├── orders.py        # GET /orders, GET /orders/{id}
│       ├── menu.py          # GET /menu, GET /categories
│       └── payments.py      # GET /payments
├── seed.py                  # One-time DB population script
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Framework   | FastAPI 0.115                        |
| ORM         | SQLAlchemy 2.0                       |
| Validation  | Pydantic v2                          |
| Database    | SQLite (dev) / PostgreSQL (prod)     |
| Server      | Uvicorn (ASGI)                       |
| Docs        | Swagger UI (auto-generated)          |

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone <repo-url>
cd restaurant_api

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Seed the database

```bash
python seed.py
# ✅ Database seeded successfully with all PDF data.
```

This creates `restaurant.db` (SQLite) with all 11 orders, 17 payment records, 10 menu items, 5 categories, and 2 menus from the assessment data.

### 3. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Open docs

- Swagger UI → http://localhost:8000/docs
- ReDoc     → http://localhost:8000/redoc

---

## 📡 API Endpoints

### `GET /api/v1/orders`
List all orders with full details (paginated).

**Query Parameters:**

| Parameter   | Type   | Default | Description                              |
|-------------|--------|---------|------------------------------------------|
| `page`      | int    | 1       | Page number                              |
| `page_size` | int    | 10      | Results per page (max 100)               |
| `date_from` | date   | —       | Filter from date (YYYY-MM-DD)            |
| `date_to`   | date   | —       | Filter to date (YYYY-MM-DD)              |
| `status`    | string | —       | Filter by order_status e.g. `Completed`  |

**Example:**
```
GET /api/v1/orders?page=1&page_size=5&date_from=2025-10-01
```

**Response fields per order:**
```json
{
  "order_id": 10,
  "order_date": "2025-10-01",
  "items": [
    {
      "id": 1,
      "item_id": 2,
      "item_name": "Item2",
      "category": "Starters",
      "size": null,
      "unit_price": 2.5,
      "qty": 1,
      "line_total": 2.5,
      "order_status": "Completed"
    }
  ],
  "items_total": 9.25,
  "payments": [
    {
      "payment_id": 100,
      "payment_date": "2025-10-01",
      "amount_due": 9.25,
      "tips": 0.0,
      "discount": 0.0,
      "total_paid": 9.25,
      "payment_type": "Card",
      "payment_status": "Completed"
    }
  ],
  "amount_due": 9.25,
  "total_paid": 9.25,
  "balance": 0.0,
  "total_tips": 0.0,
  "total_discount": 0.0,
  "payment_status": "Completed"
}
```

---

### `GET /api/v1/orders/{order_id}`
Get a single order by its ID.

```
GET /api/v1/orders/14
```

---

### `GET /api/v1/menu`
List all menu items with sizes and prices.

---

### `GET /api/v1/categories`
List all categories with their menu group.

---

### `GET /api/v1/payments`
List all payment records.

**Query Parameters:**

| Parameter      | Type   | Description                          |
|----------------|--------|--------------------------------------|
| `status`       | string | e.g. `Completed`, `Refunded`         |
| `payment_type` | string | e.g. `Card`, `Cash`                  |

---

## 📬 Postman Usage

1. Import a new request in Postman
2. Set method to **GET**
3. Set URL to `http://localhost:8000/api/v1/orders`
4. Add query params in the **Params** tab as needed
5. Hit **Send** — you'll see the full paginated order response

You can also visit `http://localhost:8000/docs` to **try all endpoints live** in the browser with Swagger UI.

---

## 🔒 Security

| Measure                   | Implementation                                               |
|---------------------------|--------------------------------------------------------------|
| CORS middleware           | Configured via `CORSMiddleware` (restrict `allow_origins` in prod) |
| TrustedHost middleware    | `TrustedHostMiddleware` — whitelist domains in production    |
| Input validation          | Pydantic validates all query parameters and response shapes  |
| Read-only API             | Only `GET` methods are allowed (no write endpoints exposed)  |
| SQL injection prevention  | SQLAlchemy ORM — no raw SQL string interpolation             |
| No secrets in code        | `DATABASE_URL` loaded from env variable via `os.getenv`      |

**For production additionally add:**
- API key / JWT authentication header
- Rate limiting (e.g. `slowapi`)
- HTTPS via reverse proxy (Nginx/Caddy)
- Restrict `allow_origins` to known frontend domains

---

## ⚡ Performance

| Measure                  | Implementation                                              |
|--------------------------|-------------------------------------------------------------|
| Pagination               | All list endpoints are paginated (max 100 per page)         |
| Eager JOIN queries       | Orders endpoint joins `order_history → menu_items → categories` in one query |
| DB indexes               | `order_id`, `item_id`, `payment_id` are indexed in ORM models |
| Request timing header    | `X-Process-Time` header shows ms per request                |
| Connection pooling       | SQLAlchemy handles connection pool automatically            |

**For production additionally consider:**
- Redis caching for menu (rarely changes)
- Async SQLAlchemy with `asyncpg` for PostgreSQL
- Query result caching on paginated order lists

---

## 🎯 Design Decisions

**Why FastAPI?**
Auto-generates Swagger/ReDoc documentation, built-in Pydantic validation, async-ready, and fast to iterate on — ideal for a demonstration API.

**Why SQLite for dev?**
Zero setup — just run `seed.py` and you're live. The `DATABASE_URL` env var makes it trivial to switch to PostgreSQL or MySQL in production without changing application code.

**Why separate `items_total` vs `amount_due`?**
`items_total` is computed from `order_history` rows (sum of line totals). `amount_due` comes from the `payments` table. In the data these often differ (due to discounts, rounding, or timing), so both are exposed separately for transparency.

**Why `payment_status` on the order level?**
Individual payment rows have their own status (Completed/Refunded), but the API rolls this up to an order-level status (`Completed`, `Partial`, `Refunded`, `Pending`) so clients can filter or display it easily without joining themselves.
