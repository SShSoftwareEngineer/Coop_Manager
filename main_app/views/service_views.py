from random import choice, random
from typing import List

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from faker import Faker
from main_app.constants import PredefinedTypes, MAIN_MENU, FILL_BASE_COUNT, RANDOM_PHOTO_SRC
from main_app.models import *
from django.conf import settings


def choice_by_probability(probabilities: List[int]) -> int:
    above_probabilities = [x / sum(probabilities) for x in probabilities]
    ranges_probabilities = [sum(above_probabilities[:x + 1]) for x in range(len(above_probabilities))]
    ranges_probabilities.insert(0, 0)
    random_value = random()
    for random_choice in range(len(ranges_probabilities)):
        if ranges_probabilities[random_choice] <= random_value < ranges_probabilities[random_choice + 1]:
            return random_choice


def fill_base(request):
    def get_random_data(model):
        return choice(model.objects.all())

    if request.method == 'POST':
        # Инициализация Faker
        faker = Faker()
        faker_ua = Faker('uk_UA')
        faker_ru = Faker('ru_RU')
        Faker.seed()
        # Инициализация предопределенных типов данных имеющимися в базе данных + заданными по умолчанию и запись их
        # в соответствующие таблицы базы данных
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
        # Генерация случайных данных о недвижимости, модель Estate
        first_estate_number = 1 if not Estate.objects.count() else int(Estate.objects.latest("id").estate_number) + 1
        estate_list = []
        for i in range(FILL_BASE_COUNT):
            current_estate = Estate(
                estate_number=str(first_estate_number + i),
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
            estate_list.append(current_estate)
        # Генерация случайных персональных данных, модель Person
        person_list = []
        photos_list = os.listdir(os.path.join(settings.BASE_DIR, RANDOM_PHOTO_SRC))
        for i in range(FILL_BASE_COUNT):
            if choice([0, 1]):
                person_name = faker_ru.first_name_male()
                person_patronymic = faker_ru.middle_name_male()
                person_surname = faker_ru.last_name_male()
            else:
                person_name = faker_ru.first_name_female()
                person_patronymic = faker_ru.middle_name_female()
                person_surname = faker_ru.last_name_female()
            random_photo = os.path.join(settings.BASE_DIR, RANDOM_PHOTO_SRC, choice(photos_list))
            new_photo_name = slugify(f'{person_surname}-{person_name}-{person_patronymic}') + '.jpg'
            photo_data = open(random_photo, 'rb').read()
            photo_file = ContentFile(photo_data)
            photo_path = default_storage.save(os.path.join(settings.PHOTO_URL, new_photo_name), photo_file)
            current_person = Person(
                name=person_name,
                patronymic=person_patronymic,
                surname=person_surname,
                photo=os.path.join(settings.PHOTO_URL, photo_path),
                update_date=faker.date_between(start_date='-5y', end_date='-1y'),
                questions=faker_ru.paragraph(nb_sentences=1),
                comment=faker_ru.paragraph(nb_sentences=1)
                # owner_id = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
            )
            person_list.append(current_person)

        # Генерация адресов
        # Генерация контактов

        for item in estate_list:
            item.save()
        for item in person_list:
            item.save()

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
        # очистка всех таблиц
        Estate.objects.all().delete()
        Person.objects.all().delete()
        Address.objects.all().delete()
        ContactType.objects.all().delete()
        Contact.objects.all().delete()
        RelationType.objects.all().delete()
        Relation.objects.all().delete()
        Pass.objects.all().delete()
        # удаление файлов фотографий
        photo_dir = os.path.join(settings.BASE_DIR, settings.MEDIA_URL[1:], settings.PHOTO_URL)
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
