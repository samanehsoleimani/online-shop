from sqlalchemy import *
from sqlalchemy.orm import backref

from extentions import db, get_current_time


class Payment(db.Model):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    status = Column(String, default="pending")
    token = Column(String)
    price= Column(Integer)
    date_created = Column(String(15),default=get_current_time)
    cart = db.relationship("Cart", backref="payments")

