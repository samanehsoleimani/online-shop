from sqlalchemy import *
from extentions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    image = Column(String, nullable=True)

    products = db.relationship(
        "Product",
        back_populates="category"
    )
