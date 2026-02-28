
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'rahul@12345',  # Replace with your MySQL password
    'database': 'internship_hub6'
}

# Route to Home Page with List of Universities
@app.route('/')
def home():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT university_id, name, location FROM University")
    universities = cursor.fetchall()
    conn.close()
    
    return render_template('index3.html', universities=universities)

# Route to Display Internships based on University ID
@app.route('/internships/<int:university_id>')
def internships(university_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, company, location, start_date, end_date
        FROM Internship
        WHERE university_id = %s
    """, (university_id,))
    internships = cursor.fetchall()
    conn.close()
    
    return render_template('internship.html', internships=internships)

if __name__ == "__main__":
    app.run(debug=True)
