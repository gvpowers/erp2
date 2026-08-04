from datetime import datetime, date
from models import db


class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    invoice_date = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default="draft")
    customer_name = db.Column(db.String(200), nullable=True)
    customer_mobile = db.Column(db.String(20), nullable=True)
    customer_address = db.Column(db.Text, nullable=True)
    customer_state = db.Column(db.String(100), nullable=True)
    customer_state_code = db.Column(db.Integer, default=29)
    customer_gstin = db.Column(db.String(20), nullable=True)
    is_intra_state = db.Column(db.Boolean, default=True)
    subtotal = db.Column(db.Float, default=0.0)
    total_discount = db.Column(db.Float, default=0.0)
    total_taxable = db.Column(db.Float, default=0.0)
    total_cgst = db.Column(db.Float, default=0.0)
    total_sgst = db.Column(db.Float, default=0.0)
    total_igst = db.Column(db.Float, default=0.0)
    round_off = db.Column(db.Float, default=0.0)
    grand_total = db.Column(db.Float, default=0.0)
    amount_paid = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(30), nullable=True)
    payment_reference = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    terms = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("InvoiceItem", backref="invoice", lazy="selectin", cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="invoice", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def balance(self) -> float:
        return self.grand_total - self.amount_paid

    @property
    def is_paid(self) -> bool:
        return self.balance <= 0


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
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

    product = db.relationship("Product", backref="invoice_items")


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    reference_number = db.Column(db.String(100), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
