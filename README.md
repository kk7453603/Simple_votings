# Проект "Simple votings"

### Цель
Предоставить пользователю сервис, на котором можно быстро создать голосование и собрать мнения пользователей касательно какого-либо вопроса

### Технологический стек:
- Python 3.6
- Django 3.1+
- SQLite 3.22+

### Инструкция по настройке проекта:
1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "simple votings" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. Обновить pip:
   ```bash
   pip install --upgrade pip
   ```
6. Установить в виртуальное окружение необходимые пакеты: 
   ```bash
   pip install -r requirements.txt
   ```

7. Скачать файл db.sqlite3 из Wiki проекта (https://gitlab.informatics.ru/2020-2021/mytischi/s105/simple_votings/-/wikis/Documentation-and-DB), вставить файл в папку проекта.
8. Синхронизировать структуру базы данных с моделями: 
   ```bash
   python manage.py migrate
   ```

9. Создать суперпользователя
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', '1@abc.net', 'promprog')"
   ```

10. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)

Внимание! Создана отдельная модель пользователя в модуле `main`! 
При создании ForeignKey'ев на User'а - использовать её!
