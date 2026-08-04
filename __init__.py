"""
GV Powers ERP - Database Models
Central import point for all models. Import db from here.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User  # noqa: E402, F401
from .customer import Customer  # noqa: E402, F401
from .product import Category, Product, StockMovement  # noqa: E402, F401
from .supplier import Supplier  # noqa: E402, F401
from .invoice import Invoice, InvoiceItem, Payment  # noqa: E402, F401
from .quotation import Quotation, QuotationItem  # noqa: E402, F401
from .purchase import PurchaseOrder, PurchaseItem  # noqa: E402, F401
from .settings import Settings, GSTMaster  # noqa: E402, F401
from .audit import AuditLog, Notification  # noqa: E402, F401
