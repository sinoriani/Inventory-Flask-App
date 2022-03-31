from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
from application.affairs.models import Affair
from application.affairs.forms import AddAffairForm
from application.affairs.operations import get_affairs,set_affair_status_op,add_affair_op,get_affair,link_product_to_affair_op,edit_affair_op
from application.inventory.operations import get_companies, update_stock_op
from application.users.operations import user_can_do_operation
affairs = Blueprint('affairs', __name__)

@affairs.route('/add_affair/<string:type_>', defaults={'parent_id': None},methods=["GET",'POST'])
@affairs.route("/add_affair/<string:type_>/<int:parent_id>",methods=["GET",'POST'])
@login_required
def add_affair(type_,parent_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Add affairs',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    form = AddAffairForm()

    if form.validate_on_submit():
        _name = form.name.data
        description = form.description.data
        invoiced = request.form.get("invoiced",False) 
        affair = Affair(
                id= None,
                name=_name,
                date_created=None,
                description = description,
                products  = request.form.getlist("products"), #form.products.data,
                status = form.status.data,
                close_date = form.close_date.data,
                amount = form.amount.data,
                probability = form.probability.data,
                origin = form.origin.data,
                responsible_user = form.responsible_user.data,
                company = form.company.data,
                type=type_,
                invoice = True if invoiced == "on" else False,
                matricule = form.matricule.data if form.matricule.data else ''
        )
        affair_id = add_affair_op(affair,parent_id=parent_id)
        return redirect(url_for('affairs.affair',affair_id=affair_id))
    return render_template('affairs/add_affair1.html',title="Add Affair",form=form,type_=type_)


@affairs.route("/edit_affair/<int:affair_id>",methods=["GET",'POST'])
@login_required
def edit_affair(affair_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit affairs',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    form = AddAffairForm()

    affair = get_affair(affair_id)
    parent_affair_id = affair.parent_id
    if request.method == 'GET':
        form.name.data = affair.name
        form.status.data = affair.status
        form.close_date.data = affair.close_date
        form.responsible_user.data = affair.responsible_user
        form.probability.data = affair.probability
        form.amount.data = affair.amount
        form.description.data = affair.description
        form.origin.data = affair.origin    
        form.company.data = str(affair.company.id) if affair.company else "-1"
        form.matricule.data = affair.matricule

    if form.validate_on_submit():
        _name = form.name.data
        description = form.description.data
        invoiced = True if request.form.get("invoiced",False) == "on" else False 
        affair = Affair(
                id= affair_id,
                name=_name,
                date_created=None,
                description = description,
                products  = request.form.getlist("products"), #form.products.data,
                status = form.status.data if form.status.data else 'Done',
                close_date = form.close_date.data,
                amount = form.amount.data,
                probability = form.probability.data,
                origin = form.origin.data,
                responsible_user = form.responsible_user.data,
                company = form.company.data if str(form.company.data) != '-1' else None,
                invoice= invoiced,
                matricule=form.matricule.data if form.matricule.data else ''
        )

       

        edit_affair_op(affair)
        
        if parent_affair_id:
            affair_id = parent_affair_id
        return redirect(url_for('affairs.affair',affair_id=affair_id))
    return render_template('affairs/add_affair1.html',title="Edit Affair",form=form,invoiced = affair.invoice,type_= affair.type)


@affairs.route("/affair/<int:affair_id>",methods=["GET"])
@login_required
def affair(affair_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Check affairs list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    affair = get_affair(affair_id=affair_id)
    if affair.parent_id:
        return redirect(url_for('affairs.affair',affair_id=affair.parent_id))
    all_companies = get_companies()
    return render_template('affairs/affair.html',title="Affair",affair=affair,all_companies=all_companies)


@affairs.route("/affairs_list",methods=["GET"])
@login_required
def affairs_list():
    curr_user = current_user
    if not user_can_do_operation(operation='Check affairs list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    affairs_ = get_affairs()
    return render_template('affairs/affairs.html',title="Affairs",affairs=affairs_)


@affairs.route("/link_product_to_affair/<int:affair_id>",methods=["POST"])
@login_required
def link_product_to_affair( affair_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit affairs',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    else:        
        products = request.form.getlist('products')
        link_product_to_affair_op(affair_id, products)
    return redirect(url_for('affairs.affair',affair_id=affair_id))


@affairs.route("/set_affair_status/<int:affair_id>",methods=["POST"])
@login_required
def set_affair_status(affair_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Update affair status',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    status = request.form.get('status',None)
    if status is not None:
        if status == 'Done':
            update_stock_op(affair=get_affair(affair_id))
        set_affair_status_op(affair_id=affair_id,status=status)
        parent_affair_id = get_affair(affair_id=affair_id)
        if parent_affair_id.parent_id:
            affair_id = parent_affair_id.parent_id
    return redirect(url_for('affairs.affair',affair_id=affair_id))