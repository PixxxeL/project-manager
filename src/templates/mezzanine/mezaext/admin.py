# -*- coding: utf8 -*-

from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import EditableBlock


@register(EditableBlock)
class EditableBlockAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'slug', 'enabled',)
    list_editable = ('enabled',)
