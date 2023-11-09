from django.contrib import admin
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.utils.text import slugify

# Register your models here.

from .models import Estate, Person, Address, ContactType, Contact, RelationType, Relation, Pass


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'update_date')
    list_display = ('estate_number', 'floor')
    list_display_links = ('estate_number',)
    search_fields = ('estate_number', 'floor', 'comment')
    list_editable = ()
    list_filter = ('floor',)
    ordering = (Cast('estate_number', IntegerField()),)
    fieldsets = [
        (None, {'fields': ['estate_number', 'floor']}),
        (None, {'fields': [('length', 'width', 'height'), 'area']}),
        (None, {'fields': ['observation_pit']}),
        (None, {'fields': [('initial_cost', 'build_date')]}),
        (None, {'fields': [('estimated_cost', 'estimated_cost_date')]}),
        (None, {'fields': [('for_rent', 'for_sale')]}),
        (None, {'fields': ['comment', 'update_date', 'slug']}),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.estate_number}-{obj.id}')
            obj.save()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'update_date')
    list_display = ('surname', 'name', 'patronymic', 'photo')
    list_display_links = ('surname', 'name', 'patronymic')
    list_editable = ('photo',)
    search_fields = ('surname', 'name', 'patronymic', 'comment')
    ordering = ('surname', 'name', 'patronymic')
    fieldsets = [
        (None, {'fields': ['surname', ('name', 'patronymic')]}),
        (None, {'fields': ['photo']}),
        (None, {'fields': [('questions', 'comment')]}),
        (None, {'fields': ['owner_id', 'update_date', 'slug']}),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.surname}-{obj.name}-{obj.patronymic}-{obj.id}')
            obj.save()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['update_date']
    list_display = ('city', 'region', 'street', 'house_number', 'flat_number')
    search_fields = ('region', 'city', 'street', 'comment')
    ordering = ('city', 'street',
                Cast('house_number', IntegerField()),
                Cast('flat_number', IntegerField()),)
    fieldsets = [
        (None, {'fields': [('city', 'region')]}),
        (None, {'fields': [('street', 'house_number', 'flat_number')]}),
        (None, {'fields': ['postal_code', 'comment', 'update_date']}),
    ]


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    ordering = ['contact_type']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['person_id', 'contact_info', 'contact_type']
    list_display_links = ['person_id', 'contact_info']
    search_fields = ['contact_info']
    list_filter = ['contact_type']
    ordering = ['person_id']


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    ordering = ['relation_type']


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    ordering = [Cast('pass_number', IntegerField())]
