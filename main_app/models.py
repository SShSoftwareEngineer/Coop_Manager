from django.db import models
from django.shortcuts import reverse
# from django.utils.text import slugify
from pytils.translit import slugify

# Create your models here.


class Estate(models.Model):
    estate_number = models.CharField(max_length=200, unique=True, verbose_name='Номер')
    floor = models.IntegerField(null=True, blank=True, verbose_name='Этаж')
    length = models.FloatField(null=True, blank=True, verbose_name='Длина')
    width = models.FloatField(null=True, blank=True, verbose_name='Ширина')
    height = models.FloatField(null=True, blank=True, verbose_name='Высота')
    area = models.FloatField(null=True, blank=True, verbose_name='Площадь')
    observation_pit = models.BooleanField(null=True, blank=True, verbose_name='Смотровая яма')
    build_date = models.DateField(null=True, blank=True, verbose_name='Дата постройки')
    initial_cost = models.CharField(max_length=200, null=True, blank=True, verbose_name='Начальная стоимость')
    estimated_cost = models.CharField(max_length=200, null=True, blank=True, verbose_name='Оценочная стоимость')
    estimated_cost_date = models.DateField(null=True, blank=True, verbose_name='Дата оценки')
    for_sale = models.BooleanField(null=True, blank=True, verbose_name='Продается')
    for_rent = models.BooleanField(null=True, blank=True, verbose_name='Сдается в аренду')
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Данные обновлены')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарии')
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True, db_index=True, verbose_name='Slug')

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


class Person(models.Model):
    surname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/%pk', null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    owner_id = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    class Meta:
        verbose_name_plural = 'Personalities'
        ordering = ['surname', 'name', 'patronymic']

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse(f'{self.surname} {self.name} {self.patronymic}', kwargs={'person_slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.surname}-{self.name}-{self.patronymic}-{self.id}')
            self.save()


class Address(models.Model):
    flat_number = models.CharField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    person_id = models.ForeignKey(Person, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.street}, {self.house_number}, {self.flat_number}, {self.city}, {self.postal_code}'


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
