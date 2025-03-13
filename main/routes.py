
from urllib.parse import urlsplit
from flask import render_template, request, redirect, url_for, flash

from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from main import app, db
from main.model import Admin, rezume, no_checked_rezume
from main.forms import LoginForm, AddRezume


def get_vacancies(offset=0, table = rezume):

    rezume_count = db.session.query(table).count()
    result = db.session.query(rezume).offset(offset).limit(10).all()

    return result , rezume_count

@app.route('/index')
@app.route('/')
def index():
    try:
        key = request.args.get('key')
        if current_user.is_authenticated:
            if key and key.isdigit():
                posts, count = get_vacancies(offset=int(key)*10, table=no_checked_rezume)
            else:
                posts, count = get_vacancies(table=no_checked_rezume)
            return render_template('index.html', posts=posts, pagins=count)
        else:
            if key and key.isdigit():
                posts, count = get_vacancies(offset=int(key)*10)
            else:
                posts, count = get_vacancies()
            return render_template('index.html', posts=posts, pagins=count)
    except:
        return render_template('index.html')


@app.route('/rezume')
def show_rezume():
    try:
        id = int(request.args.get('id'))
        user = db.session.query(rezume).filter(rezume.id == id).one()
        return render_template('rezume.html', user=user)
    except Exception as e:
        return "Нет"

@app.route('/admin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        admin= db.session.scalar(sa.select(Admin).where(Admin.login == login))
        if admin is None or not admin.check_password(password):
            #return redirect(url_for('login'))
            return "3"
        login_user(admin, remember=True)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('admin.html', form=form)

@app.route('/check_rezume', methods=['GET', 'POST'])
@login_required
def check_rezume():
    id = int(request.args.get('id'))
    if id:
        try:
            user = db.session.query(no_checked_rezume).filter(rezume.id == id).first()
            return render_template('rezume.html', user=user, admin='True')
        except:
            flash('Возникли ошибка', category='error')
            redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    

    return "Да"

@app.route('/add_rezume', methods=['GET', 'POST'])
def add_rezume():
    form = AddRezume()
    if form.validate_on_submit():
        username = form.username.data
        citi = form.citi.data
        user_number = form.user_number.data
        user_email = form.user_email.data
        salary = form.salary.data
        progrm_lang = form.progrm_lang.data
        experience = form.experience.data
        body = form.body.data
        remote_work = form.remote_work.data

        try:
            # Проверяем, существует ли резюме с таким email
            statement = sa.select(no_checked_rezume).where(no_checked_rezume.user_email == user_email)
            result = db.session.scalars(statement).first()
            if result is not None:
                flash('Резюме с таким email уже существует', category='error')
                return  "ecnm"
            #redirect(url_for('index'))

            # Создаём новое резюме
            rezume_cl = no_checked_rezume(
                username=username,
                citi=citi,
                user_number=user_number,
                user_email=user_email,
                salary=salary,
                progrm_lang=progrm_lang,
                experience=experience,
                body=body,
                remote_work=remote_work,
                status = 'False'
            )
            db.session.add(rezume_cl)
            db.session.commit()
            flash('Ваше резюме добавлено', category='success')
            return "добаввлено"
        #redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()  # Откатываем изменения в случае ошибки
            flash(f'Возникли ошибки. Повторите отправку формы: {e}', category='error')
            return "ОШибка"
        #redirect(url_for('index'))

    return render_template('add_rezume.html', form = form)

@app.route('/aprove_rezume', methods=['GET', 'POST'])
@login_required
def aprove_rezume():
    pass

@app.route('/aprove_rezume', methods=['GET', 'POST'])
@login_required
def reject_rezume():
    pass