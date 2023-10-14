from django import forms
from django.core.exceptions import ValidationError

from .models import *


class EstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = ['estate_number', 'floor', 'length', 'width', 'height', 'area', 'observation_pit', 'build_date',
                  'initial_cost', 'estimated_cost', 'for_sale', 'for_rent', 'comment']
        widgets = {'comment': forms.Textarea(attrs={'cols': 80, 'rows': 10})}

    def clean_estate_number(self):
        # пользовательский метод валидации по полю estate_number
        estate_number = self.cleaned_data['estate_number']
        if len(estate_number) > 200:
            raise ValidationError('Неправильно!!!')
        return estate_number
