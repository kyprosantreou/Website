from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'raspberrypy.ddns.net'
app.config['MYSQL_USER'] = 'taskflow'
app.config['MYSQL_PASSWORD'] = 'Ionio2002@!'
app.config['MYSQL_DB'] = 'task_flow'

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        name = request.form['Name']
        surname = request.form['Surname']
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users (name, surname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, surname, username, email, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return 'Registered successfully'

if __name__ == '__main__':
    app.run(debug=True)
