import mysql.connector
from application.database import DATABASE_NAME,DATABASE_PASSWORD,DATABASE_USERNAME

db = mysql.connector.connect(
    host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
)
c = db.cursor()

c.close()
db.close()