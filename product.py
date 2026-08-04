from datetime import datetime
from models import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship("Product", backref="category", lazy="dynamic")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=True, index=True)
    barcode = db.Column(db.String(50), unique=True, nullable=True, index=True)
    hsn = db.Column(db.String(20), nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    unit = db.Column(db.String(20), default="Pcs")
    purchase_price = db.Column(db.Float, default=0.0)
    selling_price = db.Column(db.Float, default=0.0)
    gst_rate = db.Column(db.Float, default=18.0)
    opening_stock = db.Column(db.Integer, default=0)
    current_stock = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5)
    max_stock = db.Column(db.Integer, default=500)
    location = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default="active")
    last_purchase = db.Column(db.DateTime, nullable=True)
    last_sale = db.Column(db.DateTime, nullable=True)
    warehouse = db.Column(db.String(100), nullable=True)
    warranty = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(256), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_low_stock(self) -> bool:
        return self.current_stock <= self.min_stock

    @property
    def stock_status(self) -> str:
        if self.current_stock <= 0:
            return "out_of_stock"
        if self.is_low_stock:
            return "low_stock"
        return "in_stock"

    @property
    def available_stock_value(self) -> float:
        return round(self.current_stock * self.purchase_price, 2)


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    movement_type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(db.String(30), nullable=True)
    reference_id = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    product = db.relationship("Product", backref="movements")
    user = db.relationship("User", backref="stock_movements")
