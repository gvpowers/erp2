import re
from app import create_app, Invoice, Product, Customer, StockMovement, db
app = create_app(); app.testing = True
c = app.test_client()
with app.app_context():
    for p in Product.query.filter(Product.sku.in_(['SOL-550'])).all():
        for m in StockMovement.query.filter_by(product_id=p.id).all():
            db.session.delete(m)
        db.session.delete(p)
    db.session.commit()
def form_csrf(p):
    r = c.get(p); m=re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode()); return m.group(1) if m else ''
def sess_csrf():
    with c.session_transaction() as s: return s['csrf_token']

print('admin login ->', c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':form_csrf('/login')}).status_code)
t = form_csrf('/customers')
print('add customer ->', c.post('/customers/add', data={'name':'Suresh','mobile':'9840011223','email':'suresh@example.com','address':'Salem','state':'Tamil Nadu','state_code':'33','csrf_token':t}).status_code)
print('add product ->', c.post('/products/add', data={'name':'Solar Panel 550W','sku':'SOL-550','hsn':'85414300','category_id':'','unit':'pcs','purchase_price':'2000','selling_price':'2500','gst_rate':'18','stock_quantity':'10','min_stock':'1','csrf_token':t}).status_code)

jtok = form_csrf('/invoices/create')
print('signed csrf token:', (jtok[:40] + '...') if jtok else None)
with app.app_context():
    cust = Customer.query.order_by(Customer.id.desc()).first()
    prod = Product.query.order_by(Product.id.desc()).first()
payload = {'customer_id':str(cust.id),'customer_name':cust.name,'customer_mobile':cust.mobile,'customer_email':cust.email,'customer_address':cust.address,'customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(prod.id),'product_name':prod.name,'sku':prod.sku,'hsn':prod.hsn,'qty':2,'price':2500,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
r = c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})
print('INVOICE CREATE status:', r.status_code, 'json:', r.get_json())
print('BODY:', r.data[:1200])
with app.app_context():
    inv = Invoice.query.order_by(Invoice.id.desc()).first()
    if inv:
        print('=> created', inv.invoice_number, 'grand_total', inv.grand_total, 'items', len(inv.items))
        print('   email link:', inv.customer_email)
