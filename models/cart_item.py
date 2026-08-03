from sqlalchemy import *
from sqlalchemy.orm import backref

from extentions import db


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price=Column(Integer)
    quantity =Column(Integer)

    product = db.relationship("Product", backref=backref("cart_items",lazy="dynamic"))
    cart = db.relationship("Cart", backref=backref("cart_items",lazy="dynamic"))
