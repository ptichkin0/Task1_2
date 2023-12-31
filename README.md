## Задание 1 v2 Защищенная версия приложения
[v1](https://github.com/ptichkin0/Task1_1/tree/main)
### Инструкция по сборке и запуску приложения
1. Установка зависимостей:

   ```
   pip install -r requirements.txt
   ```

2. Создание файлов для тестов:

   ```
   python create_files.py
   ```
   
3. Запуск сервера:

   ```
   python server.py
   ```
   
### Комментарии к исправлениям
XSS:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/bf93496aef4070c348c53c2a29368a8d244df6bc)
- Изменения: Добавлены экранирование и настроено CSP.
- Обоснование: Поскольку разработанное приложение достаточно маленькое в плане масштаба, функционала и имеет лишь демонстрационный характер, имело смысл реализовать только самые базовые методы защиты. По мере масштабирования проекта должна появится необходимость в валидации и санитизации данных, а также в надежном WAF.

IDOR:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/b9054d20201a8212e811d595e793acd6ee513fd4)
- Изменения: Обязательная аутентификация для доступа в профиль и использованием проверки сессии
- Обоснование: Ввод проверки прав доступа через авторизацию аутентифицированных пользователей для решения уязвимости такой как IDOR является базовым методом и более надежным. Далее можно ввести иерархию ролей, для расширения прав доступа администраторам и т.д. В некоторых случаях решением будет использование индиректных ссылок на объекты или непрогнозируемых идентификаторов, например UUID.
- Изменение в инструкциях:
  Для входа в /profile/admin теперь требуется на странице /login ввести логин и пароль (admin и password соответственно)
   ```
  http://127.0.0.1:5000/profile/admin
  http://127.0.0.1:5000/login
  http://127.0.0.1:5000/logout
   ```
  
SQL Injection:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/a6f7c8c06b8323f9db9d44a8735b61a7f88d2dca)
- Изменения: Использование параметризированных запросов и экранирование
- Обоснование: Использование заложенного в бд механизма экранирования и параметризированного запроса выглядит самым оптимальным вариантом. В дальнейшем стоит присмотреться к ORM-библиотекам и ограничениям прав доступа к базе данных сервисов. Использование WAF в дальнейшем также можно считать обязательным.

OS Command Injection:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/81b25ce117d4cbd5bcd8bc7e54e8de0edcc5a6b7)
- Изменения: Опять же экранирование, проверка на валидность, а также использование более безопасной альтернативы выполнения команд
- Обоснование: Собственная логика проверки на валидность в дополнении к остальным механизмам защиты хоть и может быть избыточной на данном примере, но она была реализована больше в демонстративных целях. В будущем думаю стоит уделить внимание проверке на Time-based и Blind Command Injection

Path Traversal:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/a11618505c7a2ac0841d45a76211c30c8b9cf532)
- Изменения: добавлен whitelist и проверки чтобы пользователь не покинул директорию
- Обоснование: Лучший способ в решении проблемы вовсе избежать динамического чтения файлов на основе вводимых пользователем данных. Рассмотрим случай если считать это невозможным, то следует прибегнуть строгой проверке входных данных. В некоторых случаях целесообразно использовать whitelist с разрешенными к прочтению файлами
- Изменение в инструкциях. requirements.txt теперь в белом списке, а secret.txt недоступен
```
http://127.0.0.1:5000/file?filename=./requirements.txt
http://127.0.0.1:5000/file?filename=./secret.txt
```
Brute Force Attack:
[Коммит](https://github.com/ptichkin0/Task1_2/commit/3d1f9add2d05e0f0c0e65d5791cfe1d1ce7c5a39)
- Изменения: Реализовано ограничения количества попыток входа(3 в минуту для страницы /login)
- Обоснование: Против Brute Force по-хорошему бы иметь как минимум хороший пароль (и чтобы хранился в хеше с солью на случай утечки), ну да ладно, сочтем пока это за условность. Тут 4 варианта основных вижу:
1) Капча через пару не удачных попыток 
2) Двухфакторная аутентификация(2FA)
3) Ограничение скорости запросов (по нарастающей)
4) Блокировка после N кол-ва неудачных запросов


Примечание. Ко всем уязвимостям в качестве профилактики можно также отнести еще следующие:
- Тестирование на проникновение и аудит кода
- Обучение и осведомленность разработчиков
- Регулярное обновление
