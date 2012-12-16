# encoding: UTF-8

from django import forms
from voodoo.admin_center.models import Order, Supplier
import os.path

class OrderForm(forms.ModelForm):
    required_css_class = 'required'
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
                   
            #'car_vin': TextInput(attrs={'size': '17', 'minlength': '17', 'maxlength': '17'}),
#            'city_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
#            'name_recipient': TextInput(attrs={'size': '63', 'maxlength': '63'}),
        }
    
class OrdersManagementForm(forms.Form):
    # Фильтр
    required_css_class = 'required'
    order_filter_number = forms.CharField(label='Номер заказа', required=False)
    order_filter_status = forms.ChoiceField(
                                      label="Статус заказа",
                                      widget=forms.Select(),
                                      choices=([
                                                ('Принят', 'Принят'),
                                                ('Обработан', 'Обработан'),
                                                ('Закрыт', 'Закрыт')
                                                ]),
                                      initial='Принят',
                                      required=False)                        
    
    order_filter_creation_date_1 = forms.DateField(label='Создан между')
    order_filter_creation_date_2 = forms.CharField(label='и')
    order_filter_text = forms.CharField(label='Искать текст')
    order_filter_order_part = forms.CharField(label='в инфе о')

IMPORT_FILE_TYPES = ['.xls', ]

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
    
    def clean_file(self):
        file = self.cleaned_data['file']
        extension = os.path.splitext(file.name)[1]
        
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s не валидный xls файл.' % extension )
        else:
            return file

class TestForm(forms.Form):
    supplier = forms.ModelMultipleChoiceField(label="Поставщик", queryset=Supplier.objects.all())
    
#    def clean_supplier(self):
#        supplier = self.cleaned_data['supplier']
#        return supplier