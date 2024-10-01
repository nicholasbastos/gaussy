from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import re
import base64
import hashlib
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaussy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# URL validation pattern (only http and https)
url_pattern = re.compile(r"^(https?)://[^\s/$.?#].[^\s]*$")

# Db Model definition
class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, unique=True, nullable=False)
    short_url = db.Column(db.String, unique=True, nullable=False)
    creation_attempts = db.Column(db.Integer, default=0)
    access_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analytics = db.relationship('URLAnalytics', backref='url', lazy=True)

class URLAnalytics(db.Model):
    __tablename__ = 'url_analytics'
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    ip_address = db.Column(db.String)
    browser = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
