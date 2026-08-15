from flask import Blueprint, render_template, request, url_for,flash
from flask_login import login_user, login_required, current_user
from werkzeug.utils import redirect

from models.cart import Cart
from models.payment import Payment
from models.product import Product
from models.user import User
from models.cart_item import CartItem
from passlib.hash import sha256_crypt
from extentions import db
import requests
app = Blueprint("user" ,__name__)


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("user/login.html")
    else:
        register = request.form.get('register', None)
        username = request.form.get('username', None)
        password = request.form.get('password')
        phone = request.form.get('phone', None)
        address = request.form.get('address', None)

        next_page = request.args.get('next')

        if register != None:
            new_user = User(
                username=username,
                password=sha256_crypt.hash(password),
                phone=phone,
                address=address
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            return redirect('/user/dashboard')

        else:
            user = User.query.filter(User.username == username).first()

            if user == None:
                flash('نام کاربری یا رمز اشتباه است.')
                return redirect(url_for('user.login'))

            if sha256_crypt.verify(password, user.password):
                login_user(user)

                if next_page and next_page.startswith('/'):
                    return redirect(next_page)

                return redirect('/user/dashboard')

            else:
                flash('نام کاربری یا رمز اشتباه است...')
                return redirect(url_for('user.login'))

        return 'done'



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
        db.session.flush()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id,
    ).first()

    if cart_item is None:
        cart_item = CartItem(
            quantity=1,
            cart=cart,
            product=product,
            price=product.price
        )
        db.session.add(cart_item)
    else:
        cart_item.quantity += 1

    db.session.commit()
    return redirect(url_for("user.cart"))


@app.route('/user/dashboard', methods=['GET'])
@login_required
def dashboard():
   return render_template('user/dashboard.html')

@app.route('/user/cart', methods=['GET'])
@login_required
def cart():
    cart = current_user.carts.filter(
        Cart.status == "pending"
    ).first()

    return render_template("user/cart.html", cart=cart)




@app.route('/remove_from_cart', methods=['GET'])
@login_required
def remove_from_cart():
    id = request.args.get('id')
    cart_item = CartItem.query.filter(CartItem.id == id).first_or_404()
    if cart_item.quantity >1:
        cart_item.quantity -= 1
    else:
        db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for("user.cart"))



@app.route('/payment', methods=['GET'])
@login_required
def payment():
   cart=current_user.carts.filter(Cart.status == "pending").first()
   r=requests.post('https://sandbox.shepa.com/api/v1/token',data={
       'api':'sandbox',
       'amount':cart.total_price(),
       'callback':"http://localhost:5000/verify"
   })

   token=r.json()['result']['token']
   url = r.json()['result']['url']

   pay= Payment(price= cart.total_price(),token=token)
   pay.cart=cart
   db.session.add(pay)
   db.session.commit()


   return redirect(url)



@app.route('/verify', methods=['GET'])
@login_required
def verify():
   token=request.args.get('token')
   pay =Payment.query.filter(Payment.token==token).first_or_404()
   r=requests.post('https://sandbox.shepa.com/api/v1/verify',data={
       'api':'sandbox',
       'amount':pay.price,
       'token':token    })

   pay_status=bool( r.json()['success'])
   if pay_status :
       refid=r.json()['result']['refid']
       transaction_id = r.json()['result']['transaction_id']
       card_pan = r.json()['result']['card_pan']
       transaction_id = r.json()['result']['transaction_id']

       pay.card_pan=card_pan
       pay.transaction_id=transaction_id
       pay.refid=refid
       pay.status = 'success'
       pay.cart.status ='paid'
   else:
       pay.status ='error'
   db.session.commit()

   return redirect(url_for('user.dashboard'))


@app.route('/user/dashboard/order/<id>', methods=['GET'])
@login_required
def order(id):
    cart= current_user.carts.filter(Cart.id==id).first_or_404()
    return render_template('user/order.html', cart=cart)


