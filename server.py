from flask import Flask, request
from markupsafe import escape
import sqlite3
import subprocess

app = Flask(__name__)

# XSS
@app.route('/xss')
def xss():
    user_input = request.args.get('input', 'Hello!')
    escape_input = escape(user_input)  # Используем экранирование flask
    return '<h2>' + escape_input + '</h2>'

# IDOR
@app.route('/profile/<user_id>')
def profile(user_id):
    return 'Профиль пользователя: ' + user_id

# SQL Injection
@app.route('/search')
def search():
    user_input = request.args.get('input', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = '" + user_input + "'")
    result = c.fetchall()
    return str(result)


@app.route('/ping')
def ping():
    hostname = request.args.get('hostname', 'localhost')

    # Формируем и выполняем команду
    command = f"ping {hostname}"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = result.communicate()

    # Разборки с кодировкой
    try:
        output = output.decode('cp866')  # Используйте cp866 для Windows
    except UnicodeDecodeError:
        output = output.decode('cp1251')  # Или попробуйте cp1251

    return output
# Path Traversal
@app.route('/file')
def file():
    filename = request.args.get('filename', 'example.txt')
    with open(filename, 'r') as file:
        content = file.read()
    return content

# Brute Force
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == 'admin' and password == 'password':
        return 'Успешный вход!'
    else:
        return 'Ошибка входа!'

# Механизмы защиты

# CSP от XSS
@app.after_request
def set_csp(response):
    # настройка CSP
    csp_policy = "default-src 'self'; script-src 'self'; style-src 'self'"
    response.headers['Content-Security-Policy'] = csp_policy
    return response


if __name__ == '__main__':
    app.run(debug=True)
