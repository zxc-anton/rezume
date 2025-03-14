
from urllib.parse import urlsplit
from flask import render_template, request, redirect, url_for, flash

from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from main import app, db
from main.model import Admin, rezume
from main.forms import LoginForm, AddRezume


def get_vacancies(args, offset=0, admin = False):
    """Получение классов резюме"""
    query = db.session.query(rezume)
    print(args)
    if args[0]:
        query.filter(rezume.progrm_lang.ilike(f'%{args[0]}%'))

    if args[1]:
        query.filter(rezume.citi.ilike(f'%{args[1]}%'))

    if args[2]:
        query.filter(rezume.salary >= int(args[2]))
        print(query)
    if args[3]:
        query.filter(rezume.salary <= int(args[3]))

    if args[4]:
        query.filter(rezume.experience >= int(args[4]))


    if admin:
        rezume_count = query.where(rezume.status == 'no_checked').count()
        result = query.where(rezume.status == 'no_checked').offset(offset).limit(10).all()
    else:
        rezume_count = query.where(rezume.status == 'true').count()
        result = query.where(rezume.status == 'true').offset(offset).limit(10) 
    print(result)
    if rezume_count == 0 or rezume_count is None:
        return False, 0
    return result , rezume_count

@app.route('/index')
@app.route('/')
def index():
    """Вывод главной страницы"""
    try:
        key = request.args.get('key')
        programming_languages = request.args.get('programming_languages')
        city = request.args.get('city')
        min_salary = request.args.get('min_salary')
        max_salary = request.args.get('max_salary')
        experience = request.args.get('experience')
        value = [programming_languages, city, min_salary, max_salary, experience]
        if current_user.is_authenticated:
            admin = True
        else:
            admin = False

        if key and key.isdigit():
            posts, count = get_vacancies(value, offset=int(key)*10, admin=admin, )
        else:
            posts, count = get_vacancies(value, admin=admin)

        if count > 9:
            return render_template('index.html', posts=posts, pagins=count, admin = admin) 
        return render_template('index.html', posts=posts, pagins=round(count/10), admin = admin)
    
    except Exception as e:
        flash('Возникла ошибка', category='error')
        print(1, e)
        return render_template('index.html')


@app.route('/rezume')
def show_rezume():
    """Вывод резюме на отдельной странице"""
    try:
        rezume_id = request.args.get('id')
        if rezume_id and rezume_id.isdigit():
            user = db.session.query(rezume).filter(rezume.id == rezume_id).first()
            if user.status != 'true':
                if current_user.is_authenticated:
                    return render_template('rezume.html', user=user)
                return render_template(url_for('index'))
            return render_template('rezume.html', user=user)
        else:
            return redirect(url_for('index'))
    except Exception as e:
        print(e)
        flash("Возникла ошибка", category='error')
        return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            admin= db.session.scalar(sa.select(Admin).where(Admin.login == login))
            if admin is None or not admin.check_password(password):
                return redirect(url_for('login'))
            login_user(admin, remember=True)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('admin.html', form=form)
    except:
        flash('Возникла ошибка', category='error')
        return redirect(url_for('index'))

@app.route('/add_rezume', methods=['GET', 'POST'])
def add_rezume():
    try:
        form = AddRezume()
        if form.validate_on_submit():
            username = form.username.data
            citi = form.citi.data
            user_number = form.user_number.data
            user_email = form.user_email.data
            salary = int(form.salary.data)
            progrm_lang = form.progrm_lang.data
            experience = int(form.experience.data)
            body = form.body.data
            remote_work = form.remote_work.data

            try:
                # Проверяем, существует ли резюме с таким email
                statement = sa.select(rezume).where(rezume.user_email == user_email)
                result = db.session.scalars(statement).first()
                if result is not None or result:
                    flash('Резюме с таким email уже существует', category='error')
                    return  redirect(url_for('add_rezume'))

                # Создаём новое резюме
                rezume_cl = rezume(
                    username=username,
                    citi=citi,
                    user_number=user_number,
                    user_email=user_email,
                    salary=salary,
                    progrm_lang=progrm_lang,
                    experience=experience,
                    body=body,
                    remote_work=remote_work,
                    status = 'no_checked'
                )
                db.session.add(rezume_cl)
                db.session.commit()
                flash('Ваше резюме добавлено', category='success')
                return redirect(url_for('index'))
            except Exception as e:
                print('error',e)
                db.session.rollback()  # Откатываем изменения в случае ошибки
                flash(f'Возникли ошибки. Повторите отправку формы: {e}', category='error')
                return redirect(url_for('index'))

        return render_template('add_rezume.html', form = form)
    except Exception as e:
        flash('Возникла ошибка', category='error')
        return redirect(url_for('index'))
    

@app.route('/aprove_rezume', methods=['GET', 'POST'])
@login_required
def aprove_rezume():
    rezume_id = request.args.get('id')
    if rezume_id and rezume_id.isdigit():
        query = db.session.query(rezume).filter(rezume.id == rezume_id).first()
        if query.status == 'no_checked':
            query.status = 'true'
            db.session.commit()
        elif query.status == 'true':
            print(url_for('show_rezume', id=rezume_id))
            return redirect(url_for('show_rezume', id=rezume_id))
        else:
            return redirect(url_for('index'))
        
    flash('Возникла ошибка', category='error')
    return redirect(url_for('index'))

@app.route('/reject_rezume', methods=['GET', 'POST'])
@login_required
def reject_rezume():
    rezume_id = request.args.get('id')
    if rezume_id and rezume_id.isdigit():
        query = db.session.query(rezume).filter(rezume.id == rezume_id).first()
        if query.status == 'no_checked':
            query.status == 'false'
            db.session.commit()
        elif query.status == 'true':
            return redirect(url_for('show_rezume', id=rezume_id))
        else:
            return redirect(url_for('index'))
        
    flash('Возникла ошибка', category='error')
    return redirect(url_for('index'))
