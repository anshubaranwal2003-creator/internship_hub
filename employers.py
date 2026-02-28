
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",        # <-- Change this
    password="rahul@12345",    # <-- Change this
    database="internship_hub1"       # <-- Change this
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employers ORDER BY created_at DESC")
    employers = cursor.fetchall()
    return render_template('list_employers.html', employers=employers)

@app.route('/add', methods=['GET', 'POST'])
def add_employers():
    if request.method == 'POST':
        data = (
            request.form['employee_id'],
            request.form['company_name'],
            request.form['contact_person'],
            request.form['email'],
            request.form['industry'],
            request.form.get('coding_test_link', '')
        )
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO employers 
            (employee_id, company_name, contact_person, email, industry, coding_test_link)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, data)
        db.commit()
        return redirect('/')
    return render_template('add_employers.html')

if __name__ == '__main__':
    app.run(debug=True)
