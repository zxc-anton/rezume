from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Форма вход в админ"""
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class AddRezume(FlaskForm):
    """Форма для добавления резюме"""
    username = StringField('Ваше ФИО', validators=[DataRequired()])
    citi = StringField('Ваш город', validators=[DataRequired()])
    user_number = StringField('Ваш номер', validators=[DataRequired()])
    user_email = EmailField('Ваш email', validators=[DataRequired()])
    salary = StringField('Зарплата', validators=[DataRequired()])
    progrm_lang = StringField('Ваши языки', validators=[DataRequired()])
    experience = StringField('Ваш опыт работы', validators=[DataRequired()])
    body = TextAreaField('Напишите о себе', validators=[DataRequired()])
    remote_work = BooleanField('Готовы к удаленой работе?')
    submit = SubmitField('Отправить')
