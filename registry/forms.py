# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from django.forms.widgets import Select
from django.utils.safestring import mark_safe
from django.contrib.localflavor.pl.forms import PLPostalCodeField


__author__ = 'jb'

from django.forms import ChoiceField, ModelForm, TypedChoiceField, ModelChoiceField

from django.db import models
from models import Dictionary, Adress

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

class TroopSrodowField(ModelChoiceField):
    def label_from_instance(self, obj):
            if obj is None:
                return ''
            return u"{obj.name} ({active})".format(obj = obj, active = "+" if obj.active else "-")

class ScoutForm(DictionayModelForm):
    class Meta:
        from models import ScoutBook
        model = ScoutBook

    troop = TroopSrodowField(queryset=Dictionary.objects.filter(type = 'troop', active=True))
    srodowisko = TroopSrodowField(queryset=Dictionary.objects.filter(type = 'Srodowisko', active=True), required=False)

class UprawkoForm(DictionayModelForm):
    class Meta:
        from models import Uprawnienie
        model = Uprawnienie

class CityField(ModelChoiceField):

    def label_from_instance(self, obj):
        if obj is None:
            return ''
        return obj.name



class AdressForm(DictionayModelForm):
    class Meta:
        from models import Adress
        model = Adress

    city = CityField(queryset=Dictionary.objects.filter(type = 'city', active = True))
    postalcode = PLPostalCodeField()


def build_corespondence_owner_queryset():
    from django.contrib.auth.models import User
    return User.objects.filter(Q(is_superuser = True) or Q(user_permissions__codename = "can_be_correspondence_owner")
        or Q(groups__permissions__codename =  "can_be_correspondence_owner"))

class AdressChoiceField(ModelChoiceField):
    def label_from_instance(self, value):
        if value is None:
            return self.empty_label
        return mark_safe(u"<strong>{adr.name}</strong> <em>Adres:</em> "
                    u"{adr.street} {adr.no} {adr.postalcode} {adr.city.name}".format(adr = value))

class CorrespondenceForm(DictionayModelForm):
    class Meta:
        from models import Corresponcence
        model = Corresponcence


    responsible = ModelChoiceField(build_corespondence_owner_queryset())
    adress = AdressChoiceField(Adress.objects.all())


