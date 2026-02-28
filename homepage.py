from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # or your remote database host
app.config['MYSQL_USER'] = 'root'       # MySQL username
app.config['MYSQL_PASSWORD'] = 'rahul@12345'       # MySQL password
app.config['MYSQL_DB'] = 'internshiphub1'

mysql = MySQL(app)

@app.route('/')
def home():
    # Query for fetching internships or any other data from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM internships LIMIT 5;")
    internships = cur.fetchall()
    cur.close()

    # Render the HTML template with the internships data
    return render_template('homepage.html', internships=internships)

if __name__ == '__main__':
    app.run(debug=True)
