from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_login import login_required,current_user
from application.inventory.forms import AddContactForm,EditRemarksForm,AddTaxCategoryForm,AddFamilyForm,AddProductForm,AddCompanyForm
from application.inventory.operations import remove_contact_from_company_op,link_contact_to_company_op, edit_tax_op,get_tax_categories,get_families, add_tax_category_op, add_family_op,edit_product_op,get_products_for_company_op,get_companies_for_product_op,link_company_to_product_op, add_product_op, get_products, get_product, add_company_op, get_companies, get_company
from application.inventory.models import Product,Service,Contact
from application.users.operations import user_can_do_operation
from application.affairs.operations import get_affairs
inventory = Blueprint('inventory', __name__)

@inventory.route("/add_product",methods=["GET",'POST'])
@login_required
def add_product():
    curr_user = current_user
    if not user_can_do_operation(operation='Add products',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    form = AddProductForm()

    if form.validate_on_submit():
        _name = form.name.data
        price = form.price.data
        family = form.family.data
        description = form.description.data
        tax_category = form.tax_category.data
        estimated_cost = form.estimated_cost.data
        location = form.location.data
        ean_upc = form.ean_upc.data
        unit = form.unit.data
        if form.type_.data == 'Product':
            product = Product(
            id= None,
            name=_name,
            price=price,
            family=family,
            description = description,
            tax_category = tax_category,
            estimated_cost = estimated_cost,
            location = location,
            ean_upc = ean_upc,
            unity=unit
        )
        else:
            product = Service(
            id= None,
            name=_name,
            price=price,
            family=family,
            description = description,
            tax_category = tax_category,
            estimated_cost = estimated_cost,
            unity=unit
        )
        add_product_op(product)
        return redirect(url_for('main.home'))
    return render_template('inventory/add_product.html',title="Add Product",form=form)

@inventory.route("/edit_product/<int:pid>",methods=["GET",'POST'])
@login_required
def edit_product(pid):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit products',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    form = AddProductForm()

    product = get_product(pid)
    if request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.family.data = product.family
        form.description.data = product.description
        form.tax_category.data = product.tax_category
        form.estimated_cost.data = product.estimated_cost
        form.unit.data = product.unity
        if product.type == "Product":
            form.location.data = product.location
            form.ean_upc.data = product.ean_upc

    if form.validate_on_submit():
        _name = form.name.data
        price = form.price.data
        family = form.family.data
        description = form.description.data
        tax_category = form.tax_category.data
        estimated_cost = form.estimated_cost.data
        location = form.location.data
        ean_upc = form.ean_upc.data
        unit = form.unit.data
        edit_product_op(Product(
            id= pid,
            name=_name,
            price=price,
            family=family,
            description = description,
            tax_category = tax_category,
            estimated_cost = estimated_cost,
            location = location,
            ean_upc = ean_upc,
            unity=unit
        ))
        return redirect(url_for('inventory.product',pid=pid))
    return render_template('inventory/add_product.html',title="Edit Product",form=form)

@inventory.route("/products",methods=["GET"])
@login_required
def products():
    curr_user = current_user
    if not user_can_do_operation(operation='Check products list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    products_list = get_products()
    return render_template('inventory/products.html',title="Products",products=products_list)

@inventory.route("/product/<int:pid>",methods=["GET"])
@login_required
def product(pid):
    curr_user = current_user
    if not user_can_do_operation(operation='Check products list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    item = get_product(pid)
    item.companies = get_companies_for_product_op(item.id)
    all_companies = []
    for company in get_companies():
        if company.id not in [s.id for s in item.companies]:
            all_companies.append(company)
    return render_template('inventory/product.html',title="Product",product=item,all_companies=all_companies)

@inventory.route("/add_company",methods=["GET",'POST'])
@login_required
def add_company():
    curr_user = current_user
    if not user_can_do_operation(operation='Add company',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    curr_user = current_user
    if 'Admin' not in curr_user.roles:
        flash('No Access','danger')
        return redirect(url_for('main.home'))

    form = AddCompanyForm()

    if form.validate_on_submit():
        add_company_op(
            company_name= form.company_name.data,
            contact_name= form.contact_name.data,
            contact_surname= form.contact_surname.data,
            contact_email = form.contact_email.data,
            contact_phone = form.contact_phone.data,
            company_remarks= form.company_remarks.data,
            matricule=form.company_matricule.data
        )
        return redirect(url_for('main.home'))
    return render_template('inventory/add_company.html',title="Add company",form=form)

@inventory.route("/companies",methods=["GET"])
@login_required
def companies():
    curr_user = current_user
    if not user_can_do_operation(operation='Check companies list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    companies_list = get_companies()
    return render_template('inventory/companies.html',title="companies",companies=companies_list)

@inventory.route("/company/<int:sid>",methods=["GET","POST"])
@login_required
def company(sid):
    curr_user = current_user
    if not user_can_do_operation(operation='Check companies list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    item = get_company(sid)
    item.products = get_products_for_company_op(item.id)
    all_products = []

    item.affairs = get_affairs(company_id=sid)

    
    for product in get_products():
        if product.id not in [p.id for p in item.products]:
            all_products.append(product)

    contactForm = AddContactForm()
    if contactForm.validate_on_submit():
        link_contact_to_company_op(company_id=sid,contact=Contact(
            name=contactForm.contact_name.data,
            surname=contactForm.contact_surname.data,
            email=contactForm.contact_email.data,
            numsTel=[contactForm.contact_phone.data]
        ))
        return redirect(url_for('inventory.company',sid=sid))
    
    return render_template('inventory/company.html',title="company",company=item,all_products=all_products,contactForm=contactForm)


@inventory.route("/update_company_remarks/<int:company_id>",methods=["POST"])
@login_required
def update_company_remarks(company_id):
    item = get_company(company_id=company_id)
    item.update_remarks(request.form.get('remarks','').strip())
    return redirect(url_for("inventory.company",sid=company_id))


@inventory.route("/link_company_to_product/<int:product_id>",methods=["POST"])
@login_required
def link_company_to_product( product_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit company',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    else:        
        company_id = request.form.get('company_id',None)
        if company_id is not None:
            link_company_to_product_op(company_id, product_id)
    return redirect(url_for('inventory.product',pid=product_id))


@inventory.route("/remove_contact_from_company/<int:company_id>/<int:contact_id>",methods=["POST"])
@login_required
def remove_contact_from_company( company_id,contact_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit company',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    remove_contact_from_company_op(company_id=company_id,contact_id=contact_id)
       
    return redirect(url_for('inventory.company',sid=company_id))

@inventory.route("/link_product_to_company/<int:company_id>",methods=["POST"])
@login_required
def link_product_to_company( company_id):
    curr_user = current_user
    if not user_can_do_operation(operation='Edit company',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    else:        
        product_id = request.form.get('product_id',None)
        if product_id is not None:
            link_company_to_product_op(company_id, product_id)
    return redirect(url_for('inventory.company',sid=company_id))

@inventory.route("/get_products_for_company",methods=["POST"])
@login_required
def get_products_for_company( ):
    import json
    curr_user = current_user
    if not user_can_do_operation(operation='Check companies list',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    else:        
        try:
            company_id =request.json['company_id']
        except:
            company_id = None
        products  = get_products_for_company_op(company_id=company_id)
        products = [(str(p.id), p.name + " (" + str(p.price) + " DT/" + p.unity +")", str(p.price)) for p in products]
    return json.dumps(products)

@inventory.route("/add_family",methods=["GET",'POST'])
@login_required
def add_family():
    curr_user = current_user
    if not user_can_do_operation(operation='Update parameters',roles=curr_user.roles):
        return redirect(url_for("main.home"))


    form = AddFamilyForm()

    if form.validate_on_submit():
        add_family_op(
            name= form.name.data,
            parent_family= form.parent_family.data
        )
        return redirect(url_for('main.home'))
    return render_template('inventory/add_family.html',title="Add family",form=form)

@inventory.route("/add_tax_category",methods=["GET",'POST'])
@login_required
def add_tax_category():
    curr_user = current_user
    if not user_can_do_operation(operation='Update parameters',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    form = AddTaxCategoryForm()

    if form.validate_on_submit():
        add_tax_category_op(
            name= form.name.data,
            value= form.value.data
        )
        return redirect(url_for('main.home'))
    return render_template('inventory/add_tax_category.html',title="Add Tax Category",form=form)

@inventory.route("/parameters",methods=["GET"])
@login_required
def parameters():
    curr_user = current_user
    if not user_can_do_operation(operation='Update parameters',roles=curr_user.roles):
        return redirect(url_for("main.home"))

    tax_categories = get_tax_categories(to_edit=True)
    families = get_families()
    
    return render_template('inventory/parameters.html',title="Parameters",tax_categories=tax_categories,families=families)

@inventory.route("/edit_tax/<string:name>",methods=['POST'])
@login_required
def edit_tax(name):
    curr_user = current_user
    if not user_can_do_operation(operation='Update parameters',roles=curr_user.roles):
        return redirect(url_for("main.home"))


    value = request.form.get('tax',0)
    if value == '':
        value = 0
    edit_tax_op(name=name,value=float(value))    
    return redirect(url_for('inventory.parameters'))