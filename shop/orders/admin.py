from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    # Получаем экземпляры полей модели
    opts = modeladmin.model._meta
    # Создаем обьект ответа класса HttpResponse с типом содержимого text/csv
    response = HttpResponse(content_type='text/csv')
    # Добавляем заголовок, к которому будет прикреплен файл
    response['Content-Disposition'] = 'attachment;' f'filename{opts.verbose_name}.csv'
    # Записываем данные файла в обьект response
    writer = csv.writer(response)
    # Динамически получаем поля модели с помощью метода get_fields() опции meta
    # исключая отношения многие ко многим, один к одному
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Заполняем строку-заголовок названиями полей
    writer.writerow([field.verbose_name for field in fields])
    # Проходим по каждому выбранному пользователем элементу и записываем данные в строку
    # при этом выполняем форматирование обьектов datetime т.к выходные данные csv
    # должны быть представлены в виде строк
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'  # Краткое описание


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [export_to_csv] # Регистрация в модели конвертера в CSV
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]