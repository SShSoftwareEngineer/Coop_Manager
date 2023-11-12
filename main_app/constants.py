# Предопределенные типы данных
class PredefinedTypes:
    ContactTypes = (
        'Мобильный телефон', 'Домашний телефон', 'Рабочий телефон', 'e-mail', 'Telegram', 'Viber', 'Whatsapp', 'Skype')
    RelationTypes = ('Владелец', 'Родственник', 'Арендатор', 'Доверенное лицо')

# Главное меню
MAIN_MENU = [{'title': 'Домашняя страница', 'url': 'home_page'},
             {'title': 'Сервисная страница', 'url': 'service_page'},
             {'title': 'Админ панель', 'url': 'admin:index'}]

# Количество генерируемых экземпляров недвижимости и других тестовых данных
FILL_BASE_COUNT = 5

# Модификация значений полей
FIELD_VALUE_MODIFICATION = {True: 'Да', False: 'Нет', None: ''}

# Повторяющиеся строки
STRING_CONST = {
    'model.update_date': 'Данные обновлены',
    'model.comment': 'Комментарии',
    'model.slug': 'Slug',
    'model.person_id': 'Человек',
    'model.person_id.photo': 'Фотография',
    'model.person_id.no_photo': 'Нет фотографии',
    'model.person_id.preview': 'Предпросмотр фото',
    'model.person_id.no_preview': 'Нет предпросмотра',
    'model.estate_id': 'Недвижимость',
    'number_divider': '-'
}

# Путь к папке со случайными фотографиями
RANDOM_PHOTO_SRC = 'Support Materials\\photos\\'
