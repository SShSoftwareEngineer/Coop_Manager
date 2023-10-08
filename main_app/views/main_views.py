from django.http import HttpResponseNotFound
from django.shortcuts import render

main_menu = [{'title': 'Домашняя страница', 'url': 'home_page'},
             {'title': 'Страница форм', 'url': 'form_page'},
             {'title': 'Сервисная страница', 'url': 'service_page'},
             {'title': 'Админ панель', 'url': 'admin:index'}]


def home(request):
    context = {'main_menu': main_menu}
    return render(request, 'main_app/home.html', context=context)
    # return HttpResponse("Hello, world!")


def service(request):
    return render(request, 'main_app/service.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')
    # return render(request, 'coop/404.html', status=404)
