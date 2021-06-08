"""
This file defines the database models
"""

from .common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#
def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None




db.define_table(
    'product',
    Field('name', length=100, requires=IS_NOT_EMPTY()),
    Field('price', 'float', default=0., requires=IS_FLOAT_IN_RANGE(0, 1e6)),
    Field('quantity', 'integer', default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field('unit', default='$', required=True),
    Field('desc', 'text'),
    Field('image', 'upload', uploadfolder='apps/EZbuy/static/product_image'),
    Field('created_by', default=get_user_email)
)

db.product.created_by.readable = db.product.created_by.writable = False

db.define_table(
    'order',
    Field('email', length=100, requires=IS_NOT_EMPTY()),
    Field('card', length=100, requires=IS_NOT_EMPTY()),
    Field('password', length=30, requires=IS_NOT_EMPTY()),
    Field('product_id', 'reference product', requires=IS_NOT_EMPTY()),
    Field('buyer', default=get_user_email)
)
db.order.buyer.readable=db.order.buyer.writable = False

db.commit()


