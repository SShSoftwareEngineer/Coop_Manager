from django.shortcuts import render, get_object_or_404
from main_app.models import Estate


def estate_data(request, estate_slug):
    estate_data = get_object_or_404(Estate, slug=estate_slug)
    context = {
        'estate_number': estate_data.estate_number,
    }
    return render(request, 'main_app/estate_data.html', context=context)
