"""
1) Создать форму регистрации для пользователя.
2) Форма должна содержать поля: имя, электронная почта,
пароль (с подтверждением), дата рождения, согласие на
обработку персональных данных.
3) Валидация должна проверять, что все поля заполнены
корректно (например, дата рождения должна быть в
формате дд.мм.гггг).

Для домашнего задания добавлено:
- организовано хранение данных в базе данных
- пароль не хранится в открытом виде - в базе данных храниться его Hash рассчитанный по SHA256
"""
from flask import Flask, render_template, request, redirect, url_for
import secrets
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
from models import db, User
import os.path
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)
DB_FILE_NAME = 'users.db'
FILE_PATH = 'instance/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_FILE_NAME
db.init_app(app)


@app.route('/')
def index():
    context = {'title': 'Глваная'}
    return render_template('index.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
        if existing_user:
            error_msg = 'Такое имя пользователя или адрес эл.почты уже есть в базе данных!'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)
        # считаем hash пароля, удаляем лишнее и сохранаяем в базу данных
        _, password = str(hashlib.sha256(form.password.data.encode()))[:-1] .split('@')
        date_of_birth = form.date_of_birth.data
        agreement = form.agreement.data
        new_user = User(name=name, email=email, password=password, date_of_birth=date_of_birth, agreement=agreement)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('agreement'))
    context = {'title': 'Регистрация пользователя'}
    return render_template('register.html', form=form, **context)


@app.route('/agreement/')
def agreement():
    context = {'title': 'Поздравляем с регистрацией в базе данных!'}
    return render_template('agreement.html', **context)


@app.route('/users/')
def users():
    users = User.query.all()
    context = {'title': 'Список зарегистрированных пользователей',
               'users': users}
    return render_template('users_view.html', **context)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('База данных создана!')


if __name__ == '__main__':
    if os.path.exists(FILE_PATH+DB_FILE_NAME):
        print('Используем имеющуюся базу данных!')
    else:
        db.create_all()
        print('База данных создана!')
    app.run(debug=True)
