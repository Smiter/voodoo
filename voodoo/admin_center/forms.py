# encoding: UTF-8

from django import forms
from django.forms import *
from voodoo.admin_center.models import *
from datetime import date, timedelta, datetime
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
                  + 'max-width:550px;min-width:550px'}),
            'order_info': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:550px;min-width:550px'}),
            'car_additional_information': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:550px;min-width:550px'}),
            'order_additional_information': forms.Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:550px;min-width:550px'}),
#            'order_status': forms.ChoiceField(),
            #'car_vin': TextInput(attrs={'size': '17', 'minlength': '17', 'maxlength': '17'}),
#            'city_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
#            'name_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
        }
        exclude = ('creation_date', 'order_total_price1', 'order_total_price2')
 
ORDER_PART_CHOICES = (
            (u'Запчасти', u'Запчасти'),
            (u'Клиенте', u'Клиенте'),
            (u'Авто', u'Авто'),
            (u'Заказе', u'Заказе'),
        )
    
class OrdersManagementForm(forms.Form):
    # Фильтр
    required_css_class = 'required'
    order_filter_number = forms.CharField(label='Номер заказа', required=False)
    order_filter_status = forms.ModelChoiceField(label="Статус заказа", queryset=OrderStatus.objects.all(), initial="1", required=False)
    order_filter_creation_date_1 = forms.DateField(label='Создан между', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',), initial=datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=7), datetime.time.min))
    order_filter_creation_date_2 = forms.DateField(label='и', required=False, widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',), initial=datetime.datetime.combine(datetime.datetime.now().date(), datetime.time.max))
    order_filter_text = forms.CharField(label='Искать текст', required=False)
    order_filter_order_part = forms.ChoiceField(label='в инфе о', choices=ORDER_PART_CHOICES, required=False)
    
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
            raise forms.ValidationError(u'%s не валидный xls файл.' % extension)
        else:
            return file


ORDER_CHOICES = (
            (u'Все', u'Все'),
            (u'Принят', u'Принят'),
            (u'Заказан', u'Заказан'),
            (u'Доставлен', u'Доставлен'),
            (u'Отказ', u'Отказ'),
)

ROLE_CHOICES = (
  ('Accountants', 'Accountants'),
  ('Clients', 'Clients'),
  ('Managers', 'Managers'),
  ('Super Managers', 'Super Managers'),
  ('Workers', 'Workers'),
)


class UserManagementForm(forms.Form):
    required_css_class = 'required'
    # id = forms.CharField(label='id', required=False)
    login = forms.CharField(label='login', required=False)
    name = forms.CharField(label='name', required=False)
    phone = forms.CharField(label='phone', required=False)
    role = ChoiceField(
        label="Роль",
        widget=Select(attrs={'style': 'width:100px'}),
        choices=ROLE_CHOICES,
        initial='1', required=False)


class ItemsManagementForm(forms.Form):
    order_id = forms.CharField(label='Номер заказа', required=False)
    item_status = forms.ModelChoiceField(label='Статус запчасти', queryset=ItemStatus.objects.all(), initial='2', required=False)
    added_after = forms.DateField(label='Создан между', required=False, widget=forms.DateInput(format='%d.%m.%Y'), input_formats=('%d.%m.%Y',), initial=datetime.datetime.combine(datetime.datetime.now() - datetime.timedelta(days=7), datetime.time.min))
    added_before = forms.DateField(label='и', required=False, widget=forms.DateInput(format='%d.%m.%Y'), input_formats=('%d.%m.%Y',), initial=datetime.datetime.combine(datetime.datetime.now().date(), datetime.time.max))
    
    supplier = forms.ModelChoiceField(label="Поставщик", queryset=Supplier.objects.all(), required=False)
    item_code = forms.CharField(label='Номер запчасти', required=False)
    expired_items = forms.BooleanField(label='Выборка "просроченных" запчастей', required=False)
    expired_date = forms.DateField(label='по дату', required=False)

