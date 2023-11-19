from flask import Flask, request, jsonify
import sqlite3
from render_pages import *
from flask_basicauth import BasicAuth
import requests
import paramiko

###############################################################################################################################################################

# Тут задаются базовые параметры, логин и пароль
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
basic_auth = BasicAuth(app)

#server = "" # ip или имя сервера
#username = "" 
#password = ""

#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # политика безопасности чтобы он не ругался на то что сервак не доступен
#ssh.connect(server, username=username, password=password)

###############################################################################################################################################################

# Читаем файл с названиями чекбоксов
with open('bin_files/checkboxes.txt', 'r', encoding='utf-8') as file:
    checkboxes = [line.strip() for line in file]

# Настройки подключения к бд
conn = sqlite3.connect('bin_files/checkboxes.db', check_same_thread=False)
cursor = conn.cursor()

###############################################################################################################################################################

# Функция проверки доступа, сравниваются несколько таблиц по принципу битовой сетки.
def checks_enters(result, name_child):  
    databases = ["checkboxes_admin_all", "checkboxes_admin_access_social", "checkboxes_admin_access_media"]
    for access_level_base in databases:
        command_get = "SELECT {}".format(''.join(f' {checkbox},' for checkbox in checkboxes)).rstrip(',') + " FROM {}".format(''.join(access_level_base)) + " ORDER BY id DESC LIMIT 1"
        cursor.execute(command_get)
        result_access = cursor.fetchone() 
        check_result = [1 if result[i] == result_access[i] == 1 else 0 for i in range(len(result_access))]
        if tuple(check_result) == result_access:

            messages = {
                "checkboxes_admin_all": "Разблокирован полный уровень доступа",
                "checkboxes_admin_access_social": "Разблокирован доступ к социальным сетям",
                "checkboxes_admin_access_media": "Разблокирован доступ к медиа"
            } # сообщения которые выводятся при совпадении условия

            if access_level_base in messages:
                message = messages[access_level_base]
                # Что будет выполнено при соблюдении условий
                if messages[access_level_base] == "Разблокирован полный уровень доступа":
                    message_tg = f"У {name_child} получен полный доступ"
                    bot_token = ''
                    chat_id = ''
                    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message_tg}"
                    requests.get(api_url)   

                if messages[access_level_base] == "Разблокирован доступ к социальным сетям":
                    cmd = "touch test_social"
                    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

                if messages[access_level_base] == "Разблокирован доступ к медиа":
                    cmd = "touch test_media"
                    #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
            # Отправка сообщения с уровнем доступа
            data = ({
                'status': 'success',
                'message': str(message)
            })

            return jsonify(data)
    # Если никакое условие не выполнено, то просто происходит отбивка что мол данные сохранены
    return jsonify({'status': 'success', 'message': 'Данные успешно сохранены.'})

###############################################################################################################################################################

# Код для проверки таблиц в бд, если они пустые (None), то забивается нулями
def check_db_if_empty(selected_value):
    # Выгрузка из бд состояний чекбоксов
    comm = "SELECT {}".format(''.join(f' {checkbox},' for checkbox in checkboxes)).rstrip(',') + f" FROM {selected_value}"+ " ORDER BY id DESC LIMIT 1" # На основании данных получаем из бд данные
    cursor.execute(comm)
    result = cursor.fetchone() 
    # Если таблица пустая, то забиваем ее нулями
    if result is None:
        values = []
        names = []
        for checkbox in checkboxes:
            names.append(checkbox)
            values.append(0)
        query = f"INSERT INTO {selected_value}" +" ({})".format(", ".join(map(str, names)))  + " VALUES ({})".format(", ".join(map(str, values)))
        cursor.execute(query)
        conn.commit()
    # Повторный запрос данных из таблицы чтобы не перезапускать страницу
    cursor.execute(comm)
    result = cursor.fetchone() 
    return result

#Код для записи значений в бд
def insert_into_db(selected_value, names, values):
    query = f"INSERT INTO {selected_value}" + "({})".format(", ".join(map(str, names)))  + " VALUES ({})".format(", ".join(map(str, values)))
    cursor.execute(query)
    conn.commit()    

# Код для записи в бд при ПОСТ запросе
def post_into_db(checkbox_data):
    # Перебираем все данные и сохраняем их в базе данных
    values = []
    names = []
    for checkbox_name in checkboxes:
        names.append(checkbox_name)
        if checkbox_name in checkbox_data:
            values.append(1)
        else:
            values.append(0)
    return names, values

###############################################################################################################################################################

# Создаем таблицу, если она еще не существует
command_sql1 = '''
CREATE TABLE IF NOT EXISTS checkboxes_vasya (id INTEGER PRIMARY KEY,{}'''.format(''.join(f' {checkbox} INTEGER,' for checkbox in checkboxes)).rstrip(',') + ''')'''
command_sql2 = '''
CREATE TABLE IF NOT EXISTS checkboxes_petya (id INTEGER PRIMARY KEY,{}'''.format(''.join(f' {checkbox} INTEGER,' for checkbox in checkboxes)).rstrip(',') + ''')'''
command_sql3 = '''
CREATE TABLE IF NOT EXISTS checkboxes_admin_all (id INTEGER PRIMARY KEY,{}'''.format(''.join(f' {checkbox} INTEGER,' for checkbox in checkboxes)).rstrip(',') + ''')'''
command_sql4 = '''
CREATE TABLE IF NOT EXISTS checkboxes_admin_access_social (id INTEGER PRIMARY KEY,{}'''.format(''.join(f' {checkbox} INTEGER,' for checkbox in checkboxes)).rstrip(',') + ''')'''
command_sql5 = '''
CREATE TABLE IF NOT EXISTS checkboxes_admin_access_media (id INTEGER PRIMARY KEY,{}'''.format(''.join(f' {checkbox} INTEGER,' for checkbox in checkboxes)).rstrip(',') + ''')'''
commands = [command_sql1, command_sql2, command_sql3, command_sql4, command_sql5]

for comm in commands:
    cursor.execute(comm)

###############################################################################################################################################################

# Генерируем главную HTML страницу 
@app.route('/', methods=['GET', 'POST'])
def index_main():
    return render_main()

###############################################################################################################################################################

# Генерируем HTML страницу на основе названий чекбоксов
@app.route('/vasya', methods=['GET', 'POST'])
def index_vasya():
    selected_value = request.args.get('selectedValue')  # Получаем выбранное значение из запроса
    result = check_db_if_empty(selected_value)
    # Если же все хорошо, то на странице генерим состояние чекбокса как нажатое
    result_stat = [(checkboxes[i], "checked" if result[i] == 1 else "unchecked") for i in range(len(checkboxes))]    
    # Если нажимается кнопка отправить
    if request.method == 'POST':
        # Получаем все данные чекбоксов
        checkbox_data = request.form
        names, values = post_into_db(checkbox_data)
        insert_into_db(selected_value, names, values)
        result_vasya = values
        # Проверяем доступ сравнивая результат и целевую бд
        return checks_enters(result_vasya, name_child="vasya")
    return render_page_vasya(result_stat)

###############################################################################################################################################################

# Генерируем HTML страницу на основе названий чекбоксов
@app.route('/petya', methods=['GET', 'POST'])
def index_petya():
    selected_value = request.args.get('selectedValue')  # Получаем выбранное значение из запроса
    result = check_db_if_empty(selected_value)
    result_stat = [(checkboxes[i], "checked" if result[i] == 1 else "unchecked") for i in range(len(checkboxes))]     
    if request.method == 'POST':
        checkbox_data = request.form
        names, values = post_into_db(checkbox_data)
        insert_into_db(selected_value, names, values)
        result_petya = values 
        return checks_enters(result_petya, name_child="Petya")
    return render_page_petya(result_stat)

###############################################################################################################################################################

# Генерируем HTML админ страницу на основе названий чекбоксов
@app.route('/admin', methods=['GET', 'POST'])
@basic_auth.required #Данная строка включает запрос логина и пароля для доступа на страницу
def index_admin():
    selected_value = request.args.get('selectedValue')  # Получаем выбранное значение из запроса
    result = check_db_if_empty(selected_value)
    result_stat = [(checkboxes[i], "checked" if result[i] == 1 else "unchecked") for i in range(len(checkboxes))]            
    if request.method == 'POST':
        checkbox_data = request.form
        names, values = post_into_db(checkbox_data)
        insert_into_db(selected_value, names, values)
        return jsonify({'status': 'success', 'message': 'Данные успешно сохранены.'})
    return render_page_admin(result_stat)

###############################################################################################################################################################

# Запуск сервера на определенном порту и на любом ip
if __name__ == '__main__':
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000) 
    # В данный момент сделано для отладки, чтобы не было проблем и прочего, запускать надо раскомментировав две строки выше
    app.run(host="0.0.0.0", port=5000, debug=True)