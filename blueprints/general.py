from flask import Blueprint, render_template, request

from models.product import Product
from models.category import Category

app = Blueprint("app", __name__)


@app.route('/')
def home():

    search = request.args.get('search', None)

    query = Product.query.filter(
        Product.active == 1
    )

    if search:
        query = query.filter(
            Product.name.like(f'%{search}%')
        )

    products = query.all()

    categories = Category.query.all()

    return render_template(
        "main.html",
        products=products,
        categories=categories
    )



@app.route('/category/<int:id>')
def category(id):

    category = Category.query.filter(
        Category.id == id
    ).first_or_404()

    products = Product.query.filter(
        Product.category_id == category.id,
        Product.active == 1
    ).all()

    return render_template(
        "category.html",
        category=category,
        products=products
    )


@app.route('/product/<int:id>/<name>')
def product(id, name):

    product = Product.query.filter(
        Product.id == id
    ).filter(
        Product.name == name
    ).filter(
        Product.active == 1
    ).first_or_404()

    return render_template(
        "product.html",
        product=product
    )


@app.route('/about')
def about():
    return render_template("/about.html")