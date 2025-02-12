from flask_mysqldb import MySQL

# Initialize MySQL
mysql = MySQL()

def init_app(app):
    # MySQL Configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'hrs_tracker'
    
    mysql.init_app(app)