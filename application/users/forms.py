from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import DateField,SelectField,StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired , Length, Email, EqualTo, Optional
from flask_login import current_user 
from application.users.operations import user_exists,email_exists,get_roles


class AddUserForm(FlaskForm):
    username = StringField('Username *', validators = [DataRequired(), Length(min=2, max=20)] )
    email = StringField('Email *' , validators= [ Email(),DataRequired()  ])
    password = PasswordField('Password *', validators = [DataRequired()])
    role = SelectField(u'Role *',  validators = [DataRequired()])
    surname = StringField('Lastname *' , validators= [DataRequired() ])
    name = StringField('Name *' , validators= [DataRequired() ])
    tel1 = StringField('Tel 1')
    tel2 = StringField('Tel 2')
    submit = SubmitField('Create Account')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [ (r, r) for r in get_roles() ]
    
    def validate_username(self,username):
        if user_exists(username.data):
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        if email_exists(email.data):
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username_email = StringField('Username / Email' , validators= [DataRequired() ])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)] )
    email = StringField('Email' , validators= [ Email() ,Optional()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:
            if user_exists(username.data):
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self,email):
        if email.data != current_user.email:
            if email_exists(email.data):
                raise ValidationError('That email is taken. Please choose a different one.')

            
        
class RequestResetform(FlaskForm):
    email = StringField('Email' , validators= [DataRequired(), Email() ])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        if not email_exists(email.data):
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

