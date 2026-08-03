"""
Seed script: Add test products with full details for GV Powers ERP.
Run: python seed_products.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Product, Category, Supplier

PRODUCTS = [
    # ── Solar Panels ──
    {"name": "Tata Solar Mono PERC 330W", "sku": "SOL-TP-330", "barcode": "8901234560001", "hsn": "8541",
     "brand": "Tata Solar", "category": "Solar Panels", "unit": "Pcs", "purchase_price": 8500, "selling_price": 12500,
     "gst_rate": 12, "opening_stock": 40, "current_stock": 40, "min_stock": 10, "max_stock": 200,
     "warranty": "25 Years Performance", "description": "330W Mono PERC Solar Panel, 5 Busbar, Efficiency 19.5%"},
    {"name": "Vikram Solar Half-Cut 375W", "sku": "SOL-VK-375", "barcode": "8901234560002", "hsn": "8541",
     "brand": "Vikram Solar", "category": "Solar Panels", "unit": "Pcs", "purchase_price": 9800, "selling_price": 14200,
     "gst_rate": 12, "opening_stock": 30, "current_stock": 30, "min_stock": 8, "max_stock": 150,
     "warranty": "25 Years Linear", "description": "375W Half-Cut Mono PERC, 144 Cells, IP67 Junction Box"},
    {"name": "Waaree Polycrystalline 320W", "sku": "SOL-WR-320", "barcode": "8901234560003", "hsn": "8541",
     "brand": "Waaree", "category": "Solar Panels", "unit": "Pcs", "purchase_price": 6800, "selling_price": 9800,
     "gst_rate": 12, "opening_stock": 50, "current_stock": 50, "min_stock": 10, "max_stock": 200,
     "warranty": "25 Years", "description": "320W Polycrystalline Solar Panel, 72 Cells"},
    {"name": "Adani Solar Mono PERC 540W", "sku": "SOL-AD-540", "barcode": "8901234560004", "hsn": "8541",
     "brand": "Adani Solar", "category": "Solar Panels", "unit": "Pcs", "purchase_price": 14500, "selling_price": 21000,
     "gst_rate": 12, "opening_stock": 20, "current_stock": 20, "min_stock": 5, "max_stock": 100,
     "warranty": "30 Years Performance", "description": "540W Bifacial Mono PERC, Dual Glass, 144 Cells"},

    # ── Solar Inverters ──
    {"name": "Growatt SPF 5000TL3-S", "sku": "INV-GR-5K", "barcode": "8901234560011", "hsn": "8504",
     "brand": "Growatt", "category": "Inverters", "unit": "Pcs", "purchase_price": 38000, "selling_price": 52000,
     "gst_rate": 18, "opening_stock": 15, "current_stock": 15, "min_stock": 3, "max_stock": 50,
     "warranty": "5 Years Standard", "description": "5KW Off-Grid Solar Inverter, MPPT 2x80A, 48V DC"},
    {"name": "Deye SUN-8K-SG03LP1", "sku": "INV-DY-8K", "barcode": "8901234560012", "hsn": "8504",
     "brand": "Deye", "category": "Inverters", "unit": "Pcs", "purchase_price": 52000, "selling_price": 72000,
     "gst_rate": 18, "opening_stock": 10, "current_stock": 10, "min_stock": 2, "max_stock": 30,
     "warranty": "5 Years", "description": "8KW Hybrid Solar Inverter, Dual MPPT, 48V"},
    {"name": "Luminous NXG Plus 1100", "sku": "INV-LU-1100", "barcode": "8901234560013", "hsn": "8504",
     "brand": "Luminous", "category": "Inverters", "unit": "Pcs", "purchase_price": 6500, "selling_price": 9200,
     "gst_rate": 18, "opening_stock": 25, "current_stock": 25, "min_stock": 5, "max_stock": 80,
     "warranty": "2 Years", "description": "1100VA Home UPS Inverter, 12V, Pure Sine Wave"},
    {"name": "Microtek MEB-1600VA", "sku": "INV-MK-1600", "barcode": "8901234560014", "hsn": "8504",
     "brand": "Microtek", "category": "Inverters", "unit": "Pcs", "purchase_price": 8500, "selling_price": 12000,
     "gst_rate": 18, "opening_stock": 20, "current_stock": 20, "min_stock": 5, "max_stock": 60,
     "warranty": "2 Years", "description": "1600VA Digital Home UPS, Intelligent Battery Management"},

    # ── Batteries ──
    {"name": "Exide Insta BIB 1500", "sku": "BAT-EX-1500", "barcode": "8901234560021", "hsn": "8507",
     "brand": "Exide", "category": "Batteries", "unit": "Pcs", "purchase_price": 12000, "selling_price": 16500,
     "gst_rate": 28, "opening_stock": 35, "current_stock": 35, "min_stock": 8, "max_stock": 100,
     "warranty": "36 Months", "description": "150Ah 12V Tubular Inverter Battery, 1500 Cycles"},
    {"name": "Amaron CR-I1500D04R", "sku": "BAT-AM-1500", "barcode": "8901234560022", "hsn": "8507",
     "brand": "Amaron", "category": "Batteries", "unit": "Pcs", "purchase_price": 11500, "selling_price": 15800,
     "gst_rate": 28, "opening_stock": 30, "current_stock": 30, "min_stock": 8, "max_stock": 100,
     "warranty": "36 Months", "description": "150Ah 12V High Performance VRLA Battery"},
    {"name": "Luminous RC 18000 150Ah", "sku": "BAT-LU-150", "barcode": "8901234560023", "hsn": "8507",
     "brand": "Luminous", "category": "Batteries", "unit": "Pcs", "purchase_price": 10800, "selling_price": 14500,
     "gst_rate": 28, "opening_stock": 40, "current_stock": 40, "min_stock": 10, "max_stock": 120,
     "warranty": "36 Months", "description": "150Ah 12V Tall Tubular Battery, Deep Cycle"},
    {"name": "Exide Solar XP 200Ah", "sku": "BAT-EX-XP200", "barcode": "8901234560024", "hsn": "8507",
     "brand": "Exide", "category": "Batteries", "unit": "Pcs", "purchase_price": 18000, "selling_price": 24500,
     "gst_rate": 28, "opening_stock": 15, "current_stock": 15, "min_stock": 5, "max_stock": 50,
     "warranty": "60 Months", "description": "200Ah 12V Solar Tubular Battery, 2500 Cycles"},

    # ── UPS ──
    {"name": "APC Smart-UPS SMT1000I", "sku": "UPS-APC-1K", "barcode": "8901234560031", "hsn": "8504",
     "brand": "APC", "category": "UPS", "unit": "Pcs", "purchase_price": 28000, "selling_price": 38000,
     "gst_rate": 18, "opening_stock": 12, "current_stock": 12, "min_stock": 3, "max_stock": 30,
     "warranty": "3 Years", "description": "1000VA Line-Interactive UPS, 230V, SmartConnect"},
    {"name": "Vertiv GXT5-1000MTBXL", "sku": "UPS-VT-1K", "barcode": "8901234560032", "hsn": "8504",
     "brand": "Vertiv", "category": "UPS", "unit": "Pcs", "purchase_price": 35000, "selling_price": 48000,
     "gst_rate": 18, "opening_stock": 8, "current_stock": 8, "min_stock": 2, "max_stock": 20,
     "warranty": "3 Years", "description": "1000VA Online UPS, Double Conversion, LCD Display"},
    {"name": "Microtek EM4160+ UPS", "sku": "UPS-MK-EM4160", "barcode": "8901234560033", "hsn": "8504",
     "brand": "Microtek", "category": "UPS", "unit": "Pcs", "purchase_price": 5500, "selling_price": 7800,
     "gst_rate": 18, "opening_stock": 20, "current_stock": 20, "min_stock": 5, "max_stock": 50,
     "warranty": "2 Years", "description": "600VA Offline UPS, 12V, Surge Protection"},

    # ── RO Systems ──
    {"name": "Kent Pearl RO+UV+UF 8L", "sku": "RO-KT-PEARL", "barcode": "8901234560041", "hsn": "8421",
     "brand": "Kent", "category": "RO Systems", "unit": "Pcs", "purchase_price": 14000, "selling_price": 19990,
     "gst_rate": 18, "opening_stock": 18, "current_stock": 18, "min_stock": 4, "max_stock": 40,
     "warranty": "1 Year Comprehensive", "description": "8L Wall-Mountable RO+UV+UF Water Purifier, TDS Controller"},
    {"name": "Aquaguard Aureus RO+UV", "sku": "RO-AG-AUREUS", "barcode": "8901234560042", "hsn": "8421",
     "brand": "Aquaguard", "category": "RO Systems", "unit": "Pcs", "purchase_price": 12000, "selling_price": 16499,
     "gst_rate": 18, "opening_stock": 15, "current_stock": 15, "min_stock": 4, "max_stock": 40,
     "warranty": "1 Year", "description": "7L RO+UV Water Purifier, 6-Stage Purification"},
    {"name": "Pureit Copper+ Mineral RO", "sku": "RO-PI-COPPER", "barcode": "8901234560043", "hsn": "8421",
     "brand": "Pureit", "category": "RO Systems", "unit": "Pcs", "purchase_price": 11000, "selling_price": 15999,
     "gst_rate": 18, "opening_stock": 12, "current_stock": 12, "min_stock": 3, "max_stock": 30,
     "warranty": "1 Year", "description": "8L Copper Mineral RO+UV+MF, 7 Stage Purification"},
    {"name": "AO Smith Z8 RO+UV 10L", "sku": "RO-AS-Z8", "barcode": "8901234560044", "hsn": "8421",
     "brand": "AO Smith", "category": "RO Systems", "unit": "Pcs", "purchase_price": 16000, "selling_price": 22999,
     "gst_rate": 18, "opening_stock": 8, "current_stock": 8, "min_stock": 2, "max_stock": 20,
     "warranty": "1 Year Comprehensive", "description": "10L RO+UV+Mineralizer, 8-Stage Advanced Purification"},

    # ── Hardware ──
    {"name": "Havells 4-Way Extension Board 25A", "sku": "HW-HV-4W25", "barcode": "8901234560051", "hsn": "8536",
     "brand": "Havells", "category": "Hardware", "unit": "Pcs", "purchase_price": 650, "selling_price": 950,
     "gst_rate": 18, "opening_stock": 60, "current_stock": 60, "min_stock": 15, "max_stock": 200,
     "warranty": "2 Years", "description": "4-Way Heavy Duty Extension Board, 4M Cord, Surge Protection"},
    {"name": "Anchor Roma Classic Switch", "sku": "HW-AN-ROMA", "barcode": "8901234560052", "hsn": "8536",
     "brand": "Anchor", "category": "Hardware", "unit": "Box", "purchase_price": 180, "selling_price": 260,
     "gst_rate": 18, "opening_stock": 100, "current_stock": 100, "min_stock": 20, "max_stock": 500,
     "warranty": "10 Years", "description": "Modular Switch Pack of 10, White"},
    {"name": "Finolex FR Cable 2.5 sq mm (90m)", "sku": "HW-FN-25FR", "barcode": "8901234560053", "hsn": "8544",
     "brand": "Finolex", "category": "Hardware", "unit": "Roll", "purchase_price": 2200, "selling_price": 3100,
     "gst_rate": 18, "opening_stock": 45, "current_stock": 45, "min_stock": 10, "max_stock": 150,
     "warranty": "15 Years", "description": "2.5 sq mm Flame Retardant Copper Cable, 90 meters"},
    {"name": "Polycab Industrial MCB 32A", "sku": "HW-PC-MCB32", "barcode": "8901234560054", "hsn": "8536",
     "brand": "Polycab", "category": "Hardware", "unit": "Pcs", "purchase_price": 320, "selling_price": 480,
     "gst_rate": 18, "opening_stock": 80, "current_stock": 80, "min_stock": 20, "max_stock": 300,
     "warranty": "5 Years", "description": "MCB 32A Single Pole, C-Curve, 10kA Breaking Capacity"},

    # ── Electrical ──
    {"name": "Crompton Greaves Fans Blanca 1200mm", "sku": "EL-CG-FAN", "barcode": "8901234560061", "hsn": "8414",
     "brand": "Crompton", "category": "Electrical", "unit": "Pcs", "purchase_price": 2800, "selling_price": 3990,
     "gst_rate": 18, "opening_stock": 25, "current_stock": 25, "min_stock": 5, "max_stock": 80,
     "warranty": "2 Years", "description": "1200mm Premium Ceiling Fan, BLDC Motor, Remote Control"},
    {"name": "Philips LED Bulb 12W Pack of 4", "sku": "EL-PH-LED12", "barcode": "8901234560062", "hsn": "9405",
     "brand": "Philips", "category": "Electrical", "unit": "Pack", "purchase_price": 350, "selling_price": 520,
     "gst_rate": 18, "opening_stock": 50, "current_stock": 50, "min_stock": 15, "max_stock": 200,
     "warranty": "2 Years", "description": "12W LED Bulbs Cool Daylight 6500K, Pack of 4"},
    {"name": "Syska 5m LED Strip Light RGB", "sku": "EL-SK-STRIP", "barcode": "8901234560063", "hsn": "9405",
     "brand": "Syska", "category": "Electrical", "unit": "Pcs", "purchase_price": 600, "selling_price": 950,
     "gst_rate": 18, "opening_stock": 35, "current_stock": 35, "min_stock": 10, "max_stock": 100,
     "warranty": "1 Year", "description": "5 Meter RGB LED Strip Light with Remote, 12V DC"},
    {"name": "Havells 1000W Immersion Water Heater", "sku": "EL-HV-IMH", "barcode": "8901234560064", "hsn": "8516",
     "brand": "Havells", "category": "Electrical", "unit": "Pcs", "purchase_price": 850, "selling_price": 1250,
     "gst_rate": 18, "opening_stock": 30, "current_stock": 30, "min_stock": 8, "max_stock": 80,
     "warranty": "2 Years", "description": "1000W Instant Immersion Rod Heater, ISI Marked, Shockproof"},
]


def seed():
    with app.app_context():
        existing_skus = {p.sku for p in Product.query.all()}
        added = 0
        skipped = 0

        # Ensure categories exist
        cat_names = set(p["category"] for p in PRODUCTS)
        categories = {}
        for cn in cat_names:
            cat = Category.query.filter_by(name=cn).first()
            if not cat:
                cat = Category(name=cn, description=f"{cn} products for GV Powers")
                db.session.add(cat)
                db.session.flush()
            categories[cn] = cat

        # Ensure a default supplier exists
        supplier = Supplier.query.filter_by(name="GV Powers Default Supplier").first()
        if not supplier:
            supplier = Supplier(
                name="GV Powers Default Supplier",
                contact_person="Purchase Manager",
                mobile="+91-9876543210",
                email="purchase@gvpowers.in",
                address="Bangalore, Karnataka",
                state="Karnataka",
                state_code=29,
                gstin="29BBBBB0000B1Z5",
            )
            db.session.add(supplier)
            db.session.flush()

        for p in PRODUCTS:
            if p["sku"] in existing_skus:
                skipped += 1
                continue
            product = Product(
                name=p["name"], sku=p["sku"], barcode=p["barcode"], hsn=p["hsn"],
                brand=p["brand"], category_id=categories[p["category"]].id,
                supplier_id=supplier.id, unit=p["unit"],
                purchase_price=p["purchase_price"], selling_price=p["selling_price"],
                gst_rate=p["gst_rate"], opening_stock=p["opening_stock"],
                current_stock=p["current_stock"], min_stock=p["min_stock"],
                max_stock=p["max_stock"], warranty=p["warranty"],
                description=p["description"], is_active=True,
            )
            db.session.add(product)
            existing_skus.add(p["sku"])
            added += 1

        db.session.commit()
        print(f"Done! Added {added} products, skipped {skipped} already existing.")


if __name__ == "__main__":
    seed()
