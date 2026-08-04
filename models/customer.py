from datetime import datetime
from sqlalchemy import func
from models import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    mobile = db.Column(db.String(20), nullable=True, index=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    state_code = db.Column(db.Integer, default=29)
    gstin = db.Column(db.String(20), nullable=True)
    pan = db.Column(db.String(10), nullable=True)
    customer_type = db.Column(db.String(20), default="B2C")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    invoices = db.relationship("Invoice", backref="customer", lazy="dynamic")
    quotations = db.relationship("Quotation", backref="customer", lazy="dynamic")

    @property
    def total_purchases(self) -> float:
        from models import Invoice
        return db.session.query(func.coalesce(func.sum(Invoice.grand_total), 0.0)).filter(
            Invoice.customer_id == self.id, Invoice.status != "cancelled"
        ).scalar()

    @property
    def invoice_count(self) -> int:
        from models import Invoice
        return Invoice.query.filter_by(customer_id=self.id).filter(
            Invoice.status != "cancelled"
        ).count()
