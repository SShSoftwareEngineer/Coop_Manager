from django.shortcuts import render
from main_app.forms import TempForm


def form(request):
    if request.method == 'POST':
        temp_form = TempForm(request.POST)
        if temp_form.is_valid():
            print(temp_form.cleaned_data)
            temp_form.save()
    else:
        temp_form = TempForm()
    return render(request, 'main_app/form.html', {'temp_form': temp_form})
