import re
from app import create_app, Invoice, Product, Customer
app = create_app(); app.testing = True
c = app.test_client()
def form_csrf(p):
    r = c.get(p); m=re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode()); return m.group(1) if m else ''
def sess_csrf():
    with c.session_transaction() as s: return s['csrf_token']

c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':form_csrf('/login')})
c.get('/invoices/create'); jtok = sess_csrf()
with app.app_context():
    cust = Customer.query.order_by(Customer.id.desc()).first()
    prod = Product.query.order_by(Product.id.desc()).first()
payload = {'customer_id':str(cust.id),'customer_name':cust.name,'customer_mobile':cust.mobile,'customer_email':cust.email,'customer_address':cust.address,'customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(prod.id),'product_name':prod.name,'sku':prod.sku,'hsn':prod.hsn,'qty':2,'price':2500,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
r = c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})
print('status', r.status_code)
print('content-type', r.headers.get('Content-Type'))
print('BODY:', r.data[:800])
