def render_main():
    page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Главная страница</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
    <p><a href="/vasya?selectedValue=checkboxes_vasya"> vasya </a></p>
    <p><a href="/petya?selectedValue=checkboxes_petya"> petya </a></p>
    <p><a href="/admin?selectedValue=checkboxes_admin_all"> admin </a></p>
    </body>
    '''
    return page


def render_page_vasya(result_stat):
    page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Результаты Васи</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Результаты Васи</h1>
        <form id="messageForm" method="POST">
        {}
        '''.format(''.join(f'<label for="{checkbox}"> <input type="checkbox" name="{checkbox}" id="{checkbox}" {checkbox_status} > {checkbox} </label> <br>\n' for checkbox, checkbox_status in result_stat)) + '''
        <button type="submit">Отправить</button>
        </form>
        <script>
            $("#messageForm").submit(function(e) {
                e.preventDefault();
                // Отправляем AJAX-запрос при подтверждении формы
                $.ajax({
                    type: "POST",
                    url: window.location.href,
                    data: $(this).serialize(),
                    success: function(data) {
                        if (data.status === 'success') {
                            alert(data.message);
                        } else {
                            // Выводим сообщение "данные сохранены"
                            alert(data.message);
                        }
                    },
                    error: function(jqXHR, errorText) {
                        alert("Ошибка AJAX-запроса: " + errorText);
                    }
                });
            });
        </script>
    </body>
    </html>
    '''
    return page

def render_page_petya(result_stat):
    page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Результаты Пети</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Результаты Пети</h1>
        <form id="messageForm" method="POST">
        {}
        '''.format(''.join(f'<label for="{checkbox}"> <input type="checkbox" name="{checkbox}" id="{checkbox}" {checkbox_status} > {checkbox} </label> <br>\n' for checkbox, checkbox_status in result_stat)) + '''
        <button type="submit">Отправить</button>
        </form>
        <script>
            $("#messageForm").submit(function(e) {
                e.preventDefault();
                // Отправляем AJAX-запрос при подтверждении формы
                $.ajax({
                    type: "POST",
                    url: window.location.href,
                    data: $(this).serialize(),
                    success: function(data) {
                        if (data.status === 'success') {
                            alert(data.message);
                        } else {
                            // Выводим сообщение "данные сохранены"
                            alert(data.message);
                        }
                    },
                    error: function(jqXHR, errorText) {
                        alert("Ошибка AJAX-запроса: " + errorText);
                    }
                });
            });
        </script>
    </body>
    </html>
    '''
    return page

def render_page_admin(result_stat):
    page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>АДМЫН</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Админская панель</h1>
        <form id="messageForm" method="POST">
        <label for="databases">Выбери бд для редактирования доступа:</label>
        <select id="databases" name="databases">
            <option value="checkboxes_admin_all">Доступ неограничен</option>
            <option value="checkboxes_admin_access_social">Доступ разрешен на социалки</option>
            <option value="checkboxes_admin_access_media">Доступ разрешен на медиа</option>
        </select>
        <p></p>
        {}
        '''.format(''.join(f'<label for="{checkbox}"> <input type="checkbox" name="{checkbox}" id="{checkbox}" {checkbox_status} > {checkbox} </label> <br>\n' for checkbox, checkbox_status in result_stat)) + '''
        <button type="submit">Отправить</button>
        </form>
        <p></p>
        <p><button onclick="window.location.href = '/admin?selectedValue=checkboxes_admin_all';">Посмотреть таблицу "Доступ неограничен"</button></p>
        <p><button onclick="window.location.href = '/admin?selectedValue=checkboxes_admin_access_social';">Посмотреть таблицу "Доступ разрешен на социалки"</button></p>
        <p><button onclick="window.location.href = '/admin?selectedValue=checkboxes_admin_access_media';">Посмотреть таблицу "Доступ разрешен на медиа"</button></p>
        <script>
            $("#messageForm").submit(function(e) {
                e.preventDefault();
                // Отправляем AJAX-запрос при подтверждении формы
                $.ajax({
                    type: "POST",
                    url: window.location.href,
                    data: $(this).serialize(),
                    success: function(data) {
                        if (data.status === 'success') {
                            alert(data.message);
                        } else {
                            // Выводим сообщение "данные сохранены"
                            alert(data.message);
                        }
                    },
                    error: function(jqXHR, errorText) {
                        alert("Ошибка AJAX-запроса: " + errorText);
                    }
                });
            });
        </script>
    </body>
    </html>
    '''
    return page