# -*- coding: utf-8 -*-
from django.db.models.fields.related import ForeignKey
from current_user.models import CurrentUserField
from django.contrib.auth.models import User
from django.dispatch.dispatcher import Signal

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

from _south import try_initialize_south
try_initialize_south()

__FIELD_ATTRS = (
    'verbose_name', 'name', 'primary_key', 'max_length', 'unique', 'blank', 'null', 'db_index',
    'rel', 'default', 'editable', 'serialize', 'unique_for_date', 'unique_for_month',
    'unique_for_year',
    'choices', 'help_text', 'db_column', 'db_tablespace', 'validators', 'error_messages'
    )

def __get_field_attrs(field):
    attrs = {}
    for f in __FIELD_ATTRS:
        attrs[f] = getattr(field, f)

    return attrs


def _create_new_fk(field, cls = ForeignKey, **kwargs):
    attrs = __get_field_attrs(field)
    attrs.update(kwargs)
    return cls(**attrs)


def _get_model(model, app_label = None):
    """
    Returns model class
    :param app_label:
    :param model: Either model class (in this case it is passed unchanged), or model name in format:
        "app_label.ModelName" or "ModelName". If second format is passed app_label defaults to
        value of 'app_label` parameter.
    :return: Returns model class
    """
    if isinstance(model, str):
        splitted = model.split('.')
        if len(splitted) == 1:
            rel_to = get_model(app_label, splitted[0])
        else:
            rel_to = get_model(splitted[0], splitted[1])
        return rel_to
    if isinstance(model, models.Model):
        return type(model)
    return model


def get_history_parent(model, app_label = None):
    """
    Returns model class that represents parent model for history model.

    If `model` represents a model class that is either History parent (that is a model for which
    field of type HistoricalRecords is defined, or a Historical model (model that holds history of
    HistoryParent). In this case history parent is returned.

    If normal model instance is passed ValueError is raised).


    :param app_label:
    :param model:
    :return:
    """

    model = _get_model(model, app_label)
    try:
        meta = model._history_meta
    except AttributeError:
        raise ValueError('Model %s passed to get_history_parent is neither history parent not history model' % model)
    return meta.ParentModel

def get_history_model(model, app_label = None):
    model = _get_model(model, app_label)
    try:
        meta = model._history_meta
    except AttributeError:
        raise ValueError('Model %s passed to get_history_parent is neither history parent not history model')
    return meta.HistoryModel

def get_current_parent(model):
    """
        Gets current instance of parent model given history model
    :param model:
    :return:
    """
    parent = get_history_parent(model)
    return getattr(model, parent.pk.attname)

class KeyToHistoryMarker(ForeignKey):
    pass

class HistoricalForeignKey(ForeignKey):
    def __init__(self, to, *largs, **kwargs):
        super(HistoricalForeignKey, self).__init__(to, *largs, **kwargs)

    def contribute_to_class(self, cls, name):
        super(HistoricalForeignKey, self).contribute_to_class(cls, name)
        models.signals.class_prepared.connect(self.check_history_object, sender=cls)

    def check_history_object(self, **kwargs):
        rel_to = self.rel.to
        rel_to = _get_model(rel_to, self.model._meta.app_label)

#        if getattr(rel_to, '_history_meta', None) is None:
#            raise ValueError(
#                "HistoricalForeignKey %s.%s is pointing to class '%s' that has no history manager" % (
#                    self.model.__name__, self.name, rel_to.__name__))

class ConvertToHistoryForeignKey(ForeignKey):
    check_history_object = HistoricalForeignKey.check_history_object
    contribute_to_class = HistoricalForeignKey.contribute_to_class

    def __init__(self, to, *largs, **kwargs):
        super(ConvertToHistoryForeignKey, self).__init__(to, *largs, **kwargs)

    def formfield(self, **kwargs):
        return super(ConvertToHistoryForeignKey, self).formfield(**kwargs)

class HistoricalOptions(object):
    def __init__(self, app_name, parent_model_name, history_manager_name, history_model_name,
                 is_parent):
        super(HistoricalOptions, self).__init__()
        self.app_name = app_name
        self.history_manager_name = history_manager_name
        self.parent_model_name = parent_model_name
        self.history_object_name = history_model_name
        self.is_parent = is_parent
        self.is_child = not is_parent

    @property
    def HistoryModel(self):
        return get_model(self.app_name, self.history_object_name)

    @property
    def ParentModel(self):
        return get_model(self.app_name, self.parent_model_name)

    @property
    def HistoryModelName(self):
        return ".".join((self.app_name, self.history_object_name))

    @property
    def ParentModelName(self):
        return ".".join((self.app_name, self.parent_model_name))

class HistoricalRecords(object):

    def contribute_to_class(self, cls, name):
        self.manager_name = name
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
        if not hasattr(sender, '_history_meta'):
            setattr(sender, '_history_meta', self.create_history_options(sender, True))


    def history_model_name(self, parent_model):
        return 'Historical%s' % parent_model._meta.object_name

    def create_history_options(self, model, is_parent):
        return  HistoricalOptions(self.app_name, model._meta.object_name, self.manager_name,
                                                        self.history_model_name(model), is_parent)

    def create_history_model(self, parent_model):
        """
        Creates a historical model to associate with the model provided.
        """
        attrs = self.copy_fields(parent_model)
        attrs.update(self.get_extra_fields(parent_model))
        attrs.update(Meta=type('Meta', (), self.get_meta_options(parent_model)))
        name = self.history_model_name(parent_model)

        historical_model_class = type(name, (models.Model,), attrs)
        setattr(historical_model_class, '_history_meta', self.create_history_options(parent_model, False))
        return historical_model_class

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

            if field.unique:
                # Unique fields can no longer be guaranteed unique,
                # but they should still be indexed for faster lookups.
                field._unique = False
                field.db_index = True

            if field.primary_key:
                field_ = _create_new_fk(field, to = model,
                                        related_name = '+',
                                        primary_key=False, unique=False, db_index = True)
                field = field_

            if isinstance(field, HistoricalForeignKey):
                rel_class = type(field.rel)
                rel_to = _get_model(field.rel.to, model._meta.app_label)
                field = _create_new_fk(field, KeyToHistoryMarker,
                                       to=rel_to._history_meta.HistoryModelName, rel_class=rel_class)

            if isinstance(field, CurrentUserField):
                field = _create_new_fk(field, to=User)

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
                ('-', 'Deleted'))
            ),
            'current': models.BooleanField(editable=False, default=False),
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
            if field.primary_key:
              attrs[field.attname] = instance
            elif isinstance(field, KeyToHistoryMarker):
                related_instance = getattr(instance, field.attname)
                result = None
                if related_instance is not None:
                    history_manager = getattr(related_instance, type(
                        related_instance)._meta.custom_history_manager_name)
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
