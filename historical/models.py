# -*- coding: utf-8 -*-
from django.db.models.fields.related import ForeignKey

__author__ = 'jb'

__LICENSE__ = u"""
    This file is part of Hufrce Program.

    This code is modified version of code discussed in chapter 11 of "Pro Django" book
    by Marty Alchin. It is relicensed wih my changes under GPL license. You can obtain
    original version of the code licensed under BSD from

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


import copy
import datetime

from django.db import models
from django.db.models.loading import get_model
from django.db.models import loading

from current_user import models as current_user
import manager

MODE_NO = 'none'
MODE_ON_HISTORY_TABLE = 'history'
MODE_ALWAYS = 'always'

__FIELD_ATTRS = (
    'verbose_name', 'name', 'primary_key', 'max_length', 'unique', 'blank', 'null', 'db_index',
    'rel', 'default', 'editable', 'serialize', 'unique_for_date', 'unique_for_month', 'unique_for_year',
    'choices', 'help_text', 'db_column', 'db_tablespace',  'validators', 'error_messages'
)

def __get_field_attrs(field):
    attrs = {}
    for f in __FIELD_ATTRS:
        attrs[f] = getattr(field, f)

    return attrs

def _create_new_fk(field, cls, **kwargs):
    attrs = __get_field_attrs(field)
    attrs.update(kwargs)
    return cls(**attrs)

def _get_to(app_label, to):
    if isinstance(to, str):
         splitted = to.split('.')
         if len(splitted) == 1:
             rel_to = get_model(app_label, splitted[0])
         else:
             rel_to = get_model(splitted[0], splitted[1])
         return rel_to
    return to



class HistoricalForeignKey(ForeignKey):

    class KeyToHistoryMarker(ForeignKey):
        pass

    def __init__(self, to, *largs, **kwargs):
        super(HistoricalForeignKey, self).__init__(to, *largs, **kwargs)

    def contribute_to_class(self, cls, name):
        super(HistoricalForeignKey, self).contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self.check_history_object, sender=cls)

    def check_history_object(self, **kwargs):
        rel_to = self.rel.to
        rel_to = _get_to(self.model._meta.app_label, rel_to)
        if getattr(rel_to, '_history_meta', None) is None:
            raise ValueError("HistoricalForeignKey %s.%s is pointing to class '%s' that has no history manager" % (self.model.__name__, self.name, rel_to.__name__))

class HistoricalOptions(object):
    def __init__(self, app_name, history_manager_name, history_model_name):
        super(HistoricalOptions, self).__init__()
        self.app_name = app_name
        self.history_manager_name=history_manager_name
        self.history_object_name=history_model_name

    @property
    def HistoryModel(self):
        return get_model(self.app_name, self.history_object_name)


class HistoricalRecords(object):
    def contribute_to_class(self, cls, name):
        self.manager_name =name
        models.signals.class_prepared.connect(self.finalize, sender=cls)


    def finalize(self, sender, **kwargs):
        self.app_name = sender._meta.app_label
        self.model_name = sender._meta.object_name
        history_model = self.create_history_model(sender)

        # The HistoricalRecords object will be discarded,
        # so the signal handlers can't use weak references.
        models.signals.post_save.connect(self.post_save, sender=sender,
                                         weak=False)
        models.signals.post_delete.connect(self.post_delete, sender=sender,
                                           weak=False)

        descriptor = manager.HistoryDescriptor(history_model)
        setattr(sender, self.manager_name, descriptor)
        setattr(sender, '_history_meta', HistoricalOptions(self.app_name, self.manager_name, history_model._meta.object_name))

    def create_history_model(self, model):
        """
        Creates a historical model to associate with the model provided.
        """
        attrs = self.copy_fields(model)
        attrs.update(self.get_extra_fields(model))
        attrs.update(Meta=type('Meta', (), self.get_meta_options(model)))
        name = 'Historical%s' % model._meta.object_name
        return type(name, (models.Model,), attrs)

    def copy_fields(self, model):
        """
        Creates copies of the model's original fields, returning
        a dictionary mapping field name to copied field object.
        """
        # Though not strictly a field, this attribute
        # is required for a model to function properly.
        fields = {'__module__': model.__module__}

        for field in model._meta.fields:
            field = copy.copy(field)

            if isinstance(field, models.AutoField):
                # The historical model gets its own AutoField, so any
                # existing one must be replaced with an IntegerField.
                field.__class__ = models.IntegerField

            if field.primary_key or field.unique:
                # Unique fields can no longer be guaranteed unique,
                # but they should still be indexed for faster lookups.
                field.primary_key = False
                field._unique = False
                field.db_index = True

            if isinstance(field, HistoricalForeignKey):
                rel_class = type(field.rel)
                rel_to = _get_to(model._meta.app_label, field.rel.to)
                field = _create_new_fk(field, HistoricalForeignKey.KeyToHistoryMarker,
                                        to = rel_to._history_meta.HistoryModel, rel_class = rel_class)

            fields[field.name] = field

        return fields

    def get_extra_fields(self, model):
        """
        Returns a dictionary of fields that will be added to the historical
        record model, in addition to the ones returned by copy_fields below.
        """
        rel_nm = '_%s_history' % model._meta.object_name.lower()
        return {
            'history_id': models.AutoField(primary_key=True),
            'history_date': models.DateTimeField(auto_now_add=True, db_index=True),
            'history_user': current_user.CurrentUserField(related_name=rel_nm),
            'history_type': models.CharField(max_length=1, choices=(
                ('+', 'Created'),
                ('~', 'Changed'),
                ('-', 'Deleted'),
            )),
            'current' : models.BooleanField(editable=False, default=False),
            'history_object': HistoricalObjectDescriptor(model),
            '__unicode__': lambda self: u'%s as of %s' % (self.history_object,
                                                          self.history_date)
        }

    def get_meta_options(self, model):
        """
        Returns a dictionary of fields that will be added to
        the Meta inner class of the historical record model.
        """
        return {
            'ordering': ('-history_date',),
        }

    def post_save(self, instance, created, **kwargs):
        self.create_historical_record(instance, created and '+' or '~')

    def post_delete(self, instance, **kwargs):
        self.create_historical_record(instance, '-')

    def create_historical_record(self, instance, type):
        manager = getattr(instance, self.manager_name)
        attrs = {}
        for field in instance._meta.fields:
            if isinstance(field, HistoricalForeignKey.KeyToHistoryMarker):
                related_instance = getattr(instance, field.attname)
                result = None
                if related_instance is not None:
                    history_manager = getattr(related_instance, type(related_instance)._meta.custom_history_manager_name)
                    result = history_manager.most_recent()
                attrs[field.attname] = result
            else:
                attrs[field.attname] = getattr(instance, field.attname)

        attrs['current'] = True
        manager.create(history_type=type, **attrs)

class HistoricalObjectDescriptor(object):
    def __init__(self, model):
        self.model = model

    def __get__(self, instance, owner):
        values = (getattr(instance, f.attname) for f in self.model._meta.fields)
        return self.model(*values)


class TestHistorySimple(models.Model):

    test_field = models.CharField(max_length=250)
    history = HistoricalRecords()

class TestRelatedTo(models.Model):

    test_field = models.CharField(max_length=250)
    history = HistoricalRecords()
