from flask import Flask, redirect, render_template, request, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_session import Session
import argon2
from functools import wraps

app = Flask(__name__)

# Set the secret key to enable session usage
app.secret_key = 'task_flow'

# Configure Flask-Session to use filesystem (You can also configure it to use other options like Redis)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['MYSQL_HOST'] = 'raspberrypy.ddns.net'
app.config['MYSQL_USER'] = 'taskflow'
app.config['MYSQL_PASSWORD'] = 'Ionio2002@!'
app.config['MYSQL_DB'] = 'task_flow'

mysql = MySQL(app)
ph = argon2.PasswordHasher()

def is_logged_in():
    return 'logged_in' in session

# Define a decorator function to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    print(session)
    theme_mode = session.get('theme_mode', 'light')
    return render_template('index.html', theme_mode=theme_mode)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['Name']
        surname = request.form['Surname']
        username = request.form['Username']
        email = request.form['Email'].lower()
        password = request.form['password']
        hashed_password = ph.hash(password)
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users (name, surname, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, surname, username, email, hashed_password))
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
   
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Email'].lower()
        password = request.form['password']
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            stored_password = user[4]  
            try:
                ph.verify(stored_password, password)
                
                session['user_id'] = user[0]
                session['logged_in'] = True
                
                session['theme_mode'] = request.form.get('theme_mode', 'light')

                return render_template('home.html')
            except argon2.exceptions.VerifyMismatchError:
                return render_template('login.html', error='Invalid email or password.')

        cur.close()

    return render_template('login.html')

@app.route('/index')
def logout():
    print(session)
    session.clear()
    return redirect(url_for('index'))

@app.route('/Templates/Profile.html')
@login_required
def profile():
    return render_template('Profile.html')

@app.route('/Templates/index.html')
@login_required
def about():
    return render_template('index.html')

@app.route('/Templates/home.html')
@login_required
def home():
    print(session)
    return render_template('home.html')

@app.route('/submit_task', methods=['POST'])
@login_required
def submit_task():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO tasks (Title, Content, Status, username) VALUES (%s, %s, %s, %s)",
                    (title, content, user_id, 'todo'))
        
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))  # Redirect to home page after submitting task

    # Return an error response if the request method is not POST
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    user_id = session['user_id']
    email = request.form.get('change-email')
    name = request.form.get('change-name')
    surname = request.form.get('change-surname')
    password = request.form.get('change-password')
    username = request.form.get('change-username')

    cur = mysql.connection.cursor()
    
    if email:
        cur.execute("UPDATE users SET email = %s WHERE name = %s", (email, user_id))
    
    if name:
        cur.execute("UPDATE users SET name = %s WHERE name = %s", (name, user_id))
    
    if surname:
        cur.execute("UPDATE users SET surname = %s WHERE name = %s", (surname, user_id))
    
    if password:
        hashed_password = ph.hash(password)
        cur.execute("UPDATE users SET password = %s WHERE name = %s", (hashed_password, user_id))
    
    if username:
        cur.execute("UPDATE users SET username = %s WHERE name = %s", (username, user_id))
    
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True})

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    
    # Delete the user from the database
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    
    mysql.connection.commit()
    cur.close()

    # Clear the session to log the user out
    session.clear()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.debug = True
    app.run()
