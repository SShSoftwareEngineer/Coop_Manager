from django import template
from main_app.constants import MAIN_MENU
from main_app.models import *

register = template.Library()


@register.simple_tag
def get_contact_types():
    return ContactType.objects.all()


@register.inclusion_tag('main_app/show_main_menu.html')
def show_main_menu():
    return {'main_menu': MAIN_MENU}


@register.inclusion_tag('main_app/show_table_data.html')
def show_table_data(table_data=None):
    return {'table_data': table_data}
