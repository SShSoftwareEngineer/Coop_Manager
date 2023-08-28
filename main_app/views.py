from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.

def index(request):
    return render(request, 'main_app/index.html')
    # return HttpResponse("Hello, world!")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')
    # return render(request, 'coop/404.html', status=404)
