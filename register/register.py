from flask import Blueprint, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from bcrypt import hashpw, gensalt
from models import db, User

register_bp = Blueprint('register', __name__)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Register')

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password1.data
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Такое имя пользователя уже существует. Выберите другое')
            return redirect('/register')
        
        # Hash the password
        pw_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')  # Ensure it's a string
        
        new_user = User(username=username, password_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Аккаунт создан! Вы можете войти.')
        return redirect('/login')
    
    return render_template('register.html', form=form)
