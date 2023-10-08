from django import template
from main_app.models import *

register = template.Library()


@register.simple_tag
def get_contact_types():
    return ContactType.objects.all()
