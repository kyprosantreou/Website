from flask import Flask, redirect, render_template, request, url_for, make_response
from flask_mysqldb import MySQL
import argon2

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'raspberrypy.ddns.net'
app.config['MYSQL_USER'] = 'taskflow'
app.config['MYSQL_PASSWORD'] = 'Ionio2002@!'
app.config['MYSQL_DB'] = 'task_flow'

mysql = MySQL(app)
ph = argon2.PasswordHasher()

@app.route('/')
def index():
    theme_mode = request.cookies.get('theme_mode', 'light')
    return render_template('index.html', theme_mode=theme_mode)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            stored_password = user[4]  
            try:
                ph.verify(stored_password, password)
                
                response = make_response(redirect(url_for('index')))
                
                response.set_cookie('theme_mode', request.form.get('theme_mode', 'light'))
                return response
            except argon2.exceptions.VerifyMismatchError:
                return render_template('login.html', error='Invalid email or password.')

        cur.close()

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['Name']
        surname = request.form['Surname']
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['password']
        hashed_password = ph.hash(password)
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users (name, surname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, surname, username, email, hashed_password))
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
   
    return render_template('register.html')


@app.route('/static/Templates/Profile.html')
def profile():
    return render_template('Profile.html')

if __name__ == '__main__':
    app.debug = True
    app.run()