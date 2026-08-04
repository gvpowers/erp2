from datetime import datetime, date
from models import db


class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    quotation_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    customer_name = db.Column(db.String(200), nullable=True)
    customer_mobile = db.Column(db.String(20), nullable=True)
    customer_address = db.Column(db.Text, nullable=True)
    customer_state = db.Column(db.String(100), nullable=True)
    customer_state_code = db.Column(db.Integer, default=29)
    customer_gstin = db.Column(db.String(20), nullable=True)
    quotation_date = db.Column(db.Date, default=date.today)
    valid_until = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default="draft")
    subtotal = db.Column(db.Float, default=0.0)
    total_discount = db.Column(db.Float, default=0.0)
    total_taxable = db.Column(db.Float, default=0.0)
    total_cgst = db.Column(db.Float, default=0.0)
    total_sgst = db.Column(db.Float, default=0.0)
    total_igst = db.Column(db.Float, default=0.0)
    round_off = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    terms = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user = db.relationship("User", backref="quotations_created")
    items = db.relationship("QuotationItem", backref="quotation", lazy="selectin", cascade="all, delete-orphan")


class QuotationItem(db.Model):
    __tablename__ = "quotation_items"

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    product_name = db.Column(db.String(300), nullable=False)
    hsn = db.Column(db.String(20), nullable=True)
    qty = db.Column(db.Integer, default=1)
    unit = db.Column(db.String(20), default="Pcs")
    price = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    gst_rate = db.Column(db.Float, default=18.0)
    taxable_value = db.Column(db.Float, default=0.0)
    cgst = db.Column(db.Float, default=0.0)
    sgst = db.Column(db.Float, default=0.0)
    igst = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    product = db.relationship("Product", backref="quotation_items")
