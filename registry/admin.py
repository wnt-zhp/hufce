# -*- coding: utf-8 -*-
__LICENSE__ = u"""
    This file is part of Hufrce Program.

    Hufrce Program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Hufrce Program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hufrce Program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    Ten plik jest częścią Hufrce Program.

    Program Hufce jest wolnym oprogramowaniem; możesz go rozprowadzać dalej
    i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU,
    wydanej przez Fundację Wolnego Oprogramowania - według wersji 2 tej
    Licencji lub (według twojego wyboru) którejś z późniejszych wersji.

    Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
    użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
    gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
    ZASTOSOWAŃ. W celu uzyskania bliższych informacji sięgnij do
    Powszechnej Licencji Publicznej GNU.

    Z pewnością wraz z niniejszym programem otrzymałeś też egzemplarz
    Powszechnej Licencji Publicznej GNU (GNU General Public License);
    jeśli nie - napisz do Free Software Foundation, Inc., 59 Temple
    Place, Fifth Floor, Boston, MA  02110-1301  USA
"""
__author__ = 'jb'
 
from django.contrib import admin

import models

import forms

from django.db.models.loading import get_model


class DictionaryAdmin(admin.ModelAdmin):
    list_filter = [
        'type', 'active'
    ]
    readonly_fields = [
            'user_changed'
        ]


class ScoutBookAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'surname', 'book_no', 'issue_date', 'troop', 'srodowisko', 'user_changed'
    ]
    list_filter = [
        'srodowisko', 'troop'
    ]
    search_fields = [
        'name', 'surname', 'book_no', 'issue_date', 'troop__name', 'srodowisko__name'
    ]
    readonly_fields = [
        'user_changed'
    ]


class ScoutBookHistoryAdminInline(admin.TabularInline):
    model = get_model("registry", "HistoricalScoutBook")
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = [
            'id', 'name', 'surname', 'book_no', 'issue_date', 'troop', 'srodowisko', 'user_changed'
    ]

class ScoutBookRegistryAdmin(ScoutBookAdmin):
    inlines = [ScoutBookHistoryAdminInline]
    form = forms.ScoutForm

#
class UprawkoHistoryInline(admin.TabularInline):
    model = get_model("registry", "HistoricalUprawnienie")
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = [
        'id', 'name', 'surname', 'uprawnienie', 'rozkaz', 'srodowisko'
    ]


class UprawkoAdmin(admin.ModelAdmin):
    list_display = [
            'id', 'name', 'surname', 'uprawnienie', 'rozkaz', 'srodowisko'
    ]
    list_filter = [
        'uprawnienie', 'srodowisko', 'rozkaz'
    ]
    search_fields = [
        'id', 'name', 'surname', 'uprawnienie__name', 'rozkaz', 'srodowisko__name', 'date'
    ]
    readonly_fields = ('user_changed',)
    form = forms.UprawkoForm
    inlines = [UprawkoHistoryInline]


class AdressAdminInline(admin.TabularInline):
    model = get_model("registry", "HistoricalAdress")
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = [
            'id', 'street', 'no', 'postalcode', 'city'
    ]

class AdressAdmin(admin.ModelAdmin):
    search_fields = ['name', 'street', 'city']
    form = forms.AdressForm
    inlines = [AdressAdminInline]

class CorrespondenceAdmin(admin.ModelAdmin):
    form = forms.CorrespondenceForm
    readonly_fields = ('number', )
    fields = (
                'number',
                'data',
                'adress',
                'subject',
                'status',
                'responsible',
                'institution_no',
                'remarks'
            )

    search_fields = [
        'number', 'data', 'adress__name', 'adress__street', 'adress__city__name',
        'responsible__username', 'responsible__last_name', 'responsible__first_name',
        'responsible__email', 'institution_no', 'remarks'
    ]

    list_filter = [
        'status', 'responsible'
    ]

    list_display = [
        'number', 'data', 'adressname', 'subject', 'status', 'responsible'
    ]

    def adressname(self, obj):
        return obj.adress.name
    adressname.admin_order_field = 'adress__name'
    adressname.short_description = "Adresat"

admin.site.register(models.Dictionary, DictionaryAdmin)

#admin.site.register(models.ScoutBookHistoryAdminInline, ScoutBookAdmin)

admin.site.register(models.ScoutBook, ScoutBookRegistryAdmin)

admin.site.register(models.Uprawnienie, UprawkoAdmin)

admin.site.register(models.Adress, AdressAdmin)

admin.site.register(models.Corresponcence, CorrespondenceAdmin)