from flask import render_template, flash, request, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from website import app, db, login_manager
from website.model import UserRegister, Product, Cart
from website.form import FormRegister, FormLogin

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def test_index():
    return render_template('home.html', products=Product.query.all())


@login_manager.user_loader
def load_user(user_id):
    return UserRegister.query.get(int(user_id))

@app.route("/addToCart", methods=['POST'])
@login_required
def addToCart():

    _productid = request.form['productid']
    _productname = request.form['productname']
    _productprice = float(request.form['productprice'])
    _quantity = int(request.form['quantity'])


    item = Cart.query.filter_by(product_id=_productid, user_id=current_user.id).first()
    if item:

        item.quantity +=  _quantity
        db.session.flush()
        db.session.commit()
        flash('Item: {}, Qty: {} , has been added to cart!'.format(_productname, _quantity))
        return redirect(url_for('test_index'))
    else:

        new_item = Cart(
            product_id = _productid,
            product_name = _productname,
            product_price = _productprice,
            quantity = _quantity,
            user_id = current_user.id
        )
        db.session.add(new_item)
        db.session.commit()

    return redirect(url_for('test_index'))

@app.route("/mycart/<int:productid>/delete", methods=['POST'])
@login_required
def deleteItem(productid):
    item = Cart.query.filter_by(product_id=productid, user_id=current_user.id).first()

    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('order'))


@app.route("/mycart", methods=['GET','POST'])
@login_required
def order():
    return render_template('order.html', user=current_user, items=Cart.query.filter_by(user_id=current_user.id))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()

        return render_template('success.html')
    return render_template('register.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def login():
    form = FormLogin()

    if form.validate_on_submit():
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:

            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('userinfo'))
            else:
                flash('Wrong Email or Password')
        else:
            flash('Wrong Email or Password')

    return render_template('login.html', form=form)

@app.route('/signout')
@login_required
def logout():
    logout_user()
    flash('Log Out Successfully.')
    return redirect(url_for('login'))

@app.route('/userinfo')
@login_required
def userinfo():

    return render_template('userinfo.html', user=current_user)



