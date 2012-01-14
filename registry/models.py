# -*- coding: utf-8 -*-
from django.db.models.expressions import F
from django.db.models.sql.aggregates import Max
from django.db.transaction import commit_unless_managed


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

from django.db import models
from registry_engine.models import create_record_types_abstract_model
from const import CHAR_FIELD_MAX_LEN
from datetime import datetime

DICTIONARY_CHOICES = (
    ('Srodowisko', 'Srodowisko'),
    ('Troop', 'Troop'),
    ("Uprawnienie", "Uprawnienie")
)

class Dictionary(models.Model):

    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, verbose_name="Nazwa")
    active = models.BooleanField(verbose_name="Aktywny", help_text="Czy dany rekord może być przypisywany do innych obiektów", default=True)
    type = models.CharField(max_length=CHAR_FIELD_MAX_LEN, choices=DICTIONARY_CHOICES)


    def __unicode__(self):
        return ' '.join(('+' if self.active else '-', self.name, self.type))

class ScoutBook(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']

    id = models.AutoField(u"Numer porządkowy", primary_key=True, editable=True)
    name = models.CharField(u"Imie", max_length=CHAR_FIELD_MAX_LEN, )
    surname = models.CharField(u"Nazwisko", max_length=CHAR_FIELD_MAX_LEN)
    srodowisko = models.ForeignKey('Dictionary', verbose_name=u"Środowisko",
                                   limit_choices_to={'type' : 'Srodowisko', 'active': True}, related_name='+', blank=True, null=True)
    troop = models.ForeignKey('Dictionary', verbose_name=u"Drużyna", limit_choices_to={'type' : 'Troop', 'active' : True},  related_name='+')
    book_no = models.CharField(u"Numer książeczki", max_length=CHAR_FIELD_MAX_LEN)
    issue_date = models.DateField(u"Data wydania", blank=True, null=True)

    def clean(self):
        if self.pk is None and self.issue_date is None:
            self.issue_date = datetime.today()

class Uprawnienie(models.Model):
    class Meta:
        abstract = True
        ordering = ['id']

    id = models.AutoField(u"Numer porządkowy", primary_key=True, editable=True)
    name = models.CharField(u"Imie", max_length=CHAR_FIELD_MAX_LEN, )
    surname = models.CharField(u"Nazwisko", max_length=CHAR_FIELD_MAX_LEN)
    uprawnienie = models.ForeignKey('Dictionary', verbose_name=u"Rodzaj uprawnienia",
                                    limit_choices_to={'type' : 'Uprawnienie', 'active' : True},
                                    related_name='+')
    rozkaz = models.CharField(u"Rozkaz", max_length=CHAR_FIELD_MAX_LEN)
    srodowisko = models.ForeignKey('Dictionary', verbose_name=u"Środowisko",
                                    limit_choices_to={'type' : 'Srodowisko', 'active': True},
                                    related_name='+', blank=True, null=True)

class ScoutBookMeta:
    verbose_name = u"Książeczka harcerska"
    verbose_name_plural = u"Rejestr książeczek harcerskich"
    unique_together = (
        ('book_no', ),
    )

class UprawnienieMeta:
    verbose_name = u"Rejestr wydanych uprawnień"
    verbose_name_plural = u"Rejestr wydanych uprawnień"


ScoutBookRegistry, ScoutBookHistory = create_record_types_abstract_model(
    ScoutBook, 'ScoutBookRegistry', 'ScoutBookHistory', registry_meta=ScoutBookMeta)

UprawnienieRegistry, UprawnienieRegistryHistory = create_record_types_abstract_model(
    Uprawnienie, 'UprawnienieRegistry', 'UprawnienieRegistryHistory', registry_meta=UprawnienieMeta)

