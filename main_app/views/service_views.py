from random import choice
from django.utils.text import slugify

from django.shortcuts import render
from django.http import HttpResponse
from main_app.constants import PredefinedTypes

from ..models import *
from faker import Faker


def fill_base(request):
    FILL_BASE_COUNT = 10

    def get_random_data(model):
        return choice(model.objects.all())

    if request.method == 'POST':
        # Инициализация Faker
        faker = Faker()
        faker_ua = Faker('uk_UA')
        faker_ru = Faker('ru_RU')
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
        # Генерация случайной модели Estate
        first_estate_number=1 if not Estate.objects.count() else int(Estate.objects.latest("id").estate_number) + 1
        # if not Estate.objects.count():
        #     first_estate_number = int(Estate.objects.latest("id").estate_number) + 1
        # else:
        #     first_estate_number = 1
        estate_list = []
        for i in range(FILL_BASE_COUNT):
            estate_list.append(Estate(estate_number=str(first_estate_number + i),
                                      slug=slugify(
                                          f'{first_estate_number + i}-{faker.random_int(min=100000, max=999999)}'),
                                      floor=faker.random_int(min=1, max=3),
                                      length=faker.random_int(min=10, max=15),
                                      width=faker.random_int(min=6, max=10),
                                      height=faker.random_int(min=3, max=4),
                                      area=faker.random_int(min=60, max=150),
                                      observation_pit=faker.null_boolean(),
                                      build_date=faker.date_between(start_date='-50y', end_date='-40y'),
                                      initial_cost=faker.pricetag(),
                                      estimated_cost=faker.pricetag(),
                                      is_sold=faker.null_boolean(),
                                      is_rented=faker.null_boolean(),
                                      comment=faker_ru.paragraph(nb_sentences=1)
                                      ))

        for i in range(FILL_BASE_COUNT):
            estate_list[i].save()

        print(get_random_data(ContactType))
        print(type(get_random_data(ContactType)))

        # Генерация адресов
        # Генерация контактов
        # Генерация персональных данных
        # result['first_name'] = fake_ua.first_name()
        # result['last_name'] = fake_ua.last_name()
        # result['birthdate'] = fake_ru.date_between(start_date='-50y', end_date='-20y').strftime('%d.%m.%Y')
        # result['residence'] = fake_ua.city()

    else:
        pass
    context = {'title': 'Добавление данных в базу', 'text': "В базу добавлены новые случайные данные"}
    return render(request, 'main_app/service_report.html', context=context)


def clean_base(request):
    if request.method == 'POST':
        Estate.objects.all().delete()
        Person.objects.all().delete()
        Address.objects.all().delete()
        ContactType.objects.all().delete()
        Contact.objects.all().delete()
        RelationType.objects.all().delete()
        Relation.objects.all().delete()
        Pass.objects.all().delete()
    else:
        pass
    context = {'title': 'Очистка базы данных', 'text': "База данных полностью очищена"}
    return render(request, 'main_app/service_report.html', context=context)
