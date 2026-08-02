from flask import Blueprint, render_template, request, url_for,flash
from flask_login import login_user, login_required, current_user
from werkzeug.utils import redirect

from models.cart import Cart
from models.product import Product
from models.user import User
from models.cart_item import CartItem
from passlib.hash import sha256_crypt
from extentions import db

app = Blueprint("user" ,__name__)


@app.route('/user/login', methods= ['GET', 'POST'])
def login():
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
                password=sha256_crypt.hash(password),
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
                return redirect(url_for('user.login'))

            if sha256_crypt.verify(password,user.password):
                login_user(user)
                return redirect('/user/dashboard')
            else:
                flash('نام کاربری یا رمز اشتباه است...')
                return redirect(url_for('user.login'))

        return  'done'



@app.route('/add_to_cart', methods=['GET'])
@login_required
def add_to_cart():
    product_id = request.args.get('id', type=int)

    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return "Product not found", 404

    cart = current_user.carts.filter_by(status="pending").first()

    if cart is None:
        cart = Cart()
        current_user.carts.append(cart)
        db.session.add(cart)
        db.session.flush()   # تا cart.id ساخته شود

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item is None:
        cart_item = CartItem(
            quantity=1,
            cart=cart,
            product=product
        )
        db.session.add(cart_item)
    else:
        cart_item.quantity += 1

    db.session.commit()
    return redirect(url_for("user.cart"))


@app.route('/user/dashboard', methods=['GET'])
@login_required
def dashboard():
    return "done...."

@app.route('/user/cart', methods=['GET'])
@login_required
def cart():
    return render_template("user/cart.html")
