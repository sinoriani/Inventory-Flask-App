from flask import flash
import mysql.connector
from application.database import DATABASE_USERNAME,DATABASE_NAME, DATABASE_PASSWORD
from application.users.operations import get_user
from application.tasks.models import Task


def add_task_op(task):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        if 'None' in task.due_hour:
            task.due_hour = ''
        c.execute("""INSERT INTO task(name,description,creator,assigned_user,due_date,priority, due_hour)
                     VALUES(%s, %s, %s, %s, STR_TO_DATE(%s,'%Y-%m-%d'), %s, %s)""",
                     (task.name , task.description, task.creator, task.assigned_user, task.due_date, task.priority, task.due_hour ))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()

def edit_task_op(task):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        if 'None' in task.due_hour:
            task.due_hour = ''
        c.execute("""UPDATE task SET name=%s,description=%s,assigned_user=%s,due_date=%s,priority=%s, due_hour=%s WHERE id = %s""",
                     (task.name , task.description,  task.assigned_user, task.due_date, task.priority, task.due_hour, task.id ))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()




def get_tasks(assigned_user_id=None):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        if assigned_user_id:
            c.execute("""SELECT id,name, description, creator, assigned_user, due_date, due_hour, priority, date_created, progress, status
                     FROM task
                     WHERE status != 'Done' and assigned_user = %s""",(assigned_user_id,))
        else:
            c.execute("""SELECT id,name, description, creator, assigned_user, due_date, due_hour, priority, date_created, progress, status
                     FROM task""")
        res = c.fetchall()
        tasks = []
        for r in res:
            tasks.append(
                Task(
                    id=r[0],
                    name=r[1],
                    description=r[2],
                    creator = get_user(id=r[3]),
                    assigned_user = get_user(id=r[4]),
                    due_date = r[5],
                    due_hour = r[6],
                    priority = r[7],
                    date_created = r[8],
                    progress=r[9],
                    status=r[10]
                )
            )
        return tasks
    except Exception as e:
        print("get_tasks error: ",e)
    finally:
        c.close()
        db.close()



def get_task(tid):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""SELECT id,name, description, creator, assigned_user, due_date, due_hour, priority, date_created, progress, status
                     FROM task
                     WHERE id = %s """,(tid, ))
        r = c.fetchone()
        return  Task(
                    id=r[0],
                    name=r[1],
                    description=r[2],
                    creator = get_user(id=r[3]),
                    assigned_user = get_user(id=r[4]),
                    due_date = r[5],
                    due_hour = r[6],
                    priority = r[7],
                    date_created = r[8],
                    awaitedTasks = get_awaited_tasks(waitingTaskId=r[0]),
                    progress=r[9],
                    status=r[10]
                )
    except Exception as e:
        print("get_task error: ",e)
    finally:
        c.close()
        db.close()



def link_task_to_task_op(awaited_id, waiting_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""INSERT INTO taskAwait(waitingTaskId, awaitedTaskId)
                     VALUES(%s, %s)""",
                     (waiting_id, awaited_id))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()

def delete_awaited_task_from_list_op(awaited_id, waiting_id):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""DELETE FROM taskAwait
                     WHERE waitingTaskId = %s and awaitedTaskId = %s """,
                     (waiting_id, awaited_id))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()


def get_awaited_tasks(waitingTaskId):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""SELECT id,name, description, creator, assigned_user, due_date, due_hour, priority, date_created, progress , status
                     FROM task
                     WHERE id IN (SELECT awaitedTaskId 
                                  FROM taskAwait
                                  WHERE waitingTaskId = %s) """, (waitingTaskId, ))
        res = c.fetchall()
        tasks = []
        for r in res:
            tasks.append(
                Task(
                    id=r[0],
                    name=r[1],
                    description=r[2],
                    creator = get_user(id=r[3]),
                    assigned_user = get_user(id=r[4]),
                    due_date = r[5],
                    due_hour = r[6],
                    priority = r[7],
                    date_created = r[8],
                    progress=r[9],
                    status=r[10]
                )
            )
        return tasks
    except Exception as e:
        print("get_tasks error: ",e)
    finally:
        c.close()
        db.close()


def set_task_progress_op(tid,status,progress):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)

        c.execute("""UPDATE task SET progress = %s , status = %s WHERE id = %s""", (progress, status , tid))
        db.commit()
        flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()

def postpone_task_op(tid, days):
    try:
        db = mysql.connector.connect(
            host='localhost', user=DATABASE_USERNAME, password=DATABASE_PASSWORD, database=DATABASE_NAME, auth_plugin='mysql_native_password'
        )
        c = db.cursor(buffered=True)
        if isinstance(days, int):
            c.execute("""UPDATE task SET due_date=ADDDATE(due_date, INTERVAL %s DAY) WHERE id = %s""", (days,  tid))
            db.commit()
            flash("Operation successful",'success')
    except Exception as e:
        print("error: ",e)
        flash('An error occured','danger')
    finally:
        c.close()
        db.close()