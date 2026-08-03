import json, re
from app import create_app, Invoice, Product, Customer, InvoiceItem
app = create_app(); app.testing = True
c = app.test_client()

def form_csrf(client, path):
    r = client.get(path); m=re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode())
    return m.group(1) if m else ''
def sess_csrf(client):
    with client.session_transaction() as s: return s['csrf_token']

r = c.get('/login'); 
print('login page', r.status_code)
tok = login=login_csrf=form_csrf(c,'/login')
print('admin login ->', c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':login_csrf}).status_code)

t = form_csrf(c,'/customers')
print('add customer ->', c.post('/customers/add', data={'name':'Suresh','mobile':'9840011223','email':'suresh@example.com','address':'Salem','state':'Tamil Nadu','state_code':'33','csrf_token':t}).status_code)
print('add product ->', c.post('/products/add', data={'name':'Solar Panel 550W','sku':'SOL-550','hsn':'85414300','category_id':'','unit':'pcs','purchase_price':'2000','selling_price':'2500','gst_rate':'18','stock_quantity':'10','min_stock':'1','csrf_token':t}).status_code)

with app.app_context():
    cust = Customer.query.order_by(Customer.id.desc()).first()
    prod = Product.query.order_by(Product.id.desc()).first()
c.get('/invoices/create'); jtok = form_csrf(c,'/invoices/create')
payload = {'customer_id':str(cust.id),'customer_name':cust.name,'customer_mobile':cust.mobile,'customer_email':cust.email,'customer_address':cust.address,'customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(prod.id),'product_name':prod.name,'sku':prod.sku,'hsn':prod.hsn,'qty':2,'price':2500,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
try:
    r = c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})
    print('INVOICE CREATE:', r.status_code, r.get_json())
except Exception as e:
    print('exception in test:', type(e).__name__, e)
with app.app_context():
    print('invoices in db:', Invoice.query.count())
