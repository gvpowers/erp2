import re
from decimal import Decimal
from app import create_app, db, Product, Customer, Supplier, Invoice, PurchaseOrder, StockMovement

app = create_app(); app.testing = True
c = app.test_client()

def form_csrf(path):
    r = c.get(path); m = re.search(r'name="csrf_token" value="([^"]+)"', r.data.decode())
    return m.group(1) if m else ''

with app.app_context():
    for sm in StockMovement.query.all(): db.session.delete(sm)
    for po in PurchaseOrder.query.all():
        [db.session.delete(i) for i in po.items]
        db.session.delete(po)
    for p in Product.query.filter(Product.sku.like('SOL-ST%')).all(): db.session.delete(p)
    for cu in Customer.query.filter(Customer.name.like('ST-%')).all(): db.session.delete(cu)
    for su in Supplier.query.filter(Supplier.name.like('ST-%')).all(): db.session.delete(su)
    db.session.commit()

ok = []
def check(label, cond, extra=''):
    ok.append(bool(cond))
    print(('PASS' if cond else 'FAIL'), '-', label, extra)

print('login ->', c.post('/login', data={'username':'gvpowers@admin','password':'admin@gvpowerssalem','csrf_token':form_csrf('/login')}).status_code)

t = form_csrf('/suppliers')
print('add supplier ->', c.post('/suppliers/add', data={'name':'ST-Supplier','contact_person':'','mobile':'9880077665','email':'st@example.com','address':'Salem','state':'Tamil Nadu','state_code':'33','csrf_token':t}).status_code)

t = form_csrf('/products')
r = c.post('/products/add', data={'name':'ST-Solar Panel','sku':'SOL-ST1','hsn':'85414300','category_id':'','unit':'pcs','purchase_price':'2000','selling_price':'2500','gst_rate':'18','stock_quantity':'10','min_stock':'2','csrf_token':t})
print('add product ->', r.status_code, r.headers.get('Location'))

with app.app_context():
    p = Product.query.filter_by(sku='SOL-ST1').first()
    su = Supplier.query.filter_by(name='ST-Supplier').first()
    pid, sup_id = p.id, su.id
check('product created with stock 10', p and p.stock_quantity == 10)

c.get(f'/products/{pid}')
t = form_csrf(f'/products/{pid}')
print('add stock 5 ->', c.post(f'/products/{pid}/stock/add', data={'quantity':'5','csrf_token':t}).status_code)
with app.app_context():
    p = db.session.get(Product, pid)
check('stock 10+5=15', p.stock_quantity == 15, f'(got {p.stock_quantity})')

t = form_csrf(f'/products/{pid}')
print('remove stock 3 ->', c.post(f'/products/{pid}/stock/remove', data={'quantity':'3','reason':'damage','csrf_token':t}).status_code)
with app.app_context():
    p = db.session.get(Product, pid)
check('stock 15-3=12', p.stock_quantity == 12, f'(got {p.stock_quantity})')

t = form_csrf(f'/products/{pid}')
print('delete stock ->', c.post(f'/products/{pid}/stock/delete', data={'confirm_delete':'DELETE','csrf_token':t}).status_code)
with app.app_context():
    p = db.session.get(Product, pid)
check('stock reset to 0', p.stock_quantity == 0, f'(got {p.stock_quantity})')

t = form_csrf(f'/products/{pid}')
print('re-add stock 10 ->', c.post(f'/products/{pid}/stock/add', data={'quantity':'10','csrf_token':t}).status_code)

c.get('/invoices/create'); jtok = form_csrf('/invoices/create')
def invoice(payload):
    return c.post('/invoices/create', json=payload, headers={'X-CSRFToken':jtok,'X-Requested-With':'XMLHttpRequest'})

with app.app_context():
    p = db.session.get(Product, pid)
    cu = Customer.query.order_by(Customer.id.desc()).first()
    cid = cu.id
payload = {'customer_id':str(cid),'customer_name':'ST-Buyer','customer_mobile':'9840011223','customer_email':'stbuyer@example.com','customer_address':'Salem','customer_state':'Tamil Nadu','customer_state_code':'33','customer_gstin':'','invoice_type':'sales','notes':'','items':[{'product_id':str(pid),'product_name':p.name,'sku':p.sku,'hsn':p.hsn,'qty':2,'price':2500,'discount_type':'percent','discount_value':0,'gst_rate':18}]}
r = invoice(payload)
check('invoice qty2 (in stock) -> 200', r.status_code == 200, r.get_json() and str(r.get_json()))
with app.app_context():
    p = db.session.get(Product, pid)
    sale_mv = [m for m in StockMovement.query.filter_by(product_id=pid).all() if m.movement_type == 'sale']
check('stock 10-2=8 after sale', p.stock_quantity == 8, f'(got {p.stock_quantity})')
check('sale movement recorded', len(sale_mv) == 1, f'({len(sale_mv)} sale movements)')
check('last_sale set', p.last_sale is not None)

bad = dict(payload); bad['items'] = [dict(i, qty=999) for i in payload['items']]
r = invoice(bad)
check('invoice qty999 WITHOUT override -> 400', r.status_code == 400)
with app.app_context():
    p = db.session.get(Product, pid)
check('stock still 8 after blocked sale', p.stock_quantity == 8, f'(got {p.stock_quantity})')

over = dict(payload); over['allow_out_of_stock'] = True; over['items'] = [dict(i, qty=20) for i in payload['items']]
r = invoice(over)
check('invoice qty20 WITH override -> 200', r.status_code == 200, r.get_json() and str(r.get_json()))
with app.app_context():
    p = db.session.get(Product, pid)
check('stock 8-20=-12 after override', p.stock_quantity == -12, f'(got {p.stock_quantity})')

t = form_csrf(f'/products/{pid}')
print('re-add stock 20 ->', c.post(f'/products/{pid}/stock/add', data={'quantity':'20','csrf_token':t}).status_code)
with app.app_context():
    p = db.session.get(Product, pid)
check('stock -12+20=8', p.stock_quantity == 8, f'(got {p.stock_quantity})')

t = form_csrf('/purchase-orders')
r = c.post('/purchase-orders/add', data={'supplier_id':str(sup_id),'order_date':'2026-08-03','expected_date':'','product_id[]':[str(pid)],'quantity[]':['20'],'price[]':['2000'],'notes':'','csrf_token':t})
print('create PO ->', r.status_code, r.headers.get('Location'))
loc = r.headers.get('Location') or ''
m = re.search(r'/purchase-orders/(\d+)', loc)
oid = int(m.group(1)) if m else None
with app.app_context():
    po = db.session.get(PurchaseOrder, oid) if oid else None
check('PO created (draft)', po is not None and po.status == 'draft', f'(status {po.status if po else None})')
check('PO subtotal=grand_total=40000', po and po.grand_total == Decimal('40000'), f'({po.grand_total if po else None})')

t = form_csrf(f'/purchase-orders/{oid}')
print('receive PO ->', c.post(f'/purchase-orders/{oid}/status', data={'status':'received','csrf_token':t}).status_code)
with app.app_context():
    p = db.session.get(Product, pid)
    po = db.session.get(PurchaseOrder, oid)
    po_mv = [m for m in StockMovement.query.filter_by(product_id=pid).all() if m.reference_type == 'purchase_order']
check('stock 8+20=28 after receive', p.stock_quantity == 28, f'(got {p.stock_quantity})')
check('PO status received', po.status == 'received')
check('PO receive movement recorded', len(po_mv) == 1, f'({len(po_mv)} movements)')
check('last_purchase set', p.last_purchase is not None)

with app.app_context():
    p = db.session.get(Product, pid)
    mv = StockMovement.query.filter_by(product_id=pid).order_by(StockMovement.created_at).all()
    types = [m.movement_type for m in mv]
print('movement types:', types)
check('movement history has opening/purchase/adjustment/reset/sale', all(k in types for k in ('opening','purchase','adjustment','reset','sale')))

check('products list 200', c.get('/products').status_code == 200)
check('product profile 200', c.get(f'/products/{pid}').status_code == 200)
check('purchase orders list 200', c.get('/purchase-orders').status_code == 200)
check('PO detail 200', c.get(f'/purchase-orders/{oid}').status_code == 200 if oid else False)

print()
print('SUMMARY:', sum(ok), '/', len(ok), 'checks passed')
