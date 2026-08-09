from itertools import product
from re import search

import requests
from flask import Blueprint, render_template, request
from models.product import Product

app = Blueprint("app" ,__name__)


@app.route('/')
def home():
    search = request.args.get('search', None)
    query = Product.query.filter(Product.active == 1)

    if search:
        query = query.filter(Product.name.like(f'%{search}%'))
    products = query.all()

    return render_template("main.html", products=products)


@app.route('/product/<int:id>/<name>')
def product(id, name):
    product = Product.query.filter(Product.id == id ).filter(Product.name == name).filter(Product.active==1).first_or_404()
    return render_template("product.html" , product=product)
@app.route('/about')
def about():
    return render_template("/about.html")
