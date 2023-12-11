import sqlite3

# Просто имя файла для базы данных
database_file = 'database.db'

# Попытка подключиться к базе данных (она будет создана, если не существует)
connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Создание таблицы, если она еще не существует
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")

# Проверка, пустая ли таблица
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    # Добавление нескольких записей в таблицу
    cursor.execute("INSERT INTO users (name, email) VALUES ('Ivan', 'ivan@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Oleg', 'oleg@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Anna', 'anna@example.com')")
    print("Добавлены начальные данные.")

# Сохранение изменений и закрытие соединения с базой данных
connection.commit()
connection.close()

print("База данных готова.")

# Открываем файл в режиме записи (w). Если файл не существует, он будет создан.
with open("secret.txt", "w") as file:
    # Записываем текст в файл
    file.write("Это секретный текст, который не должен быть доступен через веб-приложение.")

print("Файл 'secret.txt' создан.")
