from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD
import mysql.connector
from flask import current_app 
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



class User(UserMixin):

    def __init__(self,id,username,email,password,roles,surname,name,numsTel,lang):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.roles = roles 
        self.surname = surname 
        self.name = name 
        self.lang = lang
        
    def update_user(self,username,email=None):
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor()
        if email:
            c.execute("UPDATE contact SET  email = %s WHERE id = %s",(email,self.id))
            self.email = email
        else:
            c.execute("UPDATE user SET username = %s WHERE username = %s",(username,self.username))
            self.username = username
        db.commit()
        c.close()
        db.close()

    def update_password(self,password):
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor()
        c.execute("UPDATE user SET password = %s WHERE username = %s",(password,self.username))
        self.password = password
        db.commit()
        c.close()
        db.close()

    def update_picture(self,image_file):
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor()
        c.execute("UPDATE user SET image_file = %s WHERE username = %s",(image_file,self.username))
        self.image_file = image_file
        db.commit()
        c.close()
        db.close()

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return get_user(id=user_id)

    def __repr__(self):
        return f"User '{self.username}', '{self.email}' "

class Contact:
    def __init__(self,email,name,surname,numsTel=None,id=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.numsTel = numsTel
        self.id = id

from application.users.operations import get_user


