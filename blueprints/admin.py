from pydoc import describe

from flask import Blueprint, render_template, request, session, abort, url_for
from werkzeug.utils import redirect
import os
import config
from models.cart import Cart
from models.product import Product
from models.category import Category
from extentions import db
admin = Blueprint(
    'admin',
    __name__,
    template_folder=os.path.join('templates', 'admin')
)

@admin.before_request
def before_request():
    if session.get('admin_login', None) == None and request.endpoint !='admin.login':
        abort(403)

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_login'] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")

    return render_template('login.html')

@admin.route('/admin/dashboard', methods=['GET'])
def dashboard():
    cart=Cart.query.filter(Cart.status != 'pending').all()
    return render_template('dashboard.html',cart=cart)

@admin.route('/admin/dashboard/order/<id>', methods=['GET','POST'])
def order(id):
    cart = Cart.query.filter(Cart.id == id).first_or_404()

    if request.method=="GET":
        return render_template('order.html',cart=cart)
    else:
        status = request.form.get('status')
        cart.status=status
        db.session.commit()
        return redirect(url_for('admin.order', id=id))

@admin.route('/admin/dashboard/products', methods=['GET', 'POST'])
def products():

    if request.method == "GET":
        products = Product.query.all()
        categories = Category.query.all()

        return render_template(
            'products.html',
            products=products,
            categories=categories
        )

    else:
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        active = request.form.get('active')
        category_id = request.form.get('category_id')
        file = request.files.get('cover')

        p = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id
        )

        if active is None:
            p.active = 0
        else:
            p.active = 1

        db.session.add(p)
        db.session.commit()

        if file:
            file.save(f'static/cover/{p.id}.jpg')

        return "done"
@admin.route('/admin/dashboard/edit-product/<id>', methods=['GET', 'POST'])
def edit_product(id):

    product = Product.query.filter(Product.id == id).first_or_404()

    if request.method == "GET":
        categories = Category.query.all()

        return render_template(
            "edit-product.html",
            product=product,
            categories=categories
        )

    else:
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        active = request.form.get('active')
        category_id = request.form.get('category_id')
        file = request.files.get('cover')

        product.name = name
        product.description = description
        product.price = price
        product.category_id = category_id

        if active is None:
            product.active = 0
        else:
            product.active = 1

        db.session.commit()

        if file:
            file.save(f'static/cover/{product.id}.jpg')

        return redirect(
            url_for("admin.edit_product", id=id)
        )