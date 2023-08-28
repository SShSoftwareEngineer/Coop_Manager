from django.contrib import admin

# Register your models here.

from .models import Estate, Person, Address, ContactType, Contact, RelationType, Relation, Pass


@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


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


admin.site.register(ContactType)
admin.site.register(RelationType)
