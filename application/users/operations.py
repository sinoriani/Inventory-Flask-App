#from application.database import db, c, reconnect_to_database
from application.users.models import User
from datetime import date
from flask import flash
import mysql.connector
from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD



def create_user(username,email,password,role,surname,name,numerosTel):
    db = mysql.connector.connect(
        host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
    )
    c = db.cursor(buffered=True)
    
    c.execute("INSERT INTO contact(name,surname,email) VALUES(%s, %s, %s)",(name,surname,email))
    c.execute("SELECt max(id) FROM contact")
    uid = c.fetchone()[0]
    c.execute("INSERT INTO user(id,username,password)  VALUES(%s, %s, %s)", (uid,username,password))
    if numerosTel:
        for n in numerosTel:
            try:
                c.execute("INSERT INTO telephone(num) VALUES(%s) ",(n,))
            except:
                pass

            try:
                c.execute("INSERT INTO contactTelephone(num,uid) VALUES(%s,%s) ",(n,uid))
            except:
                flash("The phone number could not be linked to the user.")
    #if role == 'player':
    #    if create_player(surname,name,birth_date,uid) == -1:
    #        return False
    
    role = role.capitalize()
    c.execute("INSERT INTO user_role(uid,role) VALUES(%s,%s)", (uid, role))
    db.commit()
    c.close()
    db.close()



def get_users():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("SELECT id from user")
        res = c.fetchall()

        users = []
        for r in res:
            users.append(get_user(id=r[0]))
        return users
    except Exception as e:
        print("get_users error: ",e)
    finally:
        c.close()
        db.close()




def get_user(email=None,id=None,username=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if email and username:
            c.execute("SELECT u.id,username,email,password,surname,name,lang FROM user u,contact c WHERE u.id = c.id and (email like %s or username like %s  )",(email,username))
        elif email:
            c.execute("SELECT u.id,username,email,password,surname,name,lang FROM user u,contact c WHERE  u.id = c.id  and email like (%s)",(email,))
        elif id:
            c.execute("SELECT u.id,username,email,password,surname,name,lang FROM user u,contact c WHERE u.id = c.id  and u.id = (%s)",(id,))
        elif username:
            c.execute("SELECT u.id,username,email,password,surname,name,lang FROM user u,contact c WHERE u.id = c.id  and username = (%s)",(username,))    
        else:
            return None

        res = c.fetchone()
        if res is not None:
            username=res[1]
            email=res[2]
            password=res[3]
            surname=res[4]
            name=res[5]
            uid=res[0]
            lang=res[6]
            roles = get_user_roles(uid)
            c.execute("SELECT num FROM contactTelephone WHERE uid = %s",(uid,))
            numsTel = c.fetchall()
            numsTel = [n[0] for n in numsTel]
            return User(id=uid,username=username,email=email,
                        password=password,surname=surname,name=name,roles=roles,numsTel=numsTel,lang=lang) 
        else:
            return None
    except Exception as e:
        print("get_user error: ",e)
    finally:
        c.close()
        db.close()


def get_user_roles(uid):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("SELECT role FROM  user_role ur WHERE ur.uid = (%s) ",(uid,))
        res = c.fetchall()
        if res is None:
            return None
        else:
            return [r[0] for r in res ]

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()


def get_username(id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("SELECT username FROM user WHERE id = (%s) ",(id,))
        res = c.fetchone()
        return res[0] if res is not None else None

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()


def get_userid(_username):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT id FROM user WHERE username like (%s) ",(_username,))
        res = c.fetchone()
        return res[0] if res is not None else None

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()

def user_exists(_username):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        id = get_userid(_username)
        return True if id is not None else False

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()

def email_exists(_email):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT email FROM contact WHERE email like (%s) ",(_email,))
        res = c.fetchone()
        return True if res is not None else False

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()

def get_user_password(_email):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT password FROM user u ,contact c WHERE u.id = c.id and email like (%s) ",(_email,))
        res = c.fetchone()
        return res[0] if res is not None else None

    except Exception as e:
        print("error: ",e)
    finally:
        c.close()
        db.close()

def get_employees():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT id FROM user u ")
        res = c.fetchall()
        users = []
        for r in res:
            users.append(get_user(id=r[0]))
        return users
    except Exception as e:
        print("get_employees error: ",e)
    finally:
        c.close()
        db.close()

def get_roles():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT type FROM role")
        res = c.fetchall()
        roles = []
        for r in res:
            roles.append(r[0])
        return roles
    except Exception as e:
        print("get_roles error: ",e)
    finally:
        c.close()
        db.close()


def link_operation_to_role_op(role_name,operation):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("INSERT INTO operationRole(operation ,role_name) VALUES(%s, %s)",(operation ,role_name))
        db.commit()
        flash('Operation successful','success')

    except Exception as e:
        print("link_operation_to_role error: ",e)
    finally:
        c.close()
        db.close()


def remove_operation_from_role_op(role_name,operation):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("DELETE FROM operationRole WHERE operation = %s and role_name = %s",(operation ,role_name))
        db.commit()
        flash('Operation successful','success')

    except Exception as e:
        print("remove_operation_from_role error: ",e)
    finally:
        c.close()
        db.close()


def get_operations_for_roles():
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        all_operations = [
            ('Add users','text-default'), ('Check users list','text-default'),
            ('Add tasks','text-primary'), ('Edit tasks','text-primary'), ('Check tasks list','text-primary'), ('Update task status','text-primary'), ('Postpone tasks','text-primary'),
            ('Add products','text-secondary'), ('Edit products','text-secondary'), ('Check products list','text-secondary'), ('Add company','text-success'), ('Edit company','text-success'), ('Check companies list','text-success'), ('Update parameters','text-danger'),
            ('Add affairs','text-info'), ('Edit affairs','text-info'), ('Check affairs list','text-info'), ('Update affair status','text-info'),
            ("Check daily report","text-blue"), ("Add presence","text-blue")
        ]

        c.execute("SELECT operation, role_name FROM operationRole")
        res = c.fetchall() 
        roles = get_roles()
        result = {}
        for r in roles:
            result[r] = {
                'assigned':[],
                'available':[]
            }
        for r in res:
            operation = r[0]
            role_name = r[1]
            for op in all_operations:
                if op[0] == operation:
                    result[role_name]['assigned'].append(op)
                    break
        
        for r in roles:
            result[r]['available'] = [item for item in all_operations if item not in  result[r]['assigned']]
        return result

    except Exception as e:
        print("get_operations_for_roles error: ",e)
    finally:
        c.close()
        db.close()


def user_can_do_operation(operation,roles):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        for role_name in roles:
            c.execute("SELECT operation FROM operationRole WHERE role_name = %s and operation = %s",(role_name, operation ))
            res = c.fetchone() 
            if res is not None:
                return True
        flash('No access','danger')
        return False
        
    except Exception as e:
        print("user_can_do_operation error: ",e)
    finally:
        c.close()
        db.close()

def add_role_op(role):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("INSERT INTO role(type) VALUES(%s)",(role, ))
        db.commit()
        flash("Operation successful","success")
       
    except Exception as e:
        print("add_role_op error: ",e)
        flash("An error occured","danger")
    finally:
        c.close()
        db.close()


def add_presence_op(users_presence,dat=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        current_date = date.today()
        if dat is None or dat == "":
            dat = str(current_date)
        
        for uid,values in users_presence.items():
            if "vacation" not in values and (values['clock_in_hour'] == "0" or  values['clock_in_hour'] == "00" or values['clock_out_hour'] == "0" or  values['clock_out_hour'] == "00"):
                continue
            #else:
            #    clock_in = values['clock_in_hour'].zfill(2) + ':' + values['clock_in_minute'].zfill(2),
            #    clock_out = values['clock_out_hour'].zfill(2) + ':' + values['clock_out_minute'].zfill(2)

            if "vacation" not in values:
                clock_in = values['clock_in_hour'].zfill(2) + ':' + values['clock_in_minute'].zfill(2)
                clock_out = values['clock_out_hour'].zfill(2) + ':' + values['clock_out_minute'].zfill(2)
            else:
                clock_in = clock_out = None
            item = (
                    uid,
                    dat,
                    clock_in,
                    clock_out
                )

            try:
                c.execute("INSERT INTO presence(user_id, dat, clock_in, clock_out) VALUES(%s, STR_TO_DATE(%s,'%Y-%m-%d'), %s ,%s) ",item)
            except Exception as e:
                print("add_presence_op query error :",e)
        
        db.commit()
        flash("Operation successful","success")
       
    except Exception as e:
        print("add_presence_op error: ",e)
        flash("An error occured","danger")
    finally:
        c.close()
        db.close()

def edit_presence_op(user_id,clock_in,clock_out):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("UPDATE presence SET(clock_in = %s ,clock_out =%s ) WHERE user_id = %s",(clock_in,clock_out,user_id ))
        db.commit()
        flash("Operation successful","success")
       
    except Exception as e:
        print("add_presence_op error: ",e)
        flash("An error occured","danger")
    finally:
        c.close()
        db.close()


def get_presence_history(dat):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        
        c.execute("SELECT user_id, dat, clock_in, clock_out FROM presence WHERE dat = %s",(dat, ))
        res = c.fetchall()
       
        users = {}
        for r in res:
            user = get_user(id=r[0])
            name = user.name if user.name else '' + user.surname if user.surname else ''
            users[ name ] = {
                "clock_in":r[2],
                "clock_out":r[3]
            }
        return users
       
    except Exception as e:
        print("get_presence_history error: ",e)
        flash("An error occured","danger")
    finally:
        c.close()
        db.close()