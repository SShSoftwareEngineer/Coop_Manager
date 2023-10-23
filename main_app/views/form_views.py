from django.shortcuts import render
from main_app.forms import EstateForm


def form(request):
    if request.method == 'POST':
        estate_form = EstateForm(request.POST)
        if estate_form.is_valid():
            print(estate_form.cleaned_data)
            estate_form.save()
    else:
        estate_form = EstateForm()
    return render(request, 'main_app/estate_data.html', {'estate_form': estate_form})
