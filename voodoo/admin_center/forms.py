# encoding: UTF-8

from django import forms
from django.forms import *
from voodoo.admin_center.models import Order
import os.path

class OrderForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Order
        widgets = {
            'client_additional_information': Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
            'order_info': Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
            'car_additional_information': Textarea(
            attrs={'style': 'max-height:60px;min-height:60px;'
                  + 'max-width:400px;min-width:400px'}),
                   
            #'car_vin': TextInput(attrs={'size': '17', 'minlength': '17', 'maxlength': '17'}),
#            'city_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
#            'name_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
        }
    
class OrdersManagementForm(forms.Form):
    # Фильтр
    order_filter_number = CharField(label='Номер заказа', required=False)
    order_filter_status = ChoiceField(
                                      label="Статус заказа",
                                      widget=Select(),
                                      choices=([
                                                ('Принят', 'Принят'),
                                                ('Обработан', 'Обработан'),
                                                ('Закрыт', 'Закрыт')
                                                ]),
                                      initial='Принят',
                                      required=False)                        
    
    order_filter_creation_date_1 = DateField(label='Создан между')
    order_filter_creation_date_2 = CharField(label='и')
    order_filter_text = CharField(label='Искать текст')
    order_filter_order_part = CharField(label='в инфе о')

IMPORT_FILE_TYPES = ['.xls', ]

class XlsImportForm(forms.Form):
    # Импорт xls
    #TODO добавить подсказку
    file = FileField(label='Файл для импорта')
    column_number = IntegerField(label='Код', min_value = 1)
    column_brand = IntegerField(label='Бдэнд', min_value = 1)
    column_description = IntegerField(label='Описание', min_value = 1, required=False)
    column_count = IntegerField(label='Количество', min_value = 1)
    column_price = IntegerField(label='Цена', min_value = 1)
    
    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]
        
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s не валидный xls файл.' % extension )
        else:
            return file