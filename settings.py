from datetime import datetime
from models import db


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GSTMaster(db.Model):
    __tablename__ = "gst_master"

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float, unique=True, nullable=False)
    cgst_rate = db.Column(db.Float, nullable=False)
    sgst_rate = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
