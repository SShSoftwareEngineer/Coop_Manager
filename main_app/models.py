from django.db import models
from django.shortcuts import reverse


# Create your models here.


class Estate(models.Model):
    estate_number = models.CharField(max_length=200, unique=True, verbose_name='Number')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    floor = models.IntegerField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    observation_pit = models.BooleanField(null=True, blank=True)
    build_date = models.DateField(null=True, blank=True)
    initial_cost = models.CharField(max_length=200, null=True, blank=True)
    estimated_cost = models.CharField(max_length=200, null=True, blank=True)
    is_sold = models.BooleanField(null=True, blank=True)
    is_rented = models.BooleanField(null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Estate'
        verbose_name_plural = 'Estates'
        # ordering = []

    def __str__(self):
        return str(self.estate_number)

    def get_absolute_url(self):
        return reverse('estate_data', kwargs={'estate_slug': self.slug})


class Person(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to='photos/%pk', null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    owner_id = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'People'

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


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
