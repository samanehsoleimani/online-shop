from pydoc import describe

from flask import Blueprint, render_template, request, session, abort, url_for
from werkzeug.utils import redirect
import os
import config
from models.product import Product
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
    return render_template('dashboard.html')

@admin.route('/admin/dashboard/products', methods=['GET' ,'POST'])
def products():
    if request.method == "GET":
        products=Product.query.all()
        return render_template('products.html',products=products)
    else:
        name = request.form.get('name',None)
        price = request.form.get('price',None)
        description = request.form.get('description',None)
        active =request.form.get('active',None)

        p = Product( name=name ,description=description,price=price)
        if active == None:
            p.active = 0
        else:
             p.active = 1
        db.session.add(p)
        db.session.commit()

        return "done"
