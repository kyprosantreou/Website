import mysql.connector

try:
        mydb = mysql.connector.connect(
            host="raspberrypy.ddns.net",
            user="taskflow",
            password="Ionio2002@!",
            database="task_flow",
        )
        cursor = mydb.cursor()

        # Create the accounts table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,     
            email VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE Tasks (
            TaskID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(255) NOT NULL,
            Content TEXT,
            Status ENUM('todo', 'inprogress', 'done') DEFAULT 'todo',
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username VARCHAR(255)       
        );
        ''')


        mydb.commit()

except mysql.connector.Error as err:
        print("MySQL Error: {}".format(err))