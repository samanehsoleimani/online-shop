from flask import Blueprint, render_template, request, session, abort, url_for
from werkzeug.utils import redirect
import os
import config

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

@admin.route('/admin/dashboard/products', methods=['GET'])
def products():
    return render_template('products.html')