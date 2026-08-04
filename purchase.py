from datetime import datetime, date
from models import db


class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    order_date = db.Column(db.Date, default=date.today)
    expected_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default="draft")
    subtotal = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    items = db.relationship("PurchaseItem", backref="purchase_order", lazy="selectin", cascade="all, delete-orphan")


class PurchaseItem(db.Model):
    __tablename__ = "purchase_items"

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey("purchase_orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    product_name = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, default=0.0)
    gst_rate = db.Column(db.Float, default=18.0)
    total = db.Column(db.Float, default=0.0)

    product = db.relationship("Product", backref="purchase_items")
