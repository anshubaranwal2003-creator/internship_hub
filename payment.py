from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import stripe
import config

app = Flask(__name__)

# Stripe config
stripe.api_key = config.STRIPE_SECRET_KEY

# MySQL DB connection
db = mysql.connector.connect(**config.DB_CONFIG)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('payindex.html')

@app.route('/pay', methods=['POST'])
def pay():
    amount = int(request.form['amount']) * 100  # in paisa (Stripe uses cents)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Internship Application Fee',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('index', _external=True),
    )
    return redirect(session.url, code=303)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login')
def login():
    return render_template('paylogin.html')
@app.route('/dashboard')
def dashboard():
    # Fetch payment data from the database
    cursor.execute("SELECT * FROM payments ORDER BY payment_date DESC")
    payments = cursor.fetchall()  # Get all records from the payments table
    
    return render_template('paymentdashboard.html', payments=payments)


if __name__ == '__main__':
    app.run(debug=True,port=9000)