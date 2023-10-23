class PredefinedTypes:
    ContactTypes = (
        'Мобильный', 'Домашний телефон', 'Рабочий телефон', 'e-mail', 'Skype', 'Telegram', 'Viber', 'Whatsapp')
    RelationTypes = ('Владелец', 'Родственник', 'Арендатор', 'Доверенное лицо')


MAIN_MENU = [{'title': 'Домашняя страница', 'url': 'home_page'},
             {'title': 'Сервисная страница', 'url': 'service_page'},
             {'title': 'Админ панель', 'url': 'admin:index'}]

FILL_BASE_COUNT = 5

FIELD_VALUE_MODIFICATION = {True: 'Да', False: 'Нет', None: ''}

STRING_CONST = {
    'model.update_date': 'Данные обновлены',
    'model.comment': 'Комментарии',
    'model.slug': 'Slug'
}

# Путь к папке со случайными фотографиями
RANDOM_PHOTO_SRC = 'Support Materials\\photos\\'
