"""
GV Powers ERP - Database Seed
Creates default users, categories, GST master, and settings.
"""

import logging
from models import db, User, Category, GSTMaster, Settings


def seed_database(config: dict):
    """Seed default data if database is empty."""
    admin_user = config.get("ADMIN_USERNAME", "admin")
    admin_pass = config.get("ADMIN_PASSWORD", "Admin@123")
    admin_email = config.get("ADMIN_EMAIL", "admin@gvpowers.in")

    if not User.query.filter_by(username=admin_user).first():
        admin = User(username=admin_user, email=admin_email,
                     full_name="Administrator", role="admin", theme="dark")
        admin.set_password(admin_pass)
        db.session.add(admin)

    if not User.query.filter_by(username="sales").first():
        sales = User(username="sales", email="sales@gvpowers.in",
                     full_name="Sales User", role="sales", theme="dark")
        sales.set_password("Sales@123")
        db.session.add(sales)

    for cat_name in [
        "Solar Panels", "Solar Inverters", "Solar Batteries", "UPS Systems",
        "RO Systems", "RO Filters", "Hardware", "Electrical Items",
        "Cables & Wires", "Accessories",
    ]:
        if not Category.query.filter_by(name=cat_name).first():
            db.session.add(Category(name=cat_name))

    for rate, cgst, sgst, desc_text in [
        (0, 0, 0, "Exempt"), (5, 2.5, 2.5, "5% GST"), (12, 6, 6, "12% GST"),
        (18, 9, 9, "18% GST"), (28, 14, 14, "28% GST"),
    ]:
        if not GSTMaster.query.filter_by(rate=rate).first():
            db.session.add(GSTMaster(rate=rate, cgst_rate=cgst, sgst_rate=sgst, description=desc_text))

    defaults = {
        "invoice_terms": "1. Goods once sold will not be returned.\n2. Subject to local jurisdiction.\n3. E&OE.",
        "quotation_terms": "1. This quotation is valid for 15 days.\n2. Prices are inclusive of applicable taxes.",
        "default_gst_rate": "18", "low_stock_threshold": "5",
        "company_name": config.get("COMPANY_NAME", "GV Powers"),
        "company_gstin": config.get("COMPANY_GSTIN", "29AAAAA0000A1Z5"),
        "company_state": config.get("COMPANY_STATE", "Karnataka"),
        "company_state_code": str(config.get("COMPANY_STATE_CODE", 29)),
        "company_address": config.get("COMPANY_ADDRESS", "Bangalore, Karnataka, India"),
        "company_phone": config.get("COMPANY_PHONE", "+91-9876543210"),
        "company_email": config.get("COMPANY_EMAIL", "gvpowerssalem@gmail.com"),
    }
    for key, val in defaults.items():
        if not Settings.query.filter_by(key=key).first():
            db.session.add(Settings(key=key, value=str(val)))

    db.session.commit()
    logging.info("Database seeded successfully.")
