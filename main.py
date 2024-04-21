from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'raspberrypy.ddns.net'
app.config['MYSQL_USER'] = 'taskflow'
app.config['MYSQL_PASSWORD'] = 'Ionio2002@!'
app.config['MYSQL_DB'] = 'task_flow'

mysql = MySQL(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        cur.close()

        if user:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password.')

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
   if request.method == 'POST':
      name = request.form['Name']
      surname = request.form['Surname']
      username = request.form['Username']
      email = request.form['Email']
      password = request.form['password']
      cur = mysql.connection.cursor()

      cur.execute(f"INSERT INTO users (name, surname, username, email, password) VALUES ('{name}', '{surname}', '{username}', '{email}', '{password}')")
      
      mysql.connection.commit()

      cur.close()

      return redirect(url_for('login'))
   
   return render_template('register.html')

if __name__ == '__main__':
    app.debug = True
    app.run() 