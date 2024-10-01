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

# Generate Short URL
def generate_short_url(long_url):
    hash_object = hashlib.sha256(long_url.encode())
    short_url = base64.urlsafe_b64encode(hash_object.digest()[:4]).decode('utf-8')
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('long_url')

    if not long_url or not re.match(url_pattern, long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    ip_address = get_client_ip()
    browser = get_browser_info()

    existing_url = URL.query.filter_by(long_url=long_url).first()

    if existing_url:
        existing_url.creation_attempts += 1
        db.session.commit()
        return jsonify({"short_url": existing_url.short_url})

    short_url = generate_short_url(long_url)
    new_url = URL(long_url=long_url, short_url=short_url, creation_attempts=1)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({"short_url": short_url}), 201

# Redirect based on short URL
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    ip_address = get_client_ip()
    browser = get_browser_info()

    url_entry = URL.query.filter_by(short_url=short_url).first()

    if not url_entry:
        return jsonify({"error": "URL not found"}), 404
    
    url_entry.access_count += 1
    analytics_record = URLAnalytics(url_id=url_entry.id, ip_address=ip_address, browser=browser)
    db.session.add(analytics_record)
    db.session.commit()
    return redirect(url_entry.long_url)

