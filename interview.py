from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rahul@12345'
app.config['MYSQL_DB'] = 'interviewhub'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        application_id = request.form['application_id']
        interview_date = request.form['interview_date']
        mode = request.form['mode']
        result = request.form['result']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO interviews (application_id, interview_date, mode, result)
            VALUES (%s, %s, %s, %s)
        """, (application_id, interview_date, mode, result))
        mysql.connection.commit()
        cur.close()
        return redirect('/')

    # Show all interviews
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM interviews ORDER BY interview_id DESC")
    interviews = cur.fetchall()
    cur.close()
    return render_template('interviews.html', interviews=interviews)

if __name__ == '__main__':
    app.run(debug=True)
