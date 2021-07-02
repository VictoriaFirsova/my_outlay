import csv
import io
import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from datetime import datetime

from my_outlay.forms import UploadFileForm
from my_outlay.models import Category, Statement


# Create your views here.


# домашняя страница
def home(request):
    return render(request, 'home.html')


def drop(request):
    return render(request, 'drop.html')


# получение данных из бд
def categories_list(request):
    categories = Category.objects.all().order_by('title')
    return render(request, 'categories_list.html', {"categories": categories})


def statements_list(request):
    statements = Statement.objects.all().order_by('date')
    return render(request, 'home.html', {"statements": statements})


# сохранение данных в бд
def create(request):
    if request.method == "POST":
        tom = Category()
        tom.title = request.POST.get("title")
        tom.save()
    return HttpResponseRedirect("/categories_list")


# изменение данных в бд
def edit(request, id):
    try:
        category = Category.objects.get(id=id)

        if request.method == "POST":
            category.title = request.POST.get("title")
            category.save()
            return HttpResponseRedirect("/categories_list")
        else:
            return render(request, "edit.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect("/categories_list")
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")


def outlay_upload(request):
    template = 'drop.html'

    prompt = {
        'order': 'Order of the CSV should be date, operation_name,amount,currency, category'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endwith('.csv'):
        messages.error(request, 'Это не CSV')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)

    for column in csv.reader(io_string, delimiter=';', quotecgar='|'):
        _, created = Statement.objects.update_or_create(
            date=column[0],
            operation_name=column[1],
            amount=column[2],
            currency=column[3],
            category=column[9]
        )
    context = {}
    return render(request, template, context)


class UploadPaymentFileView(FormView):
    form_class = UploadFileForm
    template_name = 'drop.html'
    success_url = '/drop/'

    def post(self, request, **kwargs):
        csv_file = request.FILES['file'].read().decode('cp1251')
        io_string = io.StringIO(csv_file)
        df = pd.read_csv(io_string, index_col=False, delimiter=';', skiprows=25, encoding='cp1251',
                         names=['date', 'operation_name', 'amount', 'currency', 'dateop', 'com', 'ob', 'card',
                                'category'])
        # отбросить последние строки
        df['dateop'] = pd.to_datetime(df['dateop'], errors='coerce')
        df = df.dropna(subset=['dateop'])
        # убрать ненужные столбцы
        df.drop(['dateop', 'com', 'ob', 'card'], inplace=True, axis=1)
        # отобрать значения меньше 0
        df['amount'] = df['amount'].str.replace(',', '.')
        df['amount'] = df['amount'].str.replace(' ', '')
        df['amount'] = pd.to_numeric(df['amount'])
        df = df.query("~(amount >= 0)")

        for index, column in df.iterrows():
            if not Statement.objects.filter(
                    date=datetime.strptime(column['date'], "%d.%m.%Y %H:%M:%S"),
                    operation_name=column['operation_name'],
                    amount=column['amount'],
                    currency=column['currency'],
                    category=column['category'],
            ).exists():
                cat = None
                categories = {
                    #'Бензин': 'АЗС',
                    #'Здоровье': ['Медицинский сервис', 'Аптеки'],
                    #'Машина': 'Автомобили - продажа / сервис',
                    #'Продукты': 'Магазины продуктовые',
                    #'Развлечения': '',
                    #'Рестораны': 'Ресторация / бары / кафе',
                    #'Сигареты': '',
                    #'Собака': 'Товары / услуги для животных',
                    #'Спорт': 'Индивидуальные сервис провайдеры',
                    'АЗС': 'Бензин',
                    'Медицинский сервис': 'Здоровье',
                    'Аптеки': 'Здоровье',
                    'Автомобили - продажа / сервис': 'Машина',
                    'Магазины продуктовые': 'Продукты',
                    'Ресторация / бары / кафе': 'Рестораны',
                    'Товары / услуги для животных': 'Собака',
                    'Индивидуальные сервис провайдеры': 'Спорт',
                }
                for i in categories.keys():
                    if column['category'] == i:
                        cat = Category.objects.get(title=categories[i])

                    #if column['category'] == 'Магазины продуктовые':
                    #cat = Category.objects.get(title='Продукты')
                Statement.objects.create(
                    date=datetime.strptime(column['date'], "%d.%m.%Y %H:%M:%S"),
                    #date=column['date'],
                    operation_name=column['operation_name'],
                    amount=column['amount'],
                    currency=column['currency'],
                    category=column['category'],
                    my_category=cat
                )
        # engine = create_engine('sqlite:///db.sqlite3')
        # df.to_sql('Statement', con=engine, if_exists="append", chunksize=1000)

        return super(UploadPaymentFileView, self).post(request, **kwargs)


