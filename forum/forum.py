from flask import Blueprint, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from models import db, Message
from time import time
from datetime import datetime

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')

# Определяем blueprint
forum_bp = Blueprint('forum', __name__)

class MessageForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    content = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить сообщение')

@forum_bp.route('/', methods=['GET', 'POST'])
def forum():
    message_form = MessageForm()
    if message_form.validate_on_submit():
        new_message = Message(
            time=int(time()),  # Убедитесь, что это установлено правильно
            content=message_form.content.data,
            author=message_form.username.data  # Сохраняем имя пользователя
        )
        db.session.add(new_message)
        db.session.commit()
        
        flash('Сообщение успешно отправлено!', 'success')
        return redirect('/')

    # Измените порядок извлечения сообщений
    messages = Message.query.order_by(Message.time.desc()).all()  # Сортируем по времени в порядке убывания
    return render_template('forum.html', message_form=message_form, messages=messages, format_timestamp=format_timestamp)
