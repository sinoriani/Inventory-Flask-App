from flask_wtf import FlaskForm
from wtforms import DateField,StringField, SubmitField, ValidationError, TextAreaField,IntegerField,FloatField,SelectField,TextAreaField
from wtforms.validators import DataRequired , Length, EqualTo, Optional
from flask_wtf.html5 import NumberInput
from flask_login import current_user
from application.languages import LANG
from application.users.operations import get_employees

class AddTaskForm(FlaskForm):
    name = StringField('Task name' , validators= [DataRequired() ,Length(max=150)])
    description = TextAreaField('Description' , validators= [DataRequired(),Length(max=250) ])
    assigned_user = SelectField("Assigned user")
    due_date = DateField('Due date',format='%m/%d/%Y', validators= [DataRequired()])
    priority = SelectField('Priority',choices=[('Low','Low'), ('Medium','Medium'), ('High','High')], validators= [DataRequired()])
    due_hour = IntegerField('Hour', validators = [Optional()],widget=NumberInput(min=0,max=23))
    due_minute = IntegerField('Hour', validators = [Optional()],widget=NumberInput(min=0,max=59))
    submit = SubmitField('Add Task')

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        employees =  [ (str(employee.id), str(employee.name) + ' ' + str(employee.surname if employee.surname else '' )) for employee in  get_employees()]
        self.assigned_user.choices = employees
        lang = current_user.lang
        choices =[('Low',LANG[lang].get("Low","Low")), ('Medium',LANG[lang].get("Medium","Medium")), ('High',LANG[lang].get("High","High"))]
        self.priority.choices = choices
        self.name.label.text = LANG[lang].get("Name","Name")
        self.description.label.text = LANG[lang].get("Description","Description")
        self.assigned_user.label.text = LANG[lang].get("Agent","Assigned user")
        self.due_date.label.text = LANG[lang].get("Due date","Due date")
        self.priority.label.text = LANG[lang].get("Priority","Priority")
        self.due_hour.label.text = LANG[lang].get("Hour","Hour")
        self.due_minute.label.text = LANG[lang].get("Minute","Minute")
        self.submit.label.text = LANG[lang].get("Confirm","Confirm")
