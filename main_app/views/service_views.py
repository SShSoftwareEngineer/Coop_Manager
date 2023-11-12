import string
from random import (choice, choices)
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from faker import Faker
from main_app.constants import PredefinedTypes, MAIN_MENU, FILL_BASE_COUNT, RANDOM_PHOTO_SRC
from main_app.models import *
from django.conf import settings


# def choice_by_probability(probabilities: List[float]) -> int:
#     above_probabilities = [x / sum(probabilities) for x in probabilities]
#     ranges_probabilities = [sum(above_probabilities[:x + 1]) for x in range(len(above_probabilities))]
#     ranges_probabilities.insert(0, 0)
#     random_value = random()
#     for random_choice in range(len(ranges_probabilities)):
#         if ranges_probabilities[random_choice] <= random_value < ranges_probabilities[random_choice + 1]:
#             return random_choice


def fill_base(request):
    def get_random_estate(estate_number: str):
        if choices([False, True], weights=[0.8, 0.2])[0]:
            estate_number += f"{STRING_CONST.get('number_divider')}{choice(['А', 'Б', 'В', 'Г', 'Д'])}"
        rand_estate = Estate(
            estate_number=estate_number,
            floor=faker.random_int(min=1, max=3),
            length=faker.random_int(min=10, max=15),
            width=faker.random_int(min=6, max=10),
            height=faker.random_int(min=3, max=4),
            area=faker.random_int(min=60, max=150),
            observation_pit=faker.null_boolean(),
            build_date=faker.date_between(start_date='-50y', end_date='-40y'),
            initial_cost=faker.pricetag(),
            estimated_cost=faker.pricetag(),
            estimated_cost_date=faker.date_between(start_date='-30y', end_date='-20y'),
            for_sale=faker.null_boolean(),
            for_rent=faker.null_boolean(),
            comment=faker_ru.paragraph(nb_sentences=1)
        )
        return rand_estate

    def get_random_person(random_photo_path: str):
        if choices([False, True], weights=[0.5, 0.5])[0]:
            person_name = faker_ru.first_name_male()
            person_patronymic = faker_ru.middle_name_male()
            person_surname = faker_ru.last_name_male()
        else:
            person_name = faker_ru.first_name_female()
            person_patronymic = faker_ru.middle_name_female()
            person_surname = faker_ru.last_name_female()
        new_photo_name = slugify(f'{person_surname}-{person_name}-{person_patronymic}') + '.jpg'
        photo_data = open(random_photo_path, 'rb').read()
        photo_file = ContentFile(photo_data)
        photo_filepath = default_storage.save(os.path.normpath(os.path.join(settings.PHOTO_URL, new_photo_name)),
                                              photo_file)
        rand_person = Person(
            name=person_name,
            patronymic=person_patronymic,
            surname=person_surname,
            photo=os.path.join(settings.PHOTO_URL, photo_filepath),
            update_date=faker.date_between(start_date='-5y', end_date='-1y'),
            questions=faker_ru.paragraph(nb_sentences=1),
            comment=faker_ru.paragraph(nb_sentences=1),
            owner_id=None,
        )
        return rand_person

    def get_random_address(rand_person: Person):
        house_number = faker_ua.building_number()
        if choices([False, True], weights=[0.8, 0.2])[0]:
            house_number += f"{STRING_CONST.get('number_divider')}{choice(['А', 'Б', 'В', 'Г', 'Д'])}"
        rand_address = Address(
            flat_number=choice(range(300)),
            house_number=house_number,
            street=faker_ua.street_title(),
            city=faker_ua.city(),
            region=faker_ua.region(),
            postal_code=faker_ua.postcode(),
            comment=faker_ru.paragraph(nb_sentences=1),
            update_date=faker.date_between(start_date='-5y', end_date='-1y'),
            person_id=rand_person,
        )
        return rand_address

    def get_random_contact(rand_person: Person, rand_contact_type: ContactType):
        rand_contact_info = ''
        if ('телефон' in str(rand_contact_type)) or (str(rand_contact_type) in {'Viber', 'Whatsapp'}):
            rand_contact_info = faker_ua.phone_number()
        if 'e-mail' in str(rand_contact_type):
            rand_contact_info = faker_ua.ascii_email()
        if 'Telegram' in str(rand_contact_type):
            rand_contact_info = f'@{faker.word()}'
        if 'Skype' in str(rand_contact_type):
            rand_contact_info = faker.word()
        rand_contact = Contact(
            contact_info=rand_contact_info,
            contact_type=rand_contact_type,
            person_id=rand_person,
        )
        return rand_contact

    def get_random_relation(rand_estate: Estate, rand_person: Person, rand_relation_type: RelationType):
        rand_ownership_part = 100 if choices([False, True], weights=[0.1, 0.9])[0] else choice(range(100))
        rand_start_date = None
        rand_end_date = None
        if choices([False, True], weights=[0.3, 0.7])[0]:
            rand_start_date = faker.date_between(start_date='-25y', end_date='-5y')
        if choices([False, True], weights=[0.7, 0.3])[0]:
            rand_end_date = faker.date_between(start_date='-10y', end_date='-1y')
        rand_relation = Relation(
            ownership_part=rand_ownership_part,
            start_date=rand_start_date,
            end_date=rand_end_date,
            relation_type=rand_relation_type,
            estate_id=rand_estate,
            person_id=rand_person,
        )
        return rand_relation

    def get_random_pass(rand_relation: Relation):
        rand_pass = Pass(
            pass_number=rand_relation.estate_id.estate_number,
            car_model=choice(['Toyota', 'Volkswagen', 'Hyundai', 'Kia', 'Renault', 'Nissan', 'Stellantis',
                              'GMC', 'Ford', 'Suzuki', 'BMW']),
            car_color=faker_ua.color_name(),
            car_number=f'{"".join(choices(string.ascii_uppercase, k=2))} {"".join(choices(string.digits, k=4))} ' +
                       f'{"".join(choices(string.ascii_uppercase, k=2))}',
            issue_date=rand_relation.start_date,
            expiration_date=rand_relation.end_date,
            comment=faker_ru.paragraph(nb_sentences=1),
            relation_id=rand_relation,
        )
        return rand_pass

    if request.method == 'POST':
        # Инициализация Faker
        Faker.seed()
        faker = Faker()
        faker_ua = Faker('uk_UA')
        faker_ru = Faker('ru_RU')
        # Инициализация предопределенных типов данных имеющимися в базе данных + заданными по умолчанию и запись
        # их в соответствующие таблицы базы данных
        contact_types = set()
        contact_types.update(*list(ContactType.objects.values_list('contact_type')))
        contact_types.update(PredefinedTypes.ContactTypes)
        for contact_type in sorted(contact_types):
            ContactType.objects.get_or_create(contact_type=contact_type)
        relation_types = set()
        relation_types.update(*list(RelationType.objects.values_list('relation_type')))
        relation_types.update(PredefinedTypes.RelationTypes)
        for relation_type in sorted(relation_types):
            RelationType.objects.get_or_create(relation_type=relation_type)
        # Инициализация списков для экземпляров классов моделей набора тестовых данных
        estate_list = []
        person_list = []
        address_list = []
        contact_list = []
        relation_list = []
        pass_list = []
        # Получаем последний номер недвижимости в базе данных и вычисляем следующий доступный номер
        first_estate_number = 1
        if Estate.objects.count():
            first_estate_number = int(
                Estate.objects.latest('id').estate_number.split(STRING_CONST.get('number_divider'))[0]) + 1
        # Задаём путь к папке со случайными фотографиями
        photo_path = os.listdir(os.path.join(settings.BASE_DIR, RANDOM_PHOTO_SRC))
        # Получаем списки типов контактов и отношений из базы данных
        contact_type_list = ContactType.objects.all()
        contact_type_default = ContactType.objects.get(contact_type='Мобильный телефон')
        relation_type_list = RelationType.objects.all()
        relation_type_default = RelationType.objects.get(relation_type='Владелец')
        # Генерируем набор данных для тестирования в количестве заданном в FILL_BASE_COUNT
        for i1 in range(FILL_BASE_COUNT):
            # Генерация случайных данных о недвижимости, модель Estate
            random_estate = get_random_estate(str(first_estate_number + i1))
            estate_list.append(random_estate)
            # Генерация 1-3 случайных наборов персональных данных для текущей недвижимости, модель Person
            for i2 in range((choices(range(3), weights=[0.7, 0.2, 0.1]))[0] + 1):
                random_photo = os.path.join(settings.BASE_DIR, RANDOM_PHOTO_SRC, choice(photo_path))
                random_person = get_random_person(random_photo)
                # Генерация 1-2 случайных адресов для текущего набора персональных данных, модель Address
                for i3 in range((choices(range(2), weights=[0.8, 0.2]))[0] + 1):
                    random_address = get_random_address(random_person)
                    address_list.append(random_address)
                # Генерация 1-5 случайных контактов для текущего набора персональных данных, модель Contact
                for i3 in range((choices(range(5), weights=[0.4, 0.3, 0.1, 0.1, 0.1]))[0] + 1):
                    # Мобильный телефон - обязательный контакт, дальше случайный выбор
                    contact_type = contact_type_default
                    if i3:
                        contact_type = choice(contact_type_list)
                    random_contact = get_random_contact(random_person, contact_type)
                    contact_list.append(random_contact)
                # Генерация случайного отношения для текущей пары Estate и Person, модель Relation
                # Владелец - обязательное отношение, дальше случайный выбор
                relation_type = relation_type_default
                if i2:
                    relation_type = choice(relation_type_list)
                random_relation = get_random_relation(random_estate, random_person, relation_type)
                relation_list.append(random_relation)
                # Генерация случайного документа (пропуска) для текущего отношения, модель Pass
                random_pass = get_random_pass(random_relation)
                pass_list.append(random_pass)
                person_list.append(random_person)
        # Сохранение сгенерированных случайных тестовых данных в базу данных

        with transaction.atomic():
            for item in estate_list:
                item.save()
            for item in person_list:
                item.save()
            Address.objects.bulk_create(address_list)
            Contact.objects.bulk_create(contact_list)
            for item in relation_list:
                item.save()
            Pass.objects.bulk_create(pass_list)
    else:
        pass
    context = {
        'title': 'Добавление данных в базу',
        'text': "В базу добавлены новые случайные данные",
        'main_menu': MAIN_MENU
    }
    return render(request, 'main_app/service_report.html', context=context)


def clean_base(request):
    if request.method == 'POST':
        # Обнуление связей между записями в таблицах
        Person.objects.all().update(owner_id=None)
        Address.objects.all().update(person_id=None)
        Contact.objects.all().update(contact_type=None)
        Contact.objects.all().update(person_id=None)
        Relation.objects.all().update(relation_type=None)
        Relation.objects.all().update(estate_id=None)
        Relation.objects.all().update(person_id=None)
        Pass.objects.all().update(relation_id=None)
        # Очистка всех таблиц в базе данных
        Estate.objects.all().delete()
        Person.objects.all().delete()
        Address.objects.all().delete()
        Contact.objects.all().delete()
        ContactType.objects.all().delete()
        Relation.objects.all().delete()
        RelationType.objects.all().delete()
        Pass.objects.all().delete()
        # Удаление файлов личных фотографий
        photo_dir = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, settings.PHOTO_URL)
        for filename in os.listdir(photo_dir):
            file_path = os.path.join(photo_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        pass

    context = {
        'title': 'Очистка базы данных',
        'text': "База данных полностью очищена",
        'main_menu': MAIN_MENU
    }
    return render(request, 'main_app/service_report.html', context=context)
