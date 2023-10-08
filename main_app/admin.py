from django.contrib import admin
from django.db.models import IntegerField
from django.db.models.functions import Cast

# Register your models here.

from .models import Estate, Person, Address, ContactType, Contact, RelationType, Relation, Pass


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("estate_number",)}
    # list_display = ()
    # list_display_links = ()
    # search_fields = ()
    # list_editable = ()
    # list_filter = ()
    ordering = (Cast('estate_number', IntegerField()),)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "surname", "patronymic")}


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
