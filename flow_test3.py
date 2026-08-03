import re
from app import create_app, Invoice, Product, Customer, InvoiceItem, db
app = create_app(); app.testing = True
c = app.test_client()
def form_csrf(p):
    r = c.get(p); m=re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode()); return m.group(1) if m else ''
def sess_csrf():
    with c.session_transaction() as s: return s['csrf_token']

with app.app_context():
    for inv in Invoice.query.all():
        [db.session.delete(i) for i in inv.items]
        db.session.delete(inv)
    for p in Product.query.filter(Product.sku.like('SOL-T%')).all(): db.session.delete(p)
    for cu in Customer.query.filter(Customer.name.like('T-Suresh%')).all(): db.session.delete(cu)
    db.session.commit()
print('login ->', c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':form_csrf('/login')}).status_code)
t = form_csrf('/customers')
print('cust ->', c.post('/customers/add', data={'name':'T-Suresh','mobile':'9840011223','email':'suresh@example.com','address':'Salem','state':'Tamil Nadu','state_code':'33','csrf_token':t}).status_code)
print('prod ->', c.post('/products/add', data={'name':'T-Solar Panel 550W','sku':'SOL-T550','hsn':'85414300','category_id':'','unit':'pcs','purchase_price':'2000','selling_price':'2500','gst_rate':'18','stock_quantity':'10','min_stock':'1','csrf_token':t}).status_code)

c.get('/invoices/create'); jtok = sess_csrf()
with app.app_context():
    cust = Customer.query.order_by(Customer.id.desc()).first()
    prod = Product.query.order_by(Product.id.desc()).first()
payload = {'customer_id':str(cust.id),'customer_name':cust.name,'customer_mobile':cust.mobile,'customer_email':cust.email,'customer_address':cust.address,'customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(prod.id),'product_name':prod.name,'sku':prod.sku,'hsn':prod.hsn,'qty':2,'price':2500.0,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
r = c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})
print('INVOICE CREATE:', r.status_code, r.get_json())
with app.app_context():
    inv = Invoice.query.order_by(Invoice.id.desc()).first()
    if inv: print('=> invoice', inv.invoice_number, 'grand_total', inv.grand_total, 'items', len(inv.items), 'cust_email', inv.customer_email)
    print('=> view route:', c.get(f'/invoices/{inv.id}').status_code if inv else 'n/a')
