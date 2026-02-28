from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul@12345",
    database="internship_hub"
)
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()
    return render_template('index.html', internships=internships)

@app.route('/post', methods=['GET', 'POST'])
def post_internship():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        description = request.form['description']

        sql = "INSERT INTO internships (title, company, location, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (title, company, location, description))
        db.commit()
        return redirect('/')
    return render_template('post_internship.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)
