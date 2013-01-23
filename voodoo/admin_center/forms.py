# encoding: UTF-8

from django import forms
from django.forms import *
from voodoo.admin_center.models import *
from datetime import date, timedelta
import datetime
import os.path

class OrderForm(forms.ModelForm):
    required_css_class = 'required'
    order_status = ModelChoiceField(OrderStatus.objects.all(), label='Статус выполнения заказа', empty_label=None, required=False)
    
    class Meta:
        model = Order
        widgets = {
            'client_additional_information': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
            'order_info': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
            'car_additional_information': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
            'order_additional_information': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
#            'order_status': forms.ChoiceField(),
            #'car_vin': TextInput(attrs={'size': '17', 'minlength': '17', 'maxlength': '17'}),
#            'city_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
#            'name_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
        }
        exclude = ('creation_date', 'order_total_price1', 'order_total_price2')
    
class OrdersManagementForm(forms.Form):
    # Фильтр
    required_css_class = 'required'
    order_filter_number = forms.CharField(label='Номер заказа', required=False)
    order_filter_status = forms.ModelChoiceField(label="Статус заказа", queryset=OrderStatus.objects.all(), required=False)
    order_filter_creation_date_1 = forms.DateField(label='Создан между', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    order_filter_creation_date_2 = forms.DateField(label='и', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    order_filter_text = forms.CharField(label='Искать текст', required=False)
    order_filter_order_part = forms.CharField(label='в инфе о', required=False)

IMPORT_FILE_TYPES = ['.xls', '.xlsx',]

class XlsImportForm(forms.Form):
    required_css_class = 'required'
    # Импорт xls
    #TODO добавить подсказку
    file = forms.FileField(label='Файл для импорта')
    column_number = forms.IntegerField(label='Столбец "Код"', min_value = 1)
    column_brand = forms.IntegerField(label='Столбец "Бдэнд"', min_value = 1)
    column_description = forms.IntegerField(label='Столбец "Описание"', min_value = 1, required=False)
    column_count = forms.IntegerField(label='Столбец "Количество"', min_value = 1)
    column_price = forms.IntegerField(label='Столбец "Цена"', min_value = 1)
    start_row = forms.IntegerField(label='Строка с которой начать импорт', min_value = 1)
    supplier = forms.ModelChoiceField(label="Поставщик", queryset=Supplier.objects.all())
    currency = forms.ModelChoiceField(label="Цена в валюте", queryset=Currency.objects.all())
    
    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]
        
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s не валидный xls файл.' % extension )
        else:
            return file
class UserManagementForm(forms.Form):
    required_css_class = 'required'
    id = forms.CharField(label = 'id', required=False)
    login = forms.CharField(label = 'login', required=False)
    name = forms.CharField(label = 'name', required=False)
    phone = forms.CharField(label = 'phone', required=False)
    role = forms.CharField(label = 'role', required=False)

class ItemsManagementForm(forms.Form):
    order_id = forms.CharField(label = 'Номер заказа', required=False)
    item_status = forms.ModelChoiceField(label = 'Статус запчасти', queryset=ItemStatus.objects.all(), required=False)
    added_after = forms.DateField(label='Создан между', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    added_before = forms.DateField(label='и', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    
    supplier = forms.ModelChoiceField(label="Поставщик", queryset=Supplier.objects.all(), required=False)
    item_code = forms.CharField(label = 'Номер запчасти', required=False)
    expired_items = forms.BooleanField(label = 'Выборка "просроченных" запчастей', required=False)
    expired_date = forms.DateField(label='по дату', required=False)