from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rahul@12345'
app.config['MYSQL_DB'] = 'feedbackhub'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        comment = request.form['comment']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews (name, rating, comment) VALUES (%s, %s, %s)", (name, rating, comment))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    # Show all reviews
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, rating, comment, created_at FROM reviews ORDER BY id DESC")
    reviews = cur.fetchall()
    cur.close()
    return render_template('feedback.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
