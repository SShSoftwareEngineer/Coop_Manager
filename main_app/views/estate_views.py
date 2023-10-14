from django.shortcuts import render, get_object_or_404
from main_app.models import Estate
from main_app.constants import main_menu
from main_app.forms import EstateForm


def estate_data(request, estate_slug):
    # Поиск по слагу экземпляра объекта
    estate = get_object_or_404(Estate, slug=estate_slug)
    # Создание формы
    if request.method == 'POST':
        estate_form = EstateForm(request.POST)
        if estate_form.is_valid():
            print(estate_form.cleaned_data)
            estate_form.save()
    else:
        estate_form = EstateForm()
    # Создание словаря из названий и значений полей объекта
    estate_fields = dict()
    fields = estate._meta.get_fields()
    for field in fields:
        if hasattr(field, 'value_to_string') and hasattr(field, 'verbose_name'):
            name = field.verbose_name
            value = field.value_to_string(estate)
            estate_fields.update({name: value})
    # Создание контекста для шаблона
    context = {
        'estate_fields': estate_fields,
        'main_menu': main_menu,
        'estate_form': estate_form,
    }
    return render(request, 'main_app/estate_data.html', context=context)
