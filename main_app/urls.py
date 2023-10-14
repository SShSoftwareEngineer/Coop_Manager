from django.urls import path
from main_app.views import *

# URL-пути структурных частей приложения
main_urlpatterns = [
    path('', home, name='home_page'),
    path('service/', service, name='service_page'),
]

# URL-пути сервисной страницы
service_page_urlpatterns = [
    path('service_fill_base/', fill_base, name='fill_base'),
    path('service_clean_base/', clean_base, name='clean_base'),
]

# URL-пути страницы данных о недвижимости
estate_data_urlpatterns = [
    path('estate_data/<slug:estate_slug>', estate_data, name='estate_data'),
]

# URL-пути приложения, суммарный файл
urlpatterns = main_urlpatterns + service_page_urlpatterns + estate_data_urlpatterns
