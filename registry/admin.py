# -*- coding: utf-8 -*-
__author__ = 'jb'
 
from django.contrib import admin

import models

#class DictionaryAdmin(admin.ModelAdmin):
#    pass

admin.site.register(models.Dictionary)
