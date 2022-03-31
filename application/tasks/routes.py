from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
from application.tasks.models import Task
from application.tasks.operations import postpone_task_op,edit_task_op,set_task_progress_op, link_task_to_task_op,get_awaited_tasks,add_task_op, get_tasks, get_task
from application.tasks.forms import AddTaskForm
from application.users.operations import user_can_do_operation

tasks = Blueprint('tasks', __name__)
 

@tasks.route("/add_task",methods=["GET",'POST'])
@login_required
def add_task():
    curr_user = current_user
    if not user_can_do_operation(operation='Add tasks',roles=curr_user.roles):
        return redirect(url_for("main.home"))
    form = AddTaskForm()

    if form.validate_on_submit():
        _name = form.name.data
        due_date = form.due_date.data
        priority = form.priority.data
        creator = current_user.id
        assigned_user = form.assigned_user.data
        description = form.description.data
        due_hour = str(form.due_hour.data).zfill(2) + ':' +str(form.due_minute.data).zfill(2)
        add_task_op(Task(
            id= None,
            name=_name,
            due_date = due_date,
            priority = priority,
            creator = creator,
            assigned_user = assigned_user,
            description=description,
            due_hour = due_hour,
            date_created=None
        ))
        return redirect(url_for('main.home'))
    return render_template('tasks/add_task.html',title="Add Task",form=form)

@tasks.route("/edit_task/<int:tid>",methods=["GET",'POST'])
@login_required
def edit_task(tid):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit tasks',roles=curr_user.roles):
        return redirect(url_for("main.home"))
        
    form = AddTaskForm()
    task = get_task(tid)
    if request.method == 'GET':
        form.name.data = task.name
        form.due_date.data = task.due_date
        form.priority.data = task.priority
        form.assigned_user.data = task.assigned_user.id
        form.description.data = task.description
        form.due_hour.data = task.due_hour[:2]
        form.due_minute.data = task.due_hour[3:]

    if form.validate_on_submit():
        _name = form.name.data
        due_date = form.due_date.data
        priority = form.priority.data
        assigned_user = form.assigned_user.data
        description = form.description.data
        due_hour = form.due_hour.data if form.due_hour.data else ''
        due_minute = form.due_minute.data if form.due_minute.data else ''
        due_hour = str(due_hour).zfill(2) + ':' +str(due_minute).zfill(2)
        edit_task_op(Task(
            id= tid,
            name=_name,
            due_date = due_date,
            priority = priority,
            creator = None,
            assigned_user = assigned_user,
            description=description,
            due_hour = due_hour if due_hour != '00:00' else '',
            date_created=None
        ))
        return redirect(url_for('tasks.task',tid=tid))
    return render_template('tasks/add_task.html',title="Edit Task",form=form)


@tasks.route("/tasks_list",methods=["GET"])
@login_required
def tasks_list():
    curr_user = current_user
    if not user_can_do_operation(operation='Check tasks list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    from datetime import date,timedelta
    current_date = date.today() 
    tasks_list = get_tasks()
    return render_template('tasks/tasks.html',title="Tasks",tasks=tasks_list,current_date=current_date,timedelta=timedelta)

@tasks.route("/task/<int:tid>",methods=["GET"])
@login_required
def task(tid):
    curr_user = current_user
    if not user_can_do_operation(operation='Check tasks list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    from datetime import date,timedelta
    current_date = date.today() 
    task = get_task(tid)
    all_tasks = []
    for task_ in get_tasks():
        if task_.id not in [s.id for s in task.awaitedTasks] and task_.id != tid:
            all_tasks.append(task_)
    return render_template('tasks/task.html',title="Task",all_tasks=all_tasks, task=task, current_date=current_date,timedelta=timedelta)

@tasks.route("/link_task_to_task/<int:waitingTaskId>",methods=["POST"])
@login_required
def link_task_to_task(waitingTaskId):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit tasks',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    awaitedTaskId = request.form.get('awaitedTaskId',None)
    if awaitedTaskId is not None:
        link_task_to_task_op(awaited_id=awaitedTaskId, waiting_id=waitingTaskId)
    return redirect(url_for('tasks.task',tid=waitingTaskId))

@tasks.route("/set_task_progress/<int:tid>",methods=["POST"])
@login_required
def set_task_progress(tid):
    curr_user = current_user
    if not user_can_do_operation(operation='Update task status',roles=curr_user.roles):
        return redirect(url_for("main.home"))
        
    status = request.form.get('status',None)
    progress = request.form.get('progress',0)
    if progress == '':
        progress = 0
    if status is not None:
        set_task_progress_op(tid=tid,status=status,progress=int(progress))
    return redirect(url_for('tasks.task',tid=tid))

@tasks.route("/postpone_task/<int:tid>",methods=["POST"])
@login_required
def postpone_task(tid):
    curr_user = current_user
    if not user_can_do_operation(operation='Postpone tasks',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    days = request.form.get('due_date_postpone',0)
    if days == '':
        days = 0
    postpone_task_op(tid=tid,days=int(days))
    return redirect(url_for('tasks.task',tid=tid))