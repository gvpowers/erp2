"""Run with: python seed_data.py"""
import os, sys, random
from datetime import datetime, date, timedelta
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
os.environ['FLASK_ENV'] = 'development'

from app import create_app
app = create_app()

from app import db, User, Customer, Category, Product, Supplier
from app import Invoice, InvoiceItem, Quotation, QuotationItem
from app import PurchaseOrder, PurchaseItem, StockMovement, Settings

def seed():
    with app.app_context():
        if Customer.query.count() > 5:
            print("Data already exists, skipping seed.")
            update_settings()
            return

        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@gvpowers.in', full_name='Admin', role='admin', is_active=True)
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()

        staff = User.query.filter_by(username='staff1').first()
        if not staff:
            staff = User(username='staff1', email='staff@gvpowers.in', full_name='Staff User', role='staff', is_active=True)
            staff.set_password('Staff@123')
            db.session.add(staff)
            db.session.commit()

        cats = {}
        for cat_name in ['Solar Panels', 'UPS Systems', 'Inverters', 'RO Solutions', 'Electricals', 'Batteries', 'Accessories']:
            c = Category.query.filter_by(name=cat_name).first()
            if not c:
                c = Category(name=cat_name)
                db.session.add(c)
            cats[cat_name] = c
        db.session.commit()

        customers_data = [
            dict(name='Rajesh Kumar', mobile='9876543210', email='rajesh@email.com', address='123, MG Road, Indiranagar', state='Karnataka', state_code=29, gstin='29ABCDE1234F1Z5'),
            dict(name='Priya Sharma', mobile='9876543211', email='priya@email.com', address='45, Brigade Road, Bangalore', state='Karnataka', state_code=29, gstin='29FGHIJ5678K2L5'),
            dict(name='Amit Patel', mobile='9876543212', email='amit@email.com', address='78, Ellis Bridge, Ahmedabad', state='Gujarat', state_code=24, gstin='24MNOPQ9012R3S5'),
            dict(name='Sunil Rao', mobile='9876543213', email='sunil@email.com', address='Plot 56, Kharghar, Navi Mumbai', state='Maharashtra', state_code=27),
            dict(name='Ananya Gupta', mobile='9876543214', email='ananya@email.com', address='12/3, Civil Lines, Delhi', state='Delhi', state_code=7, gstin='07TUVWX3456Y4Z5'),
            dict(name='Vikram Singh', mobile='9876543215', email='vikram@email.com', address='88, Anna Nagar, Chennai', state='Tamil Nadu', state_code=33),
        ]
        customers = {}
        for cd in customers_data:
            c = Customer(**cd)
            db.session.add(c)
            customers[cd['name']] = c
        db.session.commit()

        suppliers_data = [
            dict(name='Tata Power Solar', contact_person='Rohan Desai', mobile='9988776651', email='rohan@tatapower.com', address='Mumbai, Maharashtra', state='Maharashtra', state_code=27, gstin='27ABCDE1234F1Z5', bank_name='HDFC Bank', bank_account='12345678901', bank_ifsc='HDFC0001234'),
            dict(name='Exide Industries Ltd', contact_person='Suresh Menon', mobile='9988776652', email='suresh@exide.com', address='Kolkata, West Bengal', state='West Bengal', state_code=19, gstin='19FGHIJ5678K2L5', bank_name='SBI', bank_account='98765432101', bank_ifsc='SBIN0001234'),
            dict(name='Luminous Power Tech', contact_person='Neha Gupta', mobile='9988776653', email='neha@luminous.com', address='Delhi NCR', state='Delhi', state_code=7, gstin='07MNOPQ9012R3S5', bank_name='ICICI Bank', bank_account='11122233301', bank_ifsc='ICIC0001234'),
            dict(name='Sukam Power Systems', contact_person='Deepak Jain', mobile='9988776654', email='deepak@sukam.com', address='Ahmedabad, Gujarat', state='Gujarat', state_code=24, gstin='24TUVWX3456Y4Z5', bank_name='Axis Bank', bank_account='44455566601', bank_ifsc='UTIB0001234'),
            dict(name='Havells India Ltd', contact_person='Amit Saxena', mobile='9988776655', email='amit@havells.com', address='Noida, UP', state='Uttar Pradesh', state_code=9, gstin='09ABCDE1234F1Z5', bank_name='PNB', bank_account='77788899901', bank_ifsc='PUNB0001234'),
        ]
        suppliers = {}
        for sd in suppliers_data:
            s = Supplier(**sd)
            db.session.add(s)
            suppliers[sd['name']] = s
        db.session.commit()

        products_data = [
            dict(name='Monocrystalline Solar Panel 330W', sku='SOL-MONO-330', hsn='85414300', brand='Tata Power Solar', category_id=cats['Solar Panels'].id, supplier_id=suppliers['Tata Power Solar'].id, unit='pcs', purchase_price=Decimal('12500'), selling_price=Decimal('16500'), gst_rate=5, stock_quantity=50, min_stock=5, max_stock=200, opening_stock=50, warehouse='Main Warehouse-A', warranty='25 Years'),
            dict(name='Polycrystalline Solar Panel 250W', sku='SOL-POLY-250', hsn='85414300', brand='Vikram Solar', category_id=cats['Solar Panels'].id, supplier_id=suppliers['Tata Power Solar'].id, unit='pcs', purchase_price=Decimal('8500'), selling_price=Decimal('11500'), gst_rate=5, stock_quantity=30, min_stock=5, max_stock=150, opening_stock=30, warehouse='Main Warehouse-A', warranty='25 Years'),
            dict(name='Solar Inverter 5kW', sku='INV-ON-5KW', hsn='85044030', brand='Luminous', category_id=cats['Inverters'].id, supplier_id=suppliers['Luminous Power Tech'].id, unit='pcs', purchase_price=Decimal('28000'), selling_price=Decimal('38000'), gst_rate=18, stock_quantity=15, min_stock=3, max_stock=50, opening_stock=15, warehouse='Main Warehouse-B', warranty='5 Years'),
            dict(name='Solar Inverter 3kW', sku='INV-OFF-3KW', hsn='85044030', brand='Sukam', category_id=cats['Inverters'].id, supplier_id=suppliers['Sukam Power Systems'].id, unit='pcs', purchase_price=Decimal('15000'), selling_price=Decimal('21000'), gst_rate=18, stock_quantity=20, min_stock=3, max_stock=50, opening_stock=20, warehouse='Main Warehouse-B', warranty='3 Years'),
            dict(name='UPS 1kVA Online', sku='UPS-1K-ON', hsn='85044020', brand='APC', category_id=cats['UPS Systems'].id, supplier_id=suppliers['Exide Industries Ltd'].id, unit='pcs', purchase_price=Decimal('9500'), selling_price=Decimal('13500'), gst_rate=18, stock_quantity=25, min_stock=5, max_stock=80, opening_stock=25, warehouse='Main Warehouse-C', warranty='2 Years'),
            dict(name='UPS 2kVA Online', sku='UPS-2K-ON', hsn='85044020', brand='APC', category_id=cats['UPS Systems'].id, supplier_id=suppliers['Exide Industries Ltd'].id, unit='pcs', purchase_price=Decimal('16000'), selling_price=Decimal('22500'), gst_rate=18, stock_quantity=12, min_stock=3, max_stock=40, opening_stock=12, warehouse='Main Warehouse-C', warranty='2 Years'),
            dict(name='Tubular Battery 150Ah', sku='BAT-TUB-150', hsn='85072000', brand='Exide', category_id=cats['Batteries'].id, supplier_id=suppliers['Exide Industries Ltd'].id, unit='pcs', purchase_price=Decimal('11000'), selling_price=Decimal('15500'), gst_rate=18, stock_quantity=40, min_stock=10, max_stock=100, opening_stock=40, warehouse='Battery Store', warranty='5 Years'),
            dict(name='Tubular Battery 200Ah', sku='BAT-TUB-200', hsn='85072000', brand='Exide', category_id=cats['Batteries'].id, supplier_id=suppliers['Exide Industries Ltd'].id, unit='pcs', purchase_price=Decimal('14000'), selling_price=Decimal('19500'), gst_rate=18, stock_quantity=25, min_stock=5, max_stock=60, opening_stock=25, warehouse='Battery Store', warranty='5 Years'),
            dict(name='Lithium Battery 100Ah', sku='BAT-LI-100', hsn='85076000', brand='Luminous', category_id=cats['Batteries'].id, supplier_id=suppliers['Luminous Power Tech'].id, unit='pcs', purchase_price=Decimal('32000'), selling_price=Decimal('45000'), gst_rate=18, stock_quantity=8, min_stock=2, max_stock=30, opening_stock=8, warehouse='Battery Store', warranty='7 Years'),
            dict(name='RO System 100 GPD', sku='RO-100GPD', hsn='84212100', brand='Havells', category_id=cats['RO Solutions'].id, supplier_id=suppliers['Havells India Ltd'].id, unit='pcs', purchase_price=Decimal('8500'), selling_price=Decimal('12000'), gst_rate=18, stock_quantity=18, min_stock=5, max_stock=50, opening_stock=18, warehouse='Main Warehouse-A', warranty='2 Years'),
            dict(name='RO System 200 GPD', sku='RO-200GPD', hsn='84212100', brand='Kent', category_id=cats['RO Solutions'].id, supplier_id=suppliers['Havells India Ltd'].id, unit='pcs', purchase_price=Decimal('14000'), selling_price=Decimal('19500'), gst_rate=18, stock_quantity=10, min_stock=3, max_stock=30, opening_stock=10, warehouse='Main Warehouse-A', warranty='3 Years'),
            dict(name='MC4 Connectors Pair', sku='ACC-MC4', hsn='85369090', brand='Staubli', category_id=cats['Accessories'].id, supplier_id=suppliers['Havells India Ltd'].id, unit='pair', purchase_price=Decimal('250'), selling_price=Decimal('450'), gst_rate=18, stock_quantity=200, min_stock=20, max_stock=500, opening_stock=200, warehouse='Accessories Store', warranty='1 Year'),
            dict(name='Solar Cable 4mm 50m Roll', sku='CBL-SOL-4MM', hsn='85444920', brand='Polycab', category_id=cats['Electricals'].id, supplier_id=suppliers['Havells India Ltd'].id, unit='roll', purchase_price=Decimal('1800'), selling_price=Decimal('2800'), gst_rate=18, stock_quantity=30, min_stock=5, max_stock=80, opening_stock=30, warehouse='Electricals Store'),
            dict(name='AC Distribution Box SPN', sku='ELEC-DB-SPN', hsn='85371000', brand='Legrand', category_id=cats['Electricals'].id, supplier_id=suppliers['Havells India Ltd'].id, unit='pcs', purchase_price=Decimal('1200'), selling_price=Decimal('1900'), gst_rate=18, stock_quantity=45, min_stock=5, max_stock=100, opening_stock=45, warehouse='Electricals Store'),
            dict(name='Solar Charge Controller 60A', sku='SOL-CC-60A', hsn='85044030', brand='Sukam', category_id=cats['Solar Panels'].id, supplier_id=suppliers['Sukam Power Systems'].id, unit='pcs', purchase_price=Decimal('6500'), selling_price=Decimal('9500'), gst_rate=5, stock_quantity=12, min_stock=3, max_stock=30, opening_stock=12, warehouse='Main Warehouse-B', warranty='3 Years'),
        ]
        products = {}
        for pd in products_data:
            p = Product(**pd)
            db.session.add(p)
            products[pd['name']] = p
        db.session.commit()

        today = date.today()
        def invno(d, n): return f"INV-{d.strftime('%d%m%Y')}-{n:03d}"
        def qtnno(d, n): return f"QTN-{d.strftime('%d%m%Y')}-{n:03d}"
        def pono(d, n): return f"PO-{d.strftime('%d%m%Y')}-{n:03d}"

        d1 = today - timedelta(days=5)
        inv1 = Invoice(invoice_number=invno(d1, 1), customer_id=customers['Rajesh Kumar'].id, customer_name='Rajesh Kumar', customer_mobile='9876543210', customer_email='rajesh@email.com', customer_address='123, MG Road, Indiranagar', customer_gstin='29ABCDE1234F1Z5', customer_state='Karnataka', customer_state_code=29, invoice_date=d1, subtotal=Decimal('64000'), total_discount=Decimal('500'), total_taxable=Decimal('63500'), total_cgst=Decimal('5715'), total_sgst=Decimal('5715'), round_off=Decimal('0.30'), grand_total=Decimal('74930'), amount_paid=Decimal('74930'), payment_method='UPI', status='completed', payment_status='paid', is_intra_state=True, notes='Solar panel installation for residence', created_by=admin.id)
        db.session.add(inv1)
        db.session.flush()
        for pid, qty, price, disc, gst in [
            (products['Monocrystalline Solar Panel 330W'].id, 2, Decimal('16500'), Decimal('0'), Decimal('5')),
            (products['Solar Inverter 5kW'].id, 1, Decimal('38000'), Decimal('500'), Decimal('18')),
            (products['Solar Charge Controller 60A'].id, 1, Decimal('9500'), Decimal('0'), Decimal('5')),
        ]:
            p = Product.query.get(pid)
            taxable = price * qty - Decimal(disc)
            cgst = sgst = (taxable * gst / Decimal('200')).quantize(Decimal('0.01'))
            total = taxable + cgst + sgst
            it = InvoiceItem(invoice_id=inv1.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, discount=disc, gst_rate=gst, taxable_value=taxable, cgst=cgst, sgst=sgst, igst=Decimal('0'), total=total)
            db.session.add(it)

        d2 = today - timedelta(days=2)
        inv2 = Invoice(invoice_number=invno(d2, 1), customer_id=customers['Priya Sharma'].id, customer_name='Priya Sharma', customer_mobile='9876543211', customer_email='priya@email.com', customer_address='45, Brigade Road, Bangalore', customer_state='Karnataka', customer_state_code=29, invoice_date=d2, subtotal=Decimal('57500'), total_discount=Decimal('0'), total_taxable=Decimal('57500'), total_cgst=Decimal('5175'), total_sgst=Decimal('5175'), round_off=Decimal('0'), grand_total=Decimal('67850'), amount_paid=Decimal('30000'), payment_method='Bank Transfer', status='completed', payment_status='partial', is_intra_state=True, notes='Office UPS installation', created_by=admin.id)
        db.session.add(inv2)
        db.session.flush()
        for pid, qty, price, disc, gst in [
            (products['UPS 2kVA Online'].id, 2, Decimal('22500'), Decimal('0'), Decimal('18')),
            (products['Tubular Battery 150Ah'].id, 1, Decimal('15500'), Decimal('0'), Decimal('18')),
        ]:
            p = Product.query.get(pid)
            taxable = price * qty - Decimal(disc)
            cgst = sgst = (taxable * gst / Decimal('200')).quantize(Decimal('0.01'))
            total = taxable + cgst + sgst
            it = InvoiceItem(invoice_id=inv2.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, discount=disc, gst_rate=gst, taxable_value=taxable, cgst=cgst, sgst=sgst, igst=Decimal('0'), total=total)
            db.session.add(it)

        d3 = today - timedelta(days=10)
        inv3 = Invoice(invoice_number=invno(d3, 1), customer_id=customers['Amit Patel'].id, customer_name='Amit Patel', customer_mobile='9876543212', customer_email='amit@email.com', customer_address='78, Ellis Bridge, Ahmedabad', customer_gstin='24MNOPQ9012R3S5', customer_state='Gujarat', customer_state_code=24, invoice_date=d3, subtotal=Decimal('35000'), total_discount=Decimal('1000'), total_taxable=Decimal('34000'), total_cgst=Decimal('0'), total_sgst=Decimal('0'), total_igst=Decimal('6120'), round_off=Decimal('0'), grand_total=Decimal('40120'), amount_paid=Decimal('0'), payment_method='', status='completed', payment_status='pending', is_intra_state=False, notes='RO system for office - interstate supply', created_by=staff.id)
        db.session.add(inv3)
        db.session.flush()
        for pid, qty, price, disc, gst in [
            (products['RO System 200 GPD'].id, 1, Decimal('19500'), Decimal('500'), Decimal('18')),
            (products['RO System 100 GPD'].id, 1, Decimal('12000'), Decimal('500'), Decimal('18')),
            (products['Solar Cable 4mm 50m Roll'].id, 1, Decimal('2800'), Decimal('0'), Decimal('18')),
        ]:
            p = Product.query.get(pid)
            taxable = price * qty - Decimal(disc)
            igst = (taxable * gst / Decimal('100')).quantize(Decimal('0.01'))
            total = taxable + igst
            it = InvoiceItem(invoice_id=inv3.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, discount=disc, gst_rate=gst, taxable_value=taxable, cgst=Decimal('0'), sgst=Decimal('0'), igst=igst, total=total)
            db.session.add(it)
        db.session.commit()

        qd1 = today - timedelta(days=1)
        q1 = Quotation(quotation_number=qtnno(qd1, 1), customer_id=customers['Vikram Singh'].id, customer_name='Vikram Singh', customer_mobile='9876543215', customer_address='88, Anna Nagar, Chennai', customer_state='Tamil Nadu', customer_state_code=33, quotation_date=qd1, valid_until=today + timedelta(days=15), subtotal=Decimal('72000'), total_discount=Decimal('2000'), total_taxable=Decimal('70000'), total_cgst=Decimal('0'), total_sgst=Decimal('0'), total_igst=Decimal('12600'), grand_total=Decimal('82600'), is_intra_state=False, notes='Complete solar setup for residence', status='sent', created_by=admin.id)
        db.session.add(q1)
        db.session.flush()
        for pid, qty, price, disc, gst in [
            (products['Monocrystalline Solar Panel 330W'].id, 3, Decimal('16500'), Decimal('1000'), Decimal('5')),
            (products['Solar Inverter 5kW'].id, 1, Decimal('38000'), Decimal('1000'), Decimal('18')),
            (products['Tubular Battery 200Ah'].id, 1, Decimal('19500'), Decimal('0'), Decimal('18')),
        ]:
            p = Product.query.get(pid)
            taxable = price * qty - Decimal(disc)
            igst = (taxable * gst / Decimal('100')).quantize(Decimal('0.01'))
            total = taxable + igst
            it = QuotationItem(quotation_id=q1.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, discount=disc, gst_rate=gst, taxable_value=taxable, cgst=Decimal('0'), sgst=Decimal('0'), igst=igst, total=total)
            db.session.add(it)

        q2 = Quotation(quotation_number=qtnno(today, 1), customer_id=customers['Ananya Gupta'].id, customer_name='Ananya Gupta', customer_mobile='9876543214', customer_address='12/3, Civil Lines, Delhi', customer_gstin='07TUVWX3456Y4Z5', customer_state='Delhi', customer_state_code=7, quotation_date=today, valid_until=today + timedelta(days=20), subtotal=Decimal('15500'), total_discount=Decimal('0'), total_taxable=Decimal('15500'), total_cgst=Decimal('1395'), total_sgst=Decimal('1395'), grand_total=Decimal('18290'), is_intra_state=True, notes='UPS battery replacement', status='draft', created_by=staff.id)
        db.session.add(q2)
        db.session.flush()
        for pid, qty, price, disc, gst in [
            (products['Tubular Battery 150Ah'].id, 1, Decimal('15500'), Decimal('0'), Decimal('18')),
        ]:
            p = Product.query.get(pid)
            taxable = price * qty - Decimal(disc)
            cgst = sgst = (taxable * gst / Decimal('200')).quantize(Decimal('0.01'))
            total = taxable + cgst + sgst
            it = QuotationItem(quotation_id=q2.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, discount=disc, gst_rate=gst, taxable_value=taxable, cgst=cgst, sgst=sgst, igst=Decimal('0'), total=total)
            db.session.add(it)
        db.session.commit()

        pod = today - timedelta(days=15)
        po1 = PurchaseOrder(po_number=pono(pod, 1), supplier_id=suppliers['Tata Power Solar'].id, supplier_name='Tata Power Solar', order_date=pod, expected_date=today + timedelta(days=10), subtotal=Decimal('375000'), total_tax=Decimal('18750'), grand_total=Decimal('393750'), status='confirmed', notes='Bulk order for upcoming project', created_by=admin.id)
        db.session.add(po1)
        db.session.flush()
        for pid, qty, price, gst in [
            (products['Monocrystalline Solar Panel 330W'].id, 20, Decimal('12500'), Decimal('5')),
            (products['Solar Charge Controller 60A'].id, 10, Decimal('6500'), Decimal('5')),
        ]:
            p = Product.query.get(pid)
            total = price * qty * (1 + gst / Decimal('100'))
            it = PurchaseItem(purchase_order_id=po1.id, product_id=pid, product_name=p.name, hsn=p.hsn, qty=qty, unit=p.unit, price=price, gst_rate=gst, total=total)
            db.session.add(it)
        db.session.commit()

        sm1 = StockMovement(product_id=products['Monocrystalline Solar Panel 330W'].id, movement_type='purchase', quantity=50, reference_type='opening', notes='Opening stock', user_id=admin.id)
        sm2 = StockMovement(product_id=products['Tubular Battery 150Ah'].id, movement_type='sale', quantity=-2, reference_type='invoice', reference_id=inv2.id, notes='Sold via invoice INV-2025-0002', user_id=admin.id)
        db.session.add(sm1); db.session.add(sm2)
        db.session.commit()

        settings_data = dict(
            company_name='GV Powers & Energy Solutions',
            company_gstin='29ABCDE1234F1Z5',
            company_state='Karnataka',
            company_state_code='29',
            company_address='Plot 42, KIADB Industrial Area, Doddaballapur, Bangalore - 561203',
            company_phone='+91-80-28461234',
            company_email='gvpowerssalem@gmail.com',
            company_website='https://gvpowers.in',
            bank_name='HDFC Bank',
            bank_account='50100234567890',
            bank_ifsc='HDFC0004321',
            upi_id='gvpowers@hdfcbank',
            default_state_29='Karnataka',
            default_state_27='Maharashtra',
            default_state_33='Tamil Nadu',
            default_state_7='Delhi',
            default_state_24='Gujarat',
            default_state_8='Rajasthan',
            default_state_9='Uttar Pradesh',
            default_state_19='West Bengal',
        )
        for k, v in settings_data.items():
            existing = Settings.query.filter_by(key=k).first()
            if not existing:
                db.session.add(Settings(key=k, value=v))
        db.session.commit()

        print("Settings updated/added successfully!")
        print(f"  Customers: {Customer.query.count()}")
        print(f"  Suppliers: {Supplier.query.count()}")
        print(f"  Products: {Product.query.count()}")
        print(f"  Invoices: {Invoice.query.count()}")
        print(f"  Quotations: {Quotation.query.count()}")
        print(f"  Purchase Orders: {PurchaseOrder.query.count()}")
        print(f"  Stock Movements: {StockMovement.query.count()}")


def update_settings():
    pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--smtp':
        update_settings()
    else:
        seed()
