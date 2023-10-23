from django.shortcuts import render, get_object_or_404
from main_app.models import Person
from main_app.constants import MAIN_MENU


# from main_app.forms import PersonForm


def person_data(request, person_slug):
    # Поиск по слагу экземпляра объекта
    person = get_object_or_404(Person, slug=person_slug)
    # Создание формы
    # if request.method == 'POST':
    #     person_form = PersonForm(request.POST)
    #     if person_form.is_valid():
    #         print(person_form.cleaned_data)
    #         person_form.save()
    # else:
    #     person_form = PersonForm()
    photo = {
        'URL': person.photo.url,
        'alt_text': f'{person.surname} {person.name} {person.patronymic}',
    }
    context = {
        'photo': photo,
        'person_data': person.get_data_for_personal(),
        'main_menu': MAIN_MENU,
        # 'person_form': person_form,
    }
    return render(request, 'main_app/person_data.html', context=context)
