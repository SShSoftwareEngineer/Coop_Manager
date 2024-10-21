from django.http import HttpResponseNotFound
from django.shortcuts import render
from main_app.constants import MAIN_MENU


def home(request):
    context = {'main_menu': MAIN_MENU}
    return render(request, 'main_app/home.html', context=context)
    # return HttpResponse("Hello, world!")


def service(request):
    context = {'main_menu': MAIN_MENU}
    return render(request, 'main_app/service.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')
    # return render(request, 'coopmanager/404.html', status=404)
