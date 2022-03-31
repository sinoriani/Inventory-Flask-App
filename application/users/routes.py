from flask import render_template, flash, redirect, url_for, request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from application import  bcrypt
from application.users.models import User
from application.users.operations import get_presence_history, add_presence_op,add_role_op,user_can_do_operation,create_user, get_user, get_users, get_operations_for_roles, remove_operation_from_role_op, link_operation_to_role_op
from application.users.forms import  LoginForm, UpdateAccountForm, RequestResetform, ResetPasswordForm,AddUserForm
from application.users.utils import save_picture,send_reset_email
import datetime
import json
users = Blueprint('users',__name__)



@users.route("/register", methods=["GET", "POST"])
def register():
    curr_user = current_user
    if not user_can_do_operation(operation='Add users',roles=curr_user.roles):
        return redirect(url_for("main.home"))
        
    form = AddUserForm()

    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            tel1 = form.tel1.data
            tel2 = form.tel2.data
            numsTel = [tel1]
            if tel2 != ""  and tel2 != None:
                numsTel.append(tel2)
            email = form.email.data #if form.email.data != "" else None
            username = form.username.data
           
            #try:
            #    dt = form.birth_date.data.strftime('%x')
            #except:
            #    dt = None
            
            role = form.role.data

            if create_user(username=username,email= email,password=hashed_password,
                        role=role,surname= form.surname.data,name= form.name.data,
                        numerosTel=numsTel) != False:
                flash('Account created!','success')
                with open('log2.log','a+') as f:
                    f.write(f"[{datetime.datetime.now()}] Compte créé {email} \n\n")
                return redirect(url_for("main.home"))
            else:
                flash('An error occured.','danger')
        except Exception as e:
            with open('log2.log','a+') as f:
                f.write(f"[{datetime.datetime.now()}] erreur creation patient : ERROR : {e} \n\n")

    return render_template("register.html", title='Create Account', form=form,page='register')

@users.route("/login", methods=["GET","POST"])
def login():
    print('\n\n',current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(username=form.username_email.data,email=form.username_email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Successfully logged in!",'success')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful, Please check email and password",'danger')
    return render_template("login.html" , title='Login',form = form)
    
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/reset_password", methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetform()
    if form.validate_on_submit():
        user = get_user(email=form.email.data)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for("users.login"))
    return render_template('reset_request.html',title='Reset Password',form=form)

    
@users.route("/change_password", methods=["GET","POST"])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.update_password(hashed_password)
        
        flash(f'Your password has been updated! You are now able to login','success')
        return redirect(url_for('users.account'))
    return render_template('reset_token.html',title='Change Password',form=form)

@users.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.update_password(hashed_password)
        
        flash(f'Your password has been updated! You are now able to login','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)



@users.route("/users_list", methods=["GET","POST"])
@login_required
def users_list():
    curr_user = current_user
    if not user_can_do_operation(operation='Check users list',roles=curr_user.roles):
        return redirect(url_for("main.home"))
    users = get_users()
    return render_template("users.html" , title='Users',users = users)



@users.route("/operation_roles", methods=["GET","POST"])
@login_required
def operation_roles():
    curr_user = current_user
    if 'Admin' not in curr_user.roles:
        flash('No Access','danger')
        return redirect(url_for('main.home'))
    operation_roles = get_operations_for_roles()
    return render_template("operation_roles.html" , title='Operation Roles',operation_roles = operation_roles)


@users.route("/link_operation_to_role/<string:role>", methods=["GET","POST"])
@login_required
def link_operation_to_role(role):
    curr_user = current_user
    if 'Admin' not in curr_user.roles:
        flash('No Access','danger')
        return redirect(url_for('main.home'))
    operation = request.form.get('operation',None)
    if operation:
        link_operation_to_role_op(operation=operation,role_name=role)
    return redirect(url_for('users.operation_roles'))

@users.route("/remove_operation_from_role/<string:role>-<string:operation>", methods=["POST"])
@login_required
def remove_operation_from_role(role,operation):
    curr_user = current_user
    if 'Admin' not in curr_user.roles:
        flash('No Access','danger')
        return redirect(url_for('main.home'))
    
    remove_operation_from_role_op(operation=operation,role_name=role)
    return redirect(url_for('users.operation_roles'))


@users.route("/add_role", methods=["POST"])
@login_required
def add_role():
    curr_user = current_user
    if 'Admin' not in curr_user.roles:
        flash('No Access','danger')
        return redirect(url_for('main.home'))
    role = request.form.get('role',None)
    if role:
        add_role_op(role=role)
    return redirect(url_for('users.operation_roles'))


@users.route("/add_presence", methods=["GET","POST"])
@login_required
def add_presence():
    curr_user = current_user
    if not user_can_do_operation(operation='Add presence',roles=curr_user.roles):
        flash('No Access','danger')
        return redirect(url_for('main.home'))
    users = get_users()

    if request.method == "POST":
        users_presence = {}
        for key,value in request.form.items():
            if 'date' in key or 'csrf_token' in key:
                continue
            uid, input_ = key.split("-")[0], key.split("-")[1]
            if uid not in users_presence:
                users_presence[uid] = {}
            users_presence[uid][input_] = value if value != "" in input_ else "00"
        add_presence_op(users_presence=users_presence,dat=request.form.get('date'))
    return render_template("add_daily_presence.html" , title='Add presence',users=users)


@users.route("/presence_history", methods=["GET","POST"])
@login_required
def presence_history():
    curr_user = current_user
    if not user_can_do_operation(operation='Add presence',roles=curr_user.roles):
        flash('No Access','danger')
        return redirect(url_for('main.home'))

    if request.method == "POST":
        dat = request.form.get('date',str(datetime.date.today()))
    else:
        dat = str(datetime.date.today())
    history = get_presence_history(dat=dat)
    return render_template("add_daily_presence.html" , title='Presence History',history=history, dat=dat)