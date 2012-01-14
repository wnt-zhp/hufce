# -*- coding: utf-8 -*-
from django.contrib import admin

__author__ = 'jb'

class HistoryAdminInline(admin.TabularInline):
    extra = 0
    can_delete = False
    max_num = 0
