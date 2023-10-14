from django.http import HttpResponseNotFound
from django.shortcuts import render
from main_app.constants import main_menu


def home(request):
    context = {'main_menu': main_menu}
    return render(request, 'main_app/home.html', context=context)
    # return HttpResponse("Hello, world!")


def service(request):
    context = {'main_menu': main_menu}
    return render(request, 'main_app/service.html', context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')
    # return render(request, 'coop/404.html', status=404)
