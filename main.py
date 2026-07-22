from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "iconic_vha_secure_secret_key"  # Required for sessions and flashing messages

# In-Memory Database Simulation (Replace with SQLite/PostgreSQL later if needed)
# Passwords are secure hashes to ensure Confidentiality and Integrity
USERS_DB = {
    "admin@iconicvha.com": {
        "name": "Admin User",
        "password": generate_password_hash("securepassword123")
    }
}

PROPERTIES_DB = [
    {"id": 1, "title": "Modern 2 Bedroom Apartment", "location": "Kilimani, Nairobi", "price": 45000, "type": "Apartment", "description": "Spacious and secure apartment with high-speed fiber internet and ample parking."},
    {"id": 2, "title": "Executive Studio Suite", "location": "Westlands, Nairobi", "price": 25000, "type": "Studio", "description": "Cozy fully-furnished studio suite located close to major shopping malls."},
    {"id": 3, "title": "Luxury 4 Bedroom Townhouse", "location": "Karen, Nairobi", "price": 120000, "type": "Townhouse", "description": "Exquisite townhouse with a private garden, 24/7 security, and backup generator."},
    {"id": 4, "title": "Affordable Loft Studio", "location": "Roysambu, Nairobi", "price": 18000, "type": "Studio", "description": "Modern finishes, constant water supply, and easy access to public transit."}
]

TOURS_DB = [
    {"id": 1, "property": "Modern 2 Bedroom Apartment", "date": "2026-07-25", "status": "Confirmed"}
]

@app.route('/')
def index():
    return render_template('index.html', properties=PROPERTIES_DB[:3])

@app.route('/houses')
def houses():
    location_query = request.args.get('location', '').lower()
    type_query = request.args.get('type', 'all')
    max_price = request.args.get('max_price', type=int)

    filtered = PROPERTIES_DB
    if location_query:
        filtered = [p for p in filtered if location_query in p['location'].lower()]
    if type_query and type_query != 'all':
        filtered = [p for p in filtered if p['type'] == type_query]
    if max_price:
        filtered = [p for p in filtered if p['price'] <= max_price]

    return render_template('houses.html', properties=filtered)

@app.route('/house/<int:house_id>')
def house_details(house_id):
    property_item = next((p for p in PROPERTIES_DB if p['id'] == house_id), None)
    if not property_item:
        return "Property not found", 404
    return render_template('house-details.html', property=property_item)

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = USERS_DB.get(email) # type: ignore
        
        # Strict validation ensuring Integrity and Confidentiality checks
        if user and check_password_hash(user['password'], password): # type: ignore
            session['user_email'] = email
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('tenant_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if email in USERS_DB:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('login'))

        # Store secure password hash
        USERS_DB[email] = {
            "name": name,
            "password": generate_password_hash(password) # type: ignore
        }
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def tenant_dashboard():
    if 'user_email' not in session:
        flash('Please log in to access your dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('tenant-dashboard.html', user_name=session.get('user_name'), tours=TOURS_DB)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
