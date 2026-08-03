"""
GV Powers ERP - Configuration
Environment-based config for Development and Production.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/gv_powers_erp",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }

    SESSION_TYPE = "sqlalchemy"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    BASE_DIR = BASE_DIR
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    BACKUP_FOLDER = os.path.join(BASE_DIR, "backups", "database")
    PDF_FOLDER = os.path.join(BASE_DIR, "pdf")
    EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
    LOG_FOLDER = os.path.join(BASE_DIR, "logs")

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_SIZE", 16 * 1024 * 1024))

    COMPANY_NAME = os.getenv("COMPANY_NAME", "GV Powers")
    COMPANY_TAGLINE = os.getenv("COMPANY_TAGLINE", "Powering A Better Tomorrow")
    COMPANY_SERVICES = os.getenv(
        "COMPANY_SERVICES",
        "Solar Energy | UPS Systems | Inverters | RO Solutions | Electricals",
    )
    COMPANY_GSTIN = os.getenv("COMPANY_GSTIN", "29AAAAA0000A1Z5")
    COMPANY_PAN = os.getenv("COMPANY_PAN", "AAAAA0000A")
    COMPANY_STATE = os.getenv("COMPANY_STATE", "Karnataka")
    COMPANY_STATE_CODE = int(os.getenv("COMPANY_STATE_CODE", "29"))
    COMPANY_ADDRESS = os.getenv("COMPANY_ADDRESS", "Bangalore, Karnataka, India")
    COMPANY_PHONE = os.getenv("COMPANY_PHONE", "+91-9876543210")
    COMPANY_EMAIL = os.getenv("COMPANY_EMAIL", "gvpowerssalem@gmail.com")
    COMPANY_WEBSITE = os.getenv("COMPANY_WEBSITE", "https://gvpowers.in")

    BANK_NAME = os.getenv("BANK_NAME", "State Bank of India")
    BANK_ACCOUNT = os.getenv("BANK_ACCOUNT", "12345678901234")
    BANK_IFSC = os.getenv("BANK_IFSC", "SBIN0001234")
    UPI_ID = os.getenv("UPI_ID", "gvpowers@upi")

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gvpowers.in")

    GST_RATES = [0, 5, 12, 18, 28]

    @property
    def COMPANY(self):
        return {
            "name": self.COMPANY_NAME,
            "tagline": self.COMPANY_TAGLINE,
            "services": self.COMPANY_SERVICES,
            "gstin": self.COMPANY_GSTIN,
            "pan": self.COMPANY_PAN,
            "state": self.COMPANY_STATE,
            "state_code": self.COMPANY_STATE_CODE,
            "address": self.COMPANY_ADDRESS,
            "phone": self.COMPANY_PHONE,
            "email": self.COMPANY_EMAIL,
            "website": self.COMPANY_WEBSITE,
            "bank_name": self.BANK_NAME,
            "bank_account": self.BANK_ACCOUNT,
            "bank_ifsc": self.BANK_IFSC,
            "upi_id": self.UPI_ID,
        }


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db"),
    )
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
