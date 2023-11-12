import os.path

from coop import settings
from django.contrib import admin
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from main_app.constants import STRING_CONST

# Register your models here.

from .models import Estate, Person, Address, ContactType, Contact, RelationType, Relation, Pass

# TODO: Сделать вывод дат в админке в нужном формате

def check_get_photo(person: Person, height: int):
    if person.photo:
        person_photo_path = os.path.normpath(os.path.join(settings.BASE_DIR, person.photo.url[1:]))
        if os.path.exists(person_photo_path):
            return mark_safe(f"<img src='{person.photo.url}' height={height}")


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'update_date']
    list_display = ['estate_number', 'floor', 'for_rent', 'for_sale']
    list_display_links = ['estate_number']
    search_fields = ['estate_number', 'comment']
    list_editable = []
    list_filter = ['floor', 'for_rent', 'for_sale']
    ordering = [Cast('estate_number', IntegerField())]
    fieldsets = [
        (None, {'fields': ['estate_number', 'floor']}),
        (None, {'fields': [('length', 'width', 'height'), 'area']}),
        (None, {'fields': ['observation_pit']}),
        (None, {'fields': [('initial_cost', 'build_date')]}),
        (None, {'fields': [('estimated_cost', 'estimated_cost_date')]}),
        (None, {'fields': [('for_rent', 'for_sale')]}),
        (None, {'fields': ['comment', 'update_date', 'slug']}),
    ]
    save_on_top = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.estate_number}-{obj.id}')
            obj.save()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'patronymic', 'get_preview_photo', 'owner_id']
    list_display_links = ['surname', 'name', 'patronymic', 'get_preview_photo']
    readonly_fields = ['slug', 'update_date', 'get_photo']
    list_editable = []
    search_fields = ['surname', 'name', 'patronymic', 'comment']
    ordering = ['surname', 'name', 'patronymic']
    fieldsets = [
        (None, {'fields': ['surname', ('name', 'patronymic')]}),
        (None, {'fields': [('get_photo', 'photo')]}),
        (None, {'fields': [('questions', 'comment')]}),
        (None, {'fields': ['owner_id', 'update_date', 'slug']}),
    ]
    save_on_top = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.surname}-{obj.name}-{obj.patronymic}-{obj.id}')
            obj.save()

    @admin.display(description=STRING_CONST.get('model.person_id.photo'))
    def get_photo(self, person: Person):
        photo_url = check_get_photo(person, 130)
        if photo_url:
            return photo_url
        return STRING_CONST.get('model.person_id.no_photo')

    @admin.display(description=STRING_CONST.get('model.person_id.preview'))
    def get_preview_photo(self, person: Person):
        photo_url = check_get_photo(person, 40)
        if photo_url:
            return photo_url
        return STRING_CONST.get('model.person_id.no_preview')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['update_date']
    list_display = ['person_id', 'city', 'region', 'street', 'house_number', 'flat_number']
    list_display_links = ['person_id', 'city']
    list_filter = ['city']
    search_fields = ['person_id__surname', 'person_id__name', 'person_id__patronymic', 'region', 'city', 'street',
                     'comment']
    ordering = ['city', 'street',
                Cast('house_number', IntegerField()),
                Cast('flat_number', IntegerField())]
    fieldsets = [
        (None, {'fields': ['person_id']}),
        (None, {'fields': [('city', 'region')]}),
        (None, {'fields': [('street', 'house_number', 'flat_number')]}),
        (None, {'fields': ['postal_code', 'comment', 'update_date']}),
    ]
    save_on_top = True


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    ordering = ['contact_type']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['person_id', 'contact_info', 'contact_type']
    list_display_links = ['person_id']
    list_editable = ['contact_info', 'contact_type']
    search_fields = ['person_id__surname', 'person_id__name', 'person_id__patronymic', 'contact_info']
    list_filter = ['contact_type']
    ordering = ['person_id', 'contact_type', 'contact_info']
    fieldsets = [
        (None, {'fields': ['person_id', 'contact_type', 'contact_info']}),
    ]
    save_on_top = True

    @admin.display(description=STRING_CONST.get('model.person_id'), ordering='person_id')
    def person_id_searchable(self, contact: Contact):
        return str(contact.person_id)


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    ordering = ['relation_type']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ['estate_id', 'person_id', 'relation_type', 'start_date', 'end_date']
    list_display_links = ['estate_id', 'person_id']
    list_editable = []
    search_fields = ['estate_id__estate_number', 'person_id__surname', 'person_id__name', 'person_id__patronymic']
    list_filter = ['relation_type']
    ordering = [Cast('estate_id__estate_number', IntegerField()), 'relation_type', 'person_id', 'start_date',
                'end_date']
    fieldsets = [
        (None, {'fields': ['estate_id']}),
        (None, {'fields': [('person_id', 'relation_type')]}),
        (None, {'fields': [('start_date', 'end_date')]}),
        (None, {'fields': ['ownership_part']}),
    ]
    save_on_top = True


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = ['get_person_id', 'get_estate_id', 'get_relation_type', 'car_model', 'car_color', 'issue_date',
                    'expiration_date']
    list_display_links = ['get_person_id', 'get_estate_id']
    readonly_fields = ['relation_id', 'get_person_id', 'get_estate_id', 'get_relation_type', 'get_photo']
    list_editable = []
    search_fields = ['relation_id__estate_id__estate_number', 'relation_id__person_id__surname',
                     'relation_id__person_id__name', 'relation_id__person_id__patronymic', 'comment']
    list_filter = ['car_model']
    ordering = [Cast('relation_id__estate_id', IntegerField()), 'relation_id__relation_type']
    fieldsets = [
        (None, {'fields': [('get_person_id', 'get_estate_id', 'get_relation_type')]}),
        (None, {'fields': ['pass_number', 'get_photo']}),
        (None, {'fields': [('car_model', 'car_color', 'car_number')]}),
        (None, {'fields': [('issue_date', 'expiration_date')]}),
        (None, {'fields': ['comment']}),
    ]
    save_on_top = True

    # pass_number  car_model  car_color  car_number  issue_date  expiration_date  comment  relation_id

    @admin.display(description=STRING_CONST.get('model.estate_id'))
    def get_estate_id(self, obj):
        return obj.relation_id.estate_id.estate_number

    @admin.display(description='Кому выдан')
    def get_person_id(self, obj):
        return obj.relation_id.person_id

    @admin.display(description='Отношение')
    def get_relation_type(self, obj):
        return obj.relation_id.relation_type

    @admin.display(description=STRING_CONST.get('model.person_id.photo'))
    def get_photo(self, obj):
        photo_url = check_get_photo(obj.relation_id.person_id, 130)
        if photo_url:
            return photo_url
        return STRING_CONST.get('model.person_id.no_photo')
