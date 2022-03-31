from flask_wtf import FlaskForm
from wtforms import BooleanField,DateField,Form, widgets, SelectMultipleField,StringField, SubmitField, ValidationError, TextAreaField,IntegerField,FloatField,SelectField,TextAreaField
from wtforms.validators import DataRequired , Length, Optional
from flask_wtf.html5 import NumberInput
from application.inventory.operations import get_products, get_companies,get_products_for_company_op
from application.users.operations import get_employees
from flask_login import current_user
from application.languages import LANG


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddAffairForm(FlaskForm):
    #type_ = SelectField('Type', choices=[('-','Select a type'), ('Sale','Sale'), ('Purchase','Purchase')])
    name = StringField('Name' , validators= [DataRequired() ,Length(max=150)])
    matricule = StringField('Plate' , validators= [Optional() ,Length(max=20)])
    description = TextAreaField('Description' , validators= [DataRequired(),Length(max=250) ])
    status = SelectField('Status', validators=[Optional()])
    close_date = DateField('Close date',format='%m/%d/%Y',validators=[Optional()])
    amount = FloatField('Amount', validators= [Optional() ])
    probability = FloatField('Selling Probability', validators= [Optional()])
    origin = StringField('Origin', validators= [Optional(),Length(max=100) ])
    responsible_user = SelectField("Agent in charge", validators=[DataRequired()])
    company = SelectField("Company",validators=[Optional()])
    #products  = MultiCheckboxField('Products',validators = [DataRequired()])
    submit = SubmitField('Validate')

    def __init__(self, *args, **kwargs):
        super(AddAffairForm, self).__init__(*args, **kwargs)
        companies = get_companies()
        curr_user= current_user
        statuses = [
            ('Waiting',LANG[curr_user.lang].get('Waiting','Waiting')),
            ('In Progress',LANG[curr_user.lang].get('In Progress','In Progress')), 
            ('Done',LANG[curr_user.lang].get('Done','Done'))
        ]
        self.status.choices = statuses
        #self.products.choices = [(str(product.id),product.name) for product in  get_products_for_company_op(company_id=companies[-1].id)]
        self.responsible_user.choices = [(str(user.id),user.name) for user in  get_employees()]
        self.company.choices = [('-1',LANG[curr_user.lang].get('Pick a company','Pick a company'))] +[(str(company.id),company.name) for company in  companies[::-1]]
        self.name.label.text = LANG[curr_user.lang].get('Name','Name')
        self.description.label.text = LANG[curr_user.lang].get('Description','Description')
        self.status.label.text = LANG[curr_user.lang].get('Status','Status')
        self.close_date.label.text = LANG[curr_user.lang].get('Close date','Close date')
        self.amount.label.text = LANG[curr_user.lang].get('Amount','Amount')
        self.probability.label.text = LANG[curr_user.lang].get('Selling probability','Selling Probability')
        self.responsible_user.label.text = LANG[curr_user.lang].get('Agent in charge','Agent in charge')
        self.company.label.text = LANG[curr_user.lang].get('Company','Company')
        self.origin.label.text = LANG[curr_user.lang].get('Origin','Origin')
        self.matricule.label.text = LANG[curr_user.lang].get('Plate','Plate')


    def validate_type_(self,type_):
        if type_.data == '-':
            raise ValidationError('Please select a type for the affair.')
    
