from django.contrib import admin
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.utils.text import slugify

# Register your models here.

from .models import Estate, Person, Address, ContactType, Contact, RelationType, Relation, Pass


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('estate_number', 'floor', 'area')
    list_display_links = ('estate_number',)
    search_fields = ('estate_number', 'floor')
    list_editable = ('area',)
    list_filter = ('floor',)
    ordering = (Cast('estate_number', IntegerField()),)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.estate_number}-{obj.id}')
            obj.save()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.slug:
            obj.slug = slugify(f'{obj.surname}-{obj.name}-{obj.patronymic}-{obj.id}')
            obj.save()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    ordering = ("contact_type",)


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    ordering = ("relation_type",)
