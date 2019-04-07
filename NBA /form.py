from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class FirePut(Form):
    Email = StringField('email', validators=[DataRequired()])
    Name = StringField('username', validators=[DataRequired()])
    Password = StringField('currentPassword', validators=[DataRequired()])
    Confirm = StringField('confirmPassword', validators=[DataRequired()])
