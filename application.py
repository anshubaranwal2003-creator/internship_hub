
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul@12345",
    database="internship_portal"
)
cursor = conn.cursor()

# Home route
@app.route('/')
def home():
    return render_template('indexapp.html')

# Apply route
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        student_id = request.form['student_id']
        internship_id = request.form['internship_id']
        date_applied = request.form['date_applied']
        
        # Store student_id in session after applying
        session['student_id'] = student_id
        
        # Insert application into the database
        cursor.execute("INSERT INTO applications (student_id, internship_id, date_applied) VALUES (%s, %s, %s)",
                       (student_id, internship_id, date_applied))
        conn.commit()
        return redirect('/status')
    return render_template('apply.html')

# Status route
@app.route('/status')
def status():
    # Check if student_id is in session, else redirect to login or home page
    if 'student_id' not in session:
        return redirect('/')  # Redirect to home or login page if not logged in
    
    student_id = session['student_id']
    
    # Fetch applications for the logged-in student
    cursor.execute("SELECT * FROM applications WHERE student_id = %s", (student_id,))
    applications = cursor.fetchall()
    
    return render_template('status.html', applications=applications)

# Admin dashboard
@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()
    return render_template('admin_dashboard.html', applications=applications)

# Update application status
@app.route('/update_status/<int:application_id>', methods=['POST'])
def update_status(application_id):
    new_status = request.form['status']
    cursor.execute("UPDATE applications SET status = %s WHERE application_id = %s", (new_status, application_id))
    conn.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
