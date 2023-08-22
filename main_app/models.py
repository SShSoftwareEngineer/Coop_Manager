from django.db import models


# Create your models here.

class Estate(models.Model):
    estate_number = models.CharField(max_length=200)
    floor = models.IntegerField()
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    area = models.FloatField()
    observation_pit = models.BooleanField()
    build_date = models.DateField()
    initial_cost = models.FloatField()
    estimated_cost = models.FloatField()
    # is_sold = models.BooleanField()
    # is_rented = models.BooleanField()
    update_date = models.DateTimeField(auto_now=True)
    comment = models.TextField()

    def __str__(self):
        return self.estate_number


# TODO: Проверить типы связей в базе, где 0, где 1, где много и исправить в обеих схемах

class Person(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    patronymic = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%pk')
    update_date = models.DateTimeField(auto_now=True)
    questions = models.TextField()
    comment = models.TextField()
    relation = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class Address(models.Model):
    flat_number = models.CharField(max_length=200)
    house_number = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    update_date = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return ', '.join([self.street, self.house_number, self.flat_number, self.city, self.postal_code])


class ContactType(models.Model):
    contact_type = models.CharField(max_length=200)


class Contact(models.Model):
    contact_info = models.CharField(max_length=200)
    contact_type = models.ForeignKey(ContactType, on_delete=models.DO_NOTHING)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return ': '.join([self.contact_type, self.contact_info])


class RelationType(models.Model):
    relation_type = models.CharField(max_length=200)


class Relation(models.Model):
    ownership_part = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    person_id = models.OneToOneField(Person, on_delete=models.DO_NOTHING)
    estate_id = models.ForeignKey(Estate, on_delete=models.DO_NOTHING)
    relation_type = models.ForeignKey(RelationType, on_delete=models.DO_NOTHING)


class Pass(models.Model):
    pass_number = models.CharField(max_length=200)
    car_model = models.CharField(max_length=200)
    car_color = models.CharField(max_length=200)
    car_number = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    comment = models.TextField()
    relation_id = models.OneToOneField(Relation, on_delete=models.CASCADE)

# TODO: проверить опции связанного удаления, где надо, а где не надо


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
