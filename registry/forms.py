# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q

__author__ = 'jb'

from django.forms import ChoiceField, ModelForm

from django.db import models
from models import Dictionary

class DictionayModelForm(ModelForm):

    def __init__(self, *largs, **kwargs):
        super(DictionayModelForm, self).__init__(*largs, **kwargs)
        if self.instance and self.instance.pk is not None:
            for f in self.instance._meta.fields:
                if isinstance(f, models.ForeignKey) and issubclass(f.rel.to, Dictionary):
                    model_field = self.fields[f.name]
                    value = getattr(self.instance, f.name, None)
                    if value and value not in model_field.choices:
                        model_field.queryset = Dictionary.objects.filter(Q(**f.rel.limit_choices_to) | Q(id = value.id))

class ScoutForm(DictionayModelForm):
    class Meta:
        from models import ScoutBookRegistry
        model = ScoutBookRegistry
    pass

class UprawkoForm(DictionayModelForm):
    class Meta:
        from models import UprawnienieRegistry
        model = UprawnienieRegistry
