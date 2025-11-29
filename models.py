from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    plan_selected = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, contacted, converted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'business_name': self.business_name,
            'email': self.email,
            'whatsapp_number': self.whatsapp_number,
            'country': self.country,
            'message': self.message,
            'plan_selected': self.plan_selected,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class PricingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(50), unique=True, nullable=False)  # Starter, Pro, Business
    base_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Integer, default=0)  # 0-100
    features = db.Column(db.Text, nullable=True)  # JSON string
    is_featured = db.Column(db.Boolean, default=False)
    checkout_url = db.Column(db.String(200), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def apply_discount(self, discount_percent):
        """Apply discount percentage and update current price"""
        self.discount_percent = max(0, min(100, discount_percent))  # Clamp between 0-100
        self.current_price = self.base_price * (1 - self.discount_percent / 100)
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_name': self.plan_name,
            'base_price': self.base_price,
            'current_price': self.current_price,
            'discount_percent': self.discount_percent,
            'features': self.features,
            'is_featured': self.is_featured,
            'checkout_url': self.checkout_url,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

