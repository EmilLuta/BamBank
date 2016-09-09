from flask_wtf import Form
from wtforms import IntegerField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

from .models import User
from .password_services import PasswordService


class LoginForm(Form):
    username = StringField('Username', description='Username', validators=[DataRequired()])
    password = PasswordField('Password', description='Password', validators=[DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        else:
            if not PasswordService.decrypt_password(self.password.data, user.password):
                self.password.errors.append('Invalid password')
                return False

        return True


class RegisterForm(Form):
    username = StringField('Username', description='Username', validators=[Length(min=4, max=25)])
    password = PasswordField('Password', description='Password', validators=[
        DataRequired(), 
        Length(min=6),
        EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Confirm', description='Repeat Password')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()

        if user is not None:
            self.username.errors.append('Username is taken')
            return False

        return True

class TransactionForm(Form):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        user_id = int(kwargs['user_id'])
        self.user = User.query.get(user_id)
        self.users.choices = [(user.id, user.username) for user in User.query.all() if user.id != user_id]

    users = SelectField('Send to',
        coerce=int,
        description='Send to'
        )
    amount = IntegerField('Amount', 
        description='Amount',
        validators=[NumberRange(min=1)]
        )

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.user.balance < int(self.amount.data):
            self.amount.errors.append("You don't have this amount of money on your account.")
            return False
        
        return True