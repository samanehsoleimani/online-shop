from flask import Blueprint, render_template, request, url_for,flash
from flask_login import login_user
from werkzeug.utils import redirect

from models.user import User
from passlib.hash import sha256_crypt

from extentions import db

app = Blueprint("user" ,__name__)


@app.route('/user/login', methods= ['GET', 'POST'])
def user():
    if request.method == 'GET':
        return render_template("user/login.html")
    else:
        register = request.form.get('register' ,None)
        username=request.form.get('username', None)
        password=request.form.get('password')
        phone=request.form.get('phone', None)
        address=request.form.get('address', None)

        if register != None:
            # حالا مستقیماً از User استفاده کن
            new_user = User(
                username=username,
                password=sha256_crypt.encrypt(password),
                phone=phone,
                address=address
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect('/user/dashboard')


        else:
            user= User.query.filter(User.username == username).first()
            if user == None:
                flash('نام کاربری یا رمز اشتباه است .')
                return redirect(url_for('user.user'))

            if sha256_crypt.verify(password,user.password):
                login_user(user)
                return redirect('/user/dashboard')
            else:
                flash('نام کاربری یا رمز اشتباه سات .')
                return redirect(url_for('user.login'))

        return  'done'