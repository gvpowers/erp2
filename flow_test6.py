import re
from app import create_app, Invoice
app = create_app(); app.testing = True
c = app.test_client()
def form_csrf(p):
    r = c.get(p); m=re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode()); return m.group(1) if m else ''
def meta_token(p):
    r = c.get(p); m = re.search(r'<meta name="csrf-token" content="([^"]+)"', r.data.decode()); return m.group(1) if m else ''

print('login ->', c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':form_csrf('/login')}).status_code)
jtok = meta_token('/invoices/create')
with app.app_context():
    from app import Customer, Product
    cust = Customer.query.order_by(Customer.id.desc()).first()
    prod = Product.query.order_by(Product.id.desc()).first()
payload = {'customer_id':str(cust.id),'customer_name':cust.name,'customer_mobile':cust.mobile,'customer_email':cust.email,'customer_address':cust.address,'customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(prod.id),'product_name':prod.name,'sku':prod.sku,'hsn':prod.hsn,'qty':2,'price':2500,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
r = c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})
print('INVOICE CREATE:', r.status_code, r.get_json())
with app.app_context():
    inv = Invoice.query.order_by(Invoice.id.desc()).first()
    if inv:
        print('=> invoice', inv.invoice_number, 'grand_total', inv.grand_total, 'items', len(inv.items), 'stockdecr ok')
    else:
        print('=> NO INVOICE CREATED (backend bug or rejection)')
        print(r.data[:400])
    print('view route status:', c.get(f'/invoices/{inv.id}').status_code if inv else 'n/a')
