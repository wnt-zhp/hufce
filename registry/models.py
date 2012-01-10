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

from django.db import models

# Create your models here.

CHAR_FIELD_MAX_LEN = 250


class RecordHistory(models.Model):
    class Meta:
        abstract = True
        ordering = ('save_date', )

#    parent_instance = models.ForeignKey(Meta.registry_parent, blank=False, null=False)
    save_date = models.DateField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None):
        assert not force_update
        force_insert = True
        super(RecordHistory, self).save(force_insert, force_update, using)


class Record(models.Model):

    registry_child = None

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None):
        if self.pk is not None and not force_update:
            old = type(self).objects.get(pk = self.pk)
            hist = self.create_history_objecy()
            hist.save()
        super(Record, self).save(force_insert, force_update, using)

    def create_history_objecy(self):
        hist =  self.registry_child()
        hist.parent_instance = self

        for field in self._meta.fields:
            if not field.primary_key:
                setattr(hist, field.name, getattr(self, field.name, None))
        return hist


class Srodowisko(models.Model):

    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN)

class Troop(models.Model):

    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN)

class ScoutBook:
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    surname = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    srodowisko = models.ForeignKey('Srodowisko')
    troop = models.ForeignKey('Troop')
    book_no = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    issue_date = models.DateField(blank=True, null=False)


class ScoutBookHistory(ScoutBook, RecordHistory):
    parent_instance = models.ForeignKey("ScoutBookRegistry", blank=False, null=False, related_name='history')


class ScoutBookRegistry(ScoutBook, Record):
    registry_child = ScoutBookHistory
