from django import template
from main_app.constants import main_menu
from main_app.models import *

register = template.Library()


@register.simple_tag
def get_contact_types():
    return ContactType.objects.all()


@register.inclusion_tag('main_app/show_main_menu.html')
def show_main_menu():
    return {'main_menu': main_menu}
