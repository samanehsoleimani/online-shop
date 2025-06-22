from os import abort

from click import password_option
from flask import Blueprint, render_template, request, session,abort
import os

from werkzeug.utils import redirect

import config

admin = Blueprint(
    'admin',
    __name__,
    template_folder=os.path.join('templates', 'admin')  # مسیر قالب های این بلوپرینت
)

@admin.route('/admin/login' , methods=['GET','POST'])
def login():
    if request.method == "POST":
         username=request.form.get('username',None)
         password=request.form.get('password',None)

         if username==config.ADMIN_USERNAME and password==config.ADMIN_PASSWORD:
             session['admin_login']=username
             return  redirect("/admin/dashboard")
         else:
             return redirect("/admin/login")

    else:
        return render_template('login.html')  # فقط نام فایل، چون مسیر رو دادیم در بلوپرینت



@admin.route('/admin/dashboard', methods=['GET'])
def dashboard():
    if session.get('admin_login') is None:
        abort(403)
    return "dashboard.html"
