from django.contrib import admin
from .models import Category, Statement

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    ordering = ('title',)


class StatementAdmin(admin.ModelAdmin):
    list_display = ('date', 'operation_name', 'amount', 'currency', 'category', 'my_category')
    ordering = ('date',)
    list_editable = ('my_category',)


admin.site.register(Category, CategoryAdmin)

admin.site.register(Statement, StatementAdmin)


'''fieldsets = (
        (None,
         {'classes': ('wide',),
          'fields': ('name', 'slug', 'order', 'comment')}),
    )

    add_fieldsets = (
        (None,
         {'classes': ('wide',),
          'fields': ('name', 'slug', 'order', 'comment')}),
    )
    list_editable = ('order',)'''
