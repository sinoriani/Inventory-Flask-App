from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
from application.tasks.operations import get_tasks
from application.affairs.operations import get_affairs, get_affair_years
from application.users.operations import user_can_do_operation
from application.languages import LANG

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    from datetime import timedelta,date
    curr_user = current_user
    current_date = date.today()
    if curr_user.is_authenticated:
        tasks = get_tasks(assigned_user_id=current_user.id)
        affairs = get_affairs(responsible_user_id=current_user.id)
        stats = {
            'nb_late_tasks':sum([1 if t.due_date < current_date else 0 for t in tasks]),
            'nb_tasks':len(tasks),
            'nb_affairs':len(affairs)
        }
    else:
        tasks  = stats = affairs = None

    return render_template('index.html',affairs=affairs,stats=stats,tasks=tasks,timedelta=timedelta,current_date=current_date)



@main.route("/report/<string:type_>",methods=['GET','POST'])
@login_required
def daily_report(type_):
    from calendar import month_name
    from datetime import timedelta,date
    curr_user = current_user
    if not user_can_do_operation(operation='Check daily report',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    if request.method == "POST":
        if type_ == "daily":
            date_picked = request.form.get('date',None)
            if date_picked and date_picked != "":
                affairs = get_affairs(dat=date_picked,with_products=True)
        elif type_ == "monthly":
            month = request.form.get('month',None)
            year = request.form.get('year',None)
            date_picked = LANG[curr_user.lang].get(month_name[int(month)],month_name[int(month)]) + " " + year
            if month and year and month != "" and year != "":
                affairs = get_affairs(month=month,year=year,with_products=True)
    else:
        date_picked = date.today()
        if type_ == "daily":
            affairs = get_affairs(dat=str(date_picked),with_products=True)
            date_picked = str(date_picked)
        elif type_ == "monthly":
            affairs = get_affairs(month=date_picked.month,year=date_picked.year,with_products=True)
            date_picked = LANG[curr_user.lang].get(month_name[date_picked.month],month_name[date_picked.month]) + " " + str(date_picked.year)
        

    try:
        d = date_picked.split('-')
        date_picked = date(year=int(d[0]),month=int(d[1]),day=int(d[2]))
        date_picked = f"{date_picked.day} { LANG[curr_user.lang].get(month_name[date_picked.month],month_name[date_picked.month]) } {date_picked.year} "
    except:
        print("error date picked report ")

    

    in_amount = out_amount = prevision_out_amount = prevision_in_amount =  0
    for a in affairs:
        if a.type == "Sale":
            if a.status == "Done":
                in_amount += a.amount if a.amount else 0
            else:
                prevision_in_amount += a.amount if a.amount else 0
        else:
            if a.status == "Done":
                out_amount += a.amount if a.amount else 0
            else:
                prevision_out_amount += a.amount if a.amount else 0
    amounts = {
        "in_amount":in_amount,
        "out_amount":out_amount,
        "prevision_out_amount":prevision_out_amount,
        "prevision_in_amount":prevision_in_amount
    }

    years = [ str(y[0]) for y in  get_affair_years()]
    return render_template('reports/daily_report.html',title= type_.capitalize()+ " Report" ,years=years,affairs=affairs,date_picked=date_picked,amounts=amounts)

