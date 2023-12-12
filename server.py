from flask import Flask, request, session, abort
from markupsafe import escape
import sqlite3
import subprocess
import re
import shlex
import os

app = Flask(__name__)
app.secret_key = '410e0dc210e18311dd4e5007435ef2e0'


# XSS
@app.route('/xss')
def xss():
    user_input = request.args.get('input', 'Hello!')
    escape_input = escape(user_input)  # Используем экранирование flask
    return '<h2>' + escape_input + '</h2>'


# IDOR
@app.route('/profile/<user_id>')
def profile(user_id):
    # проверка, аутентифицирован ли пользователь и имеет ли он право доступа к этому профилю
    if 'authenticated_user_id' in session and session['authenticated_user_id'] == user_id:
        return f'Профиль пользователя: {user_id}'
    abort(403)


# SQL Injection
@app.route('/search')
def search():
    user_input = request.args.get('input', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (user_input,))
    result = c.fetchall()
    return str(result)


# OS Command Injection
@app.route('/ping')
def ping():
    hostname = request.args.get('hostname', 'localhost')
    if not is_valid_hostname(hostname):
        return 'Недопустимый ввод'

    # Экранирование
    safe_hostname = shlex.quote(hostname)
    # subprocess.run по безопаснее чем subprocess.Popen
    try:
        result = subprocess.run(["ping", safe_hostname], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        output = result.stdout
    except Exception as e:
        output = str(e)

    # Разборки с кодировкой
    try:
        output = output.decode('cp866')
    except UnicodeDecodeError:
        output = output.decode('cp1251')

    return output


# Path Traversal
whitelist = {'requirements.txt'}

@app.route('/file')
def file():
    filename = request.args.get('filename', 'example.txt')
    new_filename = os.path.normpath(filename)
    if new_filename not in whitelist:
        return 'Доступ запрещен!'
    # Проверка, что файл не выходит за пределы директории
    if os.path.isabs(new_filename) or '..' in new_filename.split(os.path.sep):
        return 'Доступ запрещен!'

    try:
        with open(new_filename, 'r') as file:
            content = file.read()
        return content
    except IOError:
        return 'Файл не найден'


# Brute Force
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == 'admin' and password == 'password':
            session['authenticated_user_id'] = username  # Сохранение пользователя в сессии
            return 'Успешный вход!'
        else:
            return 'Ошибка входа!'
    return '''
    <form method="post">
        Имя пользователя: <input type="text" name="username"><br>
        Пароль: <input type="password" name="password"><br>
        <input type="submit" value="Войти">
    </form>
    '''


@app.route('/logout')
def logout():
    session.pop('authenticated_user_id', None)  # Удаляем пользователя из сессии
    return 'Вы вышли из системы'


# Механизмы защиты
# __________________________________________________________________
# CSP от XSS
@app.after_request
def set_csp(response):
    # настройка CSP
    csp_policy = "default-src 'self'; script-src 'self'; style-src 'self'"
    response.headers['Content-Security-Policy'] = csp_policy
    return response


# Проверка, является ли ввод допустимым
def is_valid_hostname(hostname):
    if re.match(r'^[a-zA-Z0-9.-]+$', hostname):
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
