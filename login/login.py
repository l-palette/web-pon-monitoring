from flask import Blueprint, render_template, redirect, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from bcrypt import checkpw
from models import db, User

login_bp = Blueprint('login', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session['username'] = username
            flash('Успешная авторизация.')
            return redirect('/')
        
        flash('Неверное имя пользователя или пароль.')
    
    return render_template('login.html', form=form)
