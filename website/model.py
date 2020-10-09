from website import db, bcrypt
from flask_login import UserMixin


class UserRegister(UserMixin, db.Model):

    __tablename__ = 'UserRegisters'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def check_password(self, password):

        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)


class Product(db.Model):

    __tablename__= 'Pruducts'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_price = db.Column(db.DECIMAL(10,2))
    product_qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'product:%s, price:%d, qty:%d' % (self.product_name, self.product_price, self.product_qty)

class Cart(db.Model):

    __tablename__ = 'Cart'
    orderid = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_price = db.Column(db.DECIMAL(10,2))
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'product_name: %s, product_id:%s, qty:%d' % (self.product_name, self.product_id, self.quantity)

