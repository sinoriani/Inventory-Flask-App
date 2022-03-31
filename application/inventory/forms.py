from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, TextAreaField,IntegerField,FloatField,SelectField,TextAreaField
from wtforms.validators import DataRequired , Length, EqualTo, Optional,Email
from flask_wtf.html5 import NumberInput
from application.inventory.operations import get_families,get_tax_categories
from application.languages import LANG
from flask_login import current_user
from application.users.operations import email_exists


class AddProductForm(FlaskForm):
    name = StringField('Product name' , validators= [DataRequired() ,Length(max=150)])
    description = TextAreaField('Description' , validators= [DataRequired(),Length(max=250) ])
    tax_category = SelectField("Tax category",choices=get_tax_categories())
    #quantity = IntegerField('Quantity (Units)', validators = [DataRequired()],widget=NumberInput())
    unit = StringField("Unit",validators=[DataRequired()])
    price = FloatField('Selling price', validators= [DataRequired() ])
    estimated_cost = FloatField('Estimated cost', validators= [Optional() ])
    ean_upc = StringField('EAN/UPC (Barcode)', validators= [Optional(),Length(min=8,max=13) ])
    location = StringField('Location', validators= [Optional(),Length(max=25) ])
    family = SelectField("Family",choices=get_families())
    type_ = SelectField("Type", choices=[('Product','Product'), ('Service','Service')])
    submit = SubmitField('Add Product')

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        families =  get_families()
        self.family.choices = families
        tax_categories =  get_tax_categories()
        self.tax_category.choices = tax_categories
        lang = current_user.lang
        typeChoices = [('Product', LANG[lang].get("Product","Product")), ('Service', LANG[lang].get("Service","Service"))]
        self.type_.choices = typeChoices
        self.name.label.text = LANG[lang].get("Name","Name")
        self.tax_category.label.text = LANG[lang].get("Tax category","Tax category")
        self.description.label.text = LANG[lang].get("Description","Description")
        self.price.label.text = LANG[lang].get("Selling price","Selling price")
        self.estimated_cost.label.text = LANG[lang].get("Estimated cost","Estimated cost")
        self.ean_upc.label.text = LANG[lang].get("Barcode","Barcode")
        self.location.label.text = LANG[lang].get("Location","Location")
        self.family.label.text = LANG[lang].get("Family","Family")
        self.type_.label.text = LANG[lang].get("Type","Type")
        self.unit.label.text = LANG[lang].get("Unit","Unit")
        self.submit.label.text = LANG[lang].get("Confirm","Confirm")


class AddContactForm(FlaskForm):
    contact_name = StringField('Contact name' , validators= [DataRequired() ,Length(max=25)])
    contact_surname = StringField('Contact lastname' , validators= [DataRequired() ,Length(max=25)])
    contact_email = StringField('Contact email' , validators= [ Email(),Optional(),Length(max=120)  ])
    contact_phone = StringField('Contact phone number' , validators= [DataRequired() ,Length(min=8,max=20)])
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
        super(AddContactForm, self).__init__(*args, **kwargs)
        lang = current_user.lang
        self.contact_name.label.text = LANG[lang].get("Contact name","Contact name")
        self.contact_surname.label.text = LANG[lang].get("Contact lastname",'Contact lastname')
        self.contact_email.label.text = LANG[lang].get("Contact email","Contact email")
        self.contact_phone.label.text = LANG[lang].get("Contact phone number","Contact phone number")
        self.submit.label.text = LANG[lang].get("Confirm","Confirm")

    def validate_contact_email(self,contact_email):
        if email_exists(contact_email.data):
            raise ValidationError('That email is taken. Please choose a different one.')

class AddCompanyForm(FlaskForm):
    company_name = StringField('Company name' , validators= [DataRequired() ,Length(max=25)])
    company_matricule = StringField('Registration number' , validators= [Optional() ,Length(max=25)])
    company_remarks = TextAreaField('Remarks' , validators= [Optional() ])
    contact_name = StringField('Contact name' , validators= [DataRequired() ,Length(max=25)])
    contact_surname = StringField('Contact lastname' , validators= [DataRequired() ,Length(max=25)])
    contact_email = StringField('Contact email' , validators= [ Email(),Optional(),Length(max=120)  ])
    contact_phone = StringField('Contact phone number' , validators= [DataRequired() ,Length(min=8,max=20)])
    submit = SubmitField('Confirm')

    def validate_contact_email(self,contact_email):
        if email_exists(contact_email.data):
            raise ValidationError('That email is taken. Please choose a different one.')

    def __init__(self, *args, **kwargs):
        super(AddCompanyForm, self).__init__(*args, **kwargs)
        lang = current_user.lang
        self.company_name.label.text = LANG[lang].get("Company name","Company name")
        self.company_matricule.label.text = LANG[lang].get("Registration number","Registration number")
        self.contact_name.label.text = LANG[lang].get("Contact name","Contact name")
        self.contact_surname.label.text = LANG[lang].get("Contact lastname",'Contact lastname')
        self.contact_email.label.text = LANG[lang].get("Contact email","Contact email")
        self.contact_phone.label.text = LANG[lang].get("Contact phone number","Contact phone number")
        self.submit.label.text = LANG[lang].get("Confirm","Confirm")
        self.company_remarks.label.text = LANG[lang].get("Remarks","Remarks")
 
class AddFamilyForm(FlaskForm):
    name = StringField('Name' , validators= [DataRequired() ,Length(max=150)])
    parent_family = SelectField("Parent family",choices=get_families())
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
        super(AddFamilyForm, self).__init__(*args, **kwargs)
        families =  get_families()
        lang = current_user.lang
        self.parent_family.choices =  [("-1",LANG[lang].get("None","None"))] + families
        self.name.label.text = LANG[lang].get("Name","Name")
        self.parent_family.label.text = LANG[lang].get("Parent family","Parent Family")
        self.submit.label.text = LANG[lang].get("Confirm","Confirm")



class AddTaxCategoryForm(FlaskForm):
    name = StringField('Name' , validators= [DataRequired() ,Length(max=150)])
    value = FloatField("Value (%)",validators= [DataRequired()])
    submit = SubmitField('Confirm')

    def __init__(self, *args, **kwargs):
        super(AddTaxCategoryForm, self).__init__(*args, **kwargs)
        lang = current_user.lang
        self.name.label.text = LANG[lang].get("Name","Name")
        self.value.label.text = LANG[lang].get("Value (%)","Value (%)")

class EditRemarksForm(FlaskForm):
    remarks = TextAreaField('Remarks' , validators= [Optional() ])
