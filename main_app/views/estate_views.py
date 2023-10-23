from django.shortcuts import render, get_object_or_404
from main_app.models import Estate
from main_app.constants import MAIN_MENU
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
    context = {
        'estate_data': estate.get_data_for_user(),
        'main_menu': MAIN_MENU,
        'estate_form': estate_form,
    }
    return render(request, 'main_app/estate_data.html', context=context)
