"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma

@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    products = db(db.product).select()
    return dict(products=products)

@action('myProduct')
@action.uses(db, auth.user, 'myProduct.html')
def my_product():
    products = db(db.product.created_by == get_user_email()).select()
    return dict(products=products)


@action('addProduct', method=["GET", "POST"])
@action.uses(db, session,auth.user, 'addProduct.html')
def add_product():
    form = Form(db.product, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('editProduct/<product_id:int>', method=['GET', 'POST'])
@action.uses(db, session, auth.user, 'editProduct.html')
def edit_product(product_id):
    p = db.product[product_id]
    if not p:
        redirect(URL('myProduct'))
    form = Form(db.product, record=p, csrf_session=session, formstyle=FormStyleBulma)
    return dict(form=form)

@action('product/<product_id:int>', method=['GET'])
@action.uses(db, session, auth.user, 'product.html')
def get_product(product_id):
    p = db.product[product_id]
    if not p:
        redirect(URL('index'))
    return dict(p=p)

@action('buy/<product_id:int>', method=['GET', 'POST'])
@action.uses(db, session, auth.user, 'buy.html')
def buy(product_id):
    p = db.product[product_id]
    if not p:
        redirect(URL('index'))
    form = Form(db.order, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)
@action('myOrder', method=['GET'])
@action.uses(db, session, auth.user, 'myOrder.html')
def my_order():
    orders = db(db.order.buyer == get_user_email()).select()
    return dict(orders=orders)

@action('search', method=['GET'])
@action.uses(db, session, auth.user, 'index.html')
def search():
    key = request.GET.get('key')
    products = []
    all = db(db.product).select()
    for p in all:
        if key in p.name:
            products.append(p)
    return dict(products=products)