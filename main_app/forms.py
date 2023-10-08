from django import forms
from django.core.exceptions import ValidationError

from .models import *


# class TempForm(forms.Form):
#     estate_number = forms.CharField(max_le ngth=200, label='Номер')
#     slug = forms.SlugField(max_length=255, label='Slug', required=False)
#     floor = forms.IntegerField(required=False)
#     length = forms.FloatField(required=False)
#     width = forms.FloatField(required=False)
#     height = forms.FloatField(required=False)
#     area = forms.FloatField(required=False)
#     observation_pit = forms.NullBooleanField(required=False)
#     build_date = forms.DateField(required=False)
#     initial_cost = forms.DecimalField(decimal_places=2, required=False)
#     estimated_cost = forms.DecimalField(decimal_places=2, required=False)
#     # is_sold = forms.BooleanField()
#     # is_rented = forms.BooleanField()
#     comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}), max_length=5000, required=False)


class TempForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = ['estate_number', 'floor', 'length', 'width', 'height', 'area', 'observation_pit', 'build_date',
                  'initial_cost', 'estimated_cost', 'comment']
        widgets = {'comment': forms.Textarea(attrs={'cols': 80, 'rows': 10})}

    def clean_estate_number(self):
        # пользовательский метод валидации по полю estate_number
        estate_number = self.cleaned_data['estate_number']
        if len(estate_number) > 200:
            raise ValidationError('Неправильно!!!')
        return estate_number
