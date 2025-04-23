from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Jewellery(db.Model):
    __tablename__ = 'jewelry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    image3 = db.Column(db.String(255))
    category = db.Column(db.String(50))
    rating = db.Column(db.Float, default=0.0)

    cart_items = db.relationship(
        'CartItem',
        back_populates='jewellery',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image1': self.image1,
            'image2': self.image2,
            'image3': self.image3,
            'price': self.price,
            'category': self.category,
            'rating': self.rating
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50),default="User")
    address = db.Column(db.String)
    phone = db.Column(db.String)

    cart_items = db.relationship(
        'CartItem',
        back_populates='customer',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    cart = association_proxy(
        'cart_items',
        'jewellery',             
        creator=lambda jewellery: CartItem(jewellery=jewellery)
    )

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'cart': [item.to_dict() for item in self.cart]
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    jewellery_id = db.Column(db.Integer, db.ForeignKey('jewelry.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    customer = db.relationship('Customer', back_populates='cart_items')
    jewellery = db.relationship('Jewellery', back_populates='cart_items')

    def to_dict(self):
        return {
            'jewellery': self.jewellery.to_dict(),
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat()
        }

