from flask import Flask,render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'raspberrypy.ddns.net'
app.config['MYSQL_USER'] = 'taskflow'
app.config['MYSQL_PASSWORD'] = 'Ionio2002@!'
app.config['MYSQL_DB'] = 'task_flow'
 
mysql = MySQL(app)