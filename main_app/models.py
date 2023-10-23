import os

from coop.settings import PHOTO_URL
from django.db import models
from django.shortcuts import reverse
from main_app.constants import FIELD_VALUE_MODIFICATION, STRING_CONST
from pytils.translit import slugify


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
                                          choices=[(True, 'Да'), (False, 'Нет'), (None, '')])
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
        verbose_name = 'Estate'
        verbose_name_plural = 'Estates'
        # ordering = []

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
    photo = models.ImageField(upload_to=PHOTO_URL, null=True, blank=True, verbose_name='Фотография')
    questions = models.TextField(null=True, blank=True, verbose_name='Вопросы')
    comment = models.TextField(null=True, blank=True, verbose_name=STRING_CONST.get('model.comment'))
    owner_id = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Владелец')
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True,
                                       verbose_name=STRING_CONST.get('model.update_date'))
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name=STRING_CONST.get('model.slug'))

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Personalities'
        ordering = ['surname', 'name', 'patronymic']

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse('person_data', kwargs={'person_slug': self.slug})

    def save(self, *args, **kwargs):
        if self.photo.name:
            photo_name, photo_extension = os.path.splitext(self.photo.name)
            photo_name = slugify(f'{self.surname}-{self.name}-{self.patronymic}')
            self.photo.name = ''.join([photo_name, photo_extension])
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
    person_id = models.ForeignKey(Person, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['city', 'street', 'house_number', 'flat_number']

    def __str__(self):
        return f'{self.street}, {self.house_number}, {self.flat_number}, {self.city}, {self.region}, {self.postal_code}'


class ContactType(models.Model):
    contact_type = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.contact_type)


class Contact(models.Model):
    contact_info = models.CharField(max_length=200)
    contact_type = models.ForeignKey(ContactType, on_delete=models.DO_NOTHING)
    person_id = models.ForeignKey(Person, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.contact_type}: {self.contact_info}'


class RelationType(models.Model):
    relation_type = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.relation_type)


class Relation(models.Model):
    ownership_part = models.FloatField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    person_id = models.OneToOneField(Person, on_delete=models.DO_NOTHING)
    estate_id = models.ForeignKey(Estate, on_delete=models.DO_NOTHING)
    relation_type = models.ForeignKey(RelationType, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.estate_id.estate_number}: {self.person_id}, {self.relation_type}'


class Pass(models.Model):
    pass_number = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200, null=True, blank=True)
    car_color = models.CharField(max_length=200, null=True, blank=True)
    car_number = models.CharField(max_length=200, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    relation_id = models.OneToOneField(Relation, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'Passes'

    def __str__(self):
        return f'{self.pass_number}: {self.relation_id}\n{self.car_model}, {self.car_color}, {self.car_number}'

# EmailField
# FilePathField
# ImageField
#
# ForeignKey
# Чтобы создать рекурсивное отношение - объект, который имеет отношение «многие-к-одному» с самим
# собой - используйте models.ForeignKey('self', on_delete = models.CASCADE)
# ForeignKey.on_delete
# ManyToManyField
# OneToOneField
