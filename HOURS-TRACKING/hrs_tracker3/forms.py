from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.validators import DataRequired, Length, EqualTo

class RecordHoursForm(FlaskForm):
    # teacher_id = IntegerField('Teacher ID', validators=[DataRequired()])
    # class_id = IntegerField('Class ID', validators=[DataRequired()])
    hours = IntegerField('Hours Taught', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Record Hours')
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
class ManageClassForm(FlaskForm):
    subject = SelectField('Subject', choices=['math,english'], validators=[DataRequired()])  # Choices will be set later
    class_name = StringField('Class Name', validators=[DataRequired()])
    hours = IntegerField('Number of Hours', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

