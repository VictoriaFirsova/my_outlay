from django.db import models
#from django.http import HttpResponseRedirect
#from django.shortcuts import render

# Create your models here.


class Category (models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Statement (models.Model):
    date = models.DateTimeField()
    operation_name = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    currency = models.CharField(max_length=3)
    category = models.CharField(max_length=100)
    my_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.date} {self.amount}'
