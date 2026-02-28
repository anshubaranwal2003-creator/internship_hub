
from flask import Flask, render_template, request, redirect,session
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",  # Your MySQL host, default is localhost
    user="root",       # MySQL username (use your own)
    password="rahul@12345",       # MySQL password (use your own)
    database="internship_hub3"  # The database you created
)
cursor = conn.cursor()

# Home route (Redirect to register page)
@app.route('/')
def home():
    return redirect('/register')

# Register route (Handles form submission and inserts data into MySQL)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        university = request.form['university']
        student_id = request.form['student_id']
        description = request.form['description']
        password = request.form['password']
        
        # Optional: Leave resume field empty for now
        resume = ""

        # Password hashing (using werkzeug to hash the password)
        hashed_password = generate_password_hash(12345)

        # SQL Query to insert data into 'students' table
        try:
            cursor.execute("""
                INSERT INTO students (name, email, phone, university, student_id, description, resume, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, phone, university, student_id, description, resume, hashed_password))
            conn.commit()
            return "✅ Registration Successful!"
        except mysql.connector.IntegrityError:
            return "❌ Email already exists. Try a different one."
    return render_template('register.html')
# Login route (Handles user authentication)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Query to get user details based on the email
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cursor.fetchone()  # Fetch the user from the database

        if user:
            # Compare hashed password stored in database with the entered password
            if check_password_hash(user[8], password):  # user[8] stores the hashed password
                session['user'] = user[1]  # Store the user's name or email in session
                return redirect('/dashboard')  # Redirect to the dashboard or home page
            else:
                return "❌ Incorrect password."
        else:
            return "❌ User not found. Please check your email."

    return render_template('login.html')
#Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')  # If no user is logged in, redirect to login page
    
    # Fetch user data based on the session's 'user' (which is stored as their name or email)
    user_email = session['user']  # This is assuming the session is storing the email of the user.
    cursor.execute("SELECT * FROM students WHERE email = %s", (user_email,))
    user_data = cursor.fetchone()  # Fetch the logged-in user's data

    if user_data:
        return render_template('dashboard.html', user=user_data)  # Pass user data to the template
    else:
        return "❌ User data not found."
 
@app.route('/logout')
def logout_confirm():
    return render_template('logout.html')

@app.route('/logout')
def logout():
     session.pop('user', None)
     flash("You have been logged out.", "info")
     return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

