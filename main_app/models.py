import os

from coopmanager.settings import PHOTO_URL
from django.db import models
from django.shortcuts import reverse
from main_app.constants import FIELD_VALUE_MODIFICATION, STRING_CONST
from pytils.translit import slugify


# TODO: переделать все отношения Многие-Ко многим бе искусственно сделанной промежуточной таблицы. Django создает её автоматически, если задать связть ManyToMany между полями

# Create your models here.

def modify_field_value(field_value):
    return FIELD_VALUE_MODIFICATION.get(field_value, field_value)


class Estate(models.Model):
    estate_number = models.CharField(max_length=200, unique=True, verbose_name='Номер')
    floor = models.IntegerField(null=True, blank=True, verbose_name='Этаж')
    length = models.FloatField(null=True, blank=True, verbose_name='Длина')
    width = models.FloatField(null=True, blank=True, verbose_name='Ширина')
    height = models.FloatField(null=True, blank=True, verbose_name='Высота')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь')
    observation_pit = models.BooleanField(null=True, blank=True, verbose_name='Смотровая яма',
                                          choices=[(True, 'Есть'), (False, 'Нет'), (None, '')])
    initial_cost = models.CharField(max_length=200, null=True, blank=True, verbose_name='Начальная стоимость')
    build_date = models.DateField(null=True, blank=True, verbose_name='Дата постройки')
    estimated_cost = models.CharField(max_length=200, null=True, blank=True, verbose_name='Оценочная стоимость')
    estimated_cost_date = models.DateField(null=True, blank=True, verbose_name='Дата оценки')
    for_rent = models.BooleanField(null=True, blank=True, verbose_name='Сдается в аренду',
                                   choices=[(True, 'Да'), (False, 'Нет'), (None, '')])
    for_sale = models.BooleanField(null=True, blank=True, verbose_name='Продается',
                                   choices=[(True, 'Да'), (False, 'Нет'), (None, '')])
    comment = models.TextField(null=True, blank=True, verbose_name=STRING_CONST.get('model.comment'))
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True,
                                       verbose_name=STRING_CONST.get('model.update_date'))
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, db_index=True,
                            verbose_name=STRING_CONST.get('model.slug'))

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self):
        return str(self.estate_number)

    def get_absolute_url(self):
        return reverse('estate_data', kwargs={'estate_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.estate_number}-{self.id}')
            self.save()

    def get_data_for_user(self):
        data_for_user = {
            self._meta.get_field('estate_number').verbose_name: self.estate_number,
            self._meta.get_field('floor').verbose_name: self.floor,
            self._meta.get_field('length').verbose_name: self.length,
            self._meta.get_field('width').verbose_name: self.width,
            self._meta.get_field('height').verbose_name: self.height,
            self._meta.get_field('area').verbose_name: self.area,
            self._meta.get_field('observation_pit').verbose_name: modify_field_value(self.observation_pit),
            self._meta.get_field('build_date').verbose_name: self.build_date.strftime("%d.%m.%Y"),
            self._meta.get_field('initial_cost').verbose_name: self.initial_cost,
            self._meta.get_field('estimated_cost').verbose_name: self.estimated_cost,
            self._meta.get_field('estimated_cost_date').verbose_name: self.estimated_cost_date.strftime("%d.%m.%Y"),
            self._meta.get_field('for_sale').verbose_name: modify_field_value(self.for_sale),
            self._meta.get_field('for_rent').verbose_name: modify_field_value(self.for_rent)}
        return data_for_user

    def get_data_for_personal(self):
        data_for_personal = self.get_data_for_user()
        data_for_personal.update({self._meta.get_field('comment').verbose_name: self.comment})
        data_for_personal.update(
            {self._meta.get_field('update_date').verbose_name: self.update_date.strftime("%d.%m.%Y")})
        return data_for_personal


class Person(models.Model):
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    name = models.CharField(max_length=200, verbose_name='Имя')
    patronymic = models.CharField(max_length=200, null=True, blank=True, verbose_name='Отчество')
    photo = models.ImageField(upload_to=PHOTO_URL, null=True, blank=True,
                              verbose_name=STRING_CONST.get('model.person_id.photo'))
    questions = models.TextField(null=True, blank=True, verbose_name='Вопросы')
    comment = models.TextField(null=True, blank=True, verbose_name=STRING_CONST.get('model.comment'))
    owner_id = models.OneToOneField('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Владелец')
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True,
                                       verbose_name=STRING_CONST.get('model.update_date'))
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name=STRING_CONST.get('model.slug'))

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Члены кооператива и связанные лица'
        ordering = ['surname', 'name', 'patronymic']

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse('person_data', kwargs={'person_slug': self.slug})

    def save(self, *args, **kwargs):
        if self.photo.name:
            photo_name, photo_extension = os.path.splitext(self.photo.name)
            photo_name = slugify(f'{self.surname}-{self.name}-{self.patronymic}')
            self.photo.name = ''.join([PHOTO_URL, photo_name, photo_extension])
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.surname}-{self.name}-{self.patronymic}-{self.id}')
            self.save()

    def get_data_for_user(self):
        data_for_user = {
            self._meta.get_field('surname').verbose_name: self.surname,
            self._meta.get_field('name').verbose_name: self.name,
            self._meta.get_field('patronymic').verbose_name: modify_field_value(self.patronymic),
        }
        if self.owner_id:
            data_for_user.update({self._meta.get_field('owner_id').verbose_name: self.owner_id})
        return data_for_user

    def get_data_for_personal(self):
        data_for_personal = self.get_data_for_user()
        data_for_personal.update({self._meta.get_field('questions').verbose_name: modify_field_value(self.questions)})
        data_for_personal.update({self._meta.get_field('comment').verbose_name: modify_field_value(self.comment)})
        data_for_personal.update({self._meta.get_field('owner_id').verbose_name: modify_field_value(self.owner_id)})
        data_for_personal.update(
            {self._meta.get_field('update_date').verbose_name: self.update_date.strftime("%d.%m.%Y")})
        return data_for_personal


class Address(models.Model):
    flat_number = models.CharField(max_length=200, null=True, blank=True, verbose_name='Квартира')
    house_number = models.CharField(max_length=200, null=True, blank=True, verbose_name='Дом')
    street = models.CharField(max_length=200, null=True, blank=True, verbose_name='Улица')
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name='Населенный пункт')
    region = models.CharField(max_length=200, null=True, blank=True, verbose_name='Область, район')
    postal_code = models.CharField(max_length=200, null=True, blank=True, verbose_name='Почтовый индекс')
    comment = models.TextField(null=True, blank=True, verbose_name=STRING_CONST.get('model.comment'))
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True,
                                       verbose_name=STRING_CONST.get('model.update_date'))
    person_id = models.ForeignKey(Person, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=STRING_CONST.get('model.person_id'))

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['region', 'city', 'street', 'house_number', 'flat_number']

    def __str__(self):
        return (f'{self.street}, {self.house_number}, кв. {self.flat_number}, {self.city}, ' +
                f'{self.region}, {self.postal_code}')

    def get_data_for_user(self):
        data_for_user = {
            self._meta.get_field('flat_number').verbose_name: self.flat_number,
            self._meta.get_field('house_number').verbose_name: self.house_number,
            self._meta.get_field('street').verbose_name: modify_field_value(self.street),
            self._meta.get_field('city').verbose_name: modify_field_value(self.city),
            self._meta.get_field('region').verbose_name: modify_field_value(self.region),
            self._meta.get_field('postal_code').verbose_name: modify_field_value(self.postal_code),
        }
        if self.person_id:
            data_for_user.update({self._meta.get_field('owner_id').verbose_name: self.person_id})
        return data_for_user

    def get_data_for_personal(self):
        data_for_personal = self.get_data_for_user()
        data_for_personal.update({self._meta.get_field('comment').verbose_name: modify_field_value(self.comment)})
        data_for_personal.update(
            {self._meta.get_field('update_date').verbose_name: self.update_date.strftime("%d.%m.%Y")})
        return data_for_personal


class ContactType(models.Model):
    contact_type = models.CharField(max_length=200, verbose_name='Тип контактной информации')

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактов'

    def __str__(self):
        return str(self.contact_type)


class Contact(models.Model):
    contact_info = models.CharField(max_length=200, verbose_name='Контактная информация')
    contact_type = models.ForeignKey(ContactType, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Тип контактной информации')
    person_id = models.ForeignKey(Person, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=STRING_CONST.get('model.person_id'))

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['person_id', 'contact_type', 'contact_info']

    def __str__(self):
        return f'{self.contact_type}: {self.contact_info}'


# TODO: Стандартизировать подписи ко всем встречающимся типам контактов везде

class RelationType(models.Model):
    relation_type = models.CharField(max_length=200, verbose_name='Тип отношения к владельцу')

    class Meta:
        verbose_name = 'Тип отношения к владельцу'
        verbose_name_plural = 'Типы отношений'

    # TODO: Стандартизировать подписи ко всем встречающимся типам отношений везде

    def __str__(self):
        return str(self.relation_type)


class Relation(models.Model):
    ownership_part = models.FloatField(null=True, blank=True, verbose_name='Доля собственности', default=100)
    start_date = models.DateField(null=True, blank=True, verbose_name='Отношение возникло')
    end_date = models.DateField(null=True, blank=True, verbose_name='Отношение прекращено')
    estate_id = models.ForeignKey(Estate, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=STRING_CONST.get('model.estate_id'))
    person_id = models.ForeignKey(Person, null=True, blank=True, on_delete=models.DO_NOTHING,
                                  verbose_name=STRING_CONST.get('model.person_id'))
    relation_type = models.ForeignKey(RelationType, null=True, blank=True, on_delete=models.SET_NULL,
                                      verbose_name='Отношение')

    class Meta:
        verbose_name = 'Отношение'
        verbose_name_plural = 'Отношения'

    def __str__(self):
        return f'{self.estate_id.estate_number},  {self.person_id},  {self.relation_type}'


class Pass(models.Model):
    pass_number = models.CharField(max_length=200, verbose_name='Номер пропуска')
    car_model = models.CharField(max_length=200, null=True, blank=True, verbose_name='Модель ТС')
    car_color = models.CharField(max_length=200, null=True, blank=True, verbose_name='Цвет ТС')
    car_number = models.CharField(max_length=200, null=True, blank=True, verbose_name='Номерной знак ТС')
    issue_date = models.DateField(null=True, blank=True, verbose_name='Дата выдачи')
    expiration_date = models.DateField(null=True, blank=True, verbose_name='Действует до')
    comment = models.TextField(null=True, blank=True, verbose_name=STRING_CONST.get('model.comment'))
    relation_id = models.OneToOneField(Relation, null=True, blank=True, on_delete=models.DO_NOTHING,
                                       verbose_name='Имеет отношение')

    class Meta:
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуска'

    def __str__(self):
        return (f'{self.relation_id.person_id}, {self.relation_id.estate_id}, {self.relation_id.relation_type}, '
                f'{self.car_model}, {self.car_color}, {self.car_number}, № {self.pass_number}')
