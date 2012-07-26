## -*- coding: utf-8 -*-
from django.contrib.localflavor.pl.forms import PLPostalCodeField
from django.core.exceptions import ValidationError
from django.db.models.expressions import F
from django.db.models.sql.aggregates import Max
from django.db.transaction import commit_unless_managed
from django.forms.fields import RegexField


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
#from registry_engine.models import create_record_types_abstract_model
from const import CHAR_FIELD_MAX_LEN
from datetime import datetime, date
from historical.models import HistoricalRecords, HistoricalForeignKey

from current_user.models import CurrentUserField

from django.utils.translation import ugettext_lazy as _

from django.utils.translation import ugettext_lazy

DICTIONARY_CHOICES = (
    ('Srodowisko', 'Srodowisko'),
    ('Troop', 'Drużyna'),
    ("Uprawnienie", "Uprawnienie"),
    ('city', "Miasto"),
    ('corr-stat', "Status korespondencji")
)

class Dictionary(models.Model):
    class Meta:
        verbose_name = u"Słownik"
        verbose_name_plural = u"Słowniki"

    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, verbose_name="Nazwa")
    active = models.BooleanField(verbose_name="Aktywny", help_text="Czy dany rekord może być przypisywany do innych obiektów", default=True)
    type = models.CharField(max_length=CHAR_FIELD_MAX_LEN, choices=DICTIONARY_CHOICES)
    user_changed = CurrentUserField()

    def __unicode__(self):
        return ' '.join(('+' if self.active else '-', self.name, self.type))
#
class ScoutBook(models.Model):
    class Meta:
        verbose_name = u"Ksiżeczka harcerska"
        verbose_name_plural = u"Rejestr książeczek harcerskich"
        ordering = ['id']

    id = models.AutoField(u"Numer porządkowy", primary_key=True, editable=True)
    name = models.CharField(u"Imie", max_length=CHAR_FIELD_MAX_LEN, )
    surname = models.CharField(u"Nazwisko", max_length=CHAR_FIELD_MAX_LEN)
    srodowisko = models.ForeignKey('Dictionary', verbose_name=u"Środowisko",
                                   limit_choices_to={'type' : 'Srodowisko', 'active': True}, related_name='+', blank=True, null=True)
    troop = models.ForeignKey('Dictionary', verbose_name=u"Drużyna", limit_choices_to={'type' : 'Troop', 'active' : True},  related_name='+')
    book_no = models.CharField(u"Numer książeczki", max_length=CHAR_FIELD_MAX_LEN, unique=True)
    issue_date = models.DateField(u"Data wydania", blank=True, null=True)

    user_changed = CurrentUserField()
    historical = HistoricalRecords()


    def clean(self):
        if self.pk is None and self.issue_date is None:
            self.issue_date = datetime.today()
#
class Uprawnienie(models.Model):
    class Meta:
        verbose_name = u"Wydane uprwanienie"
        verbose_name_plural = u"Rejestr wydanych uprawnień"
        ordering = ['id']

    id = models.AutoField(u"Numer porządkowy", primary_key=True, editable=True)
    name = models.CharField(u"Imie", max_length=CHAR_FIELD_MAX_LEN, )
    surname = models.CharField(u"Nazwisko", max_length=CHAR_FIELD_MAX_LEN)
    uprawnienie = models.ForeignKey('Dictionary', verbose_name=u"Rodzaj uprawnienia",
                                    limit_choices_to={'type' : 'Uprawnienie', 'active' : True},
                                    related_name='+')
    rozkaz = models.CharField(u"Rozkaz", max_length=CHAR_FIELD_MAX_LEN)
    date = models.DateField(u"Data przyznania", blank=True, null=True)

    srodowisko = models.ForeignKey('Dictionary', verbose_name=u"Środowisko",
                                    limit_choices_to={'type' : 'Srodowisko', 'active': True},
                                    related_name='+', blank=True, null=True)

    druzyna = models.ForeignKey("Dictionary", verbose_name=u"Drużyna",
                                            limit_choices_to={'type' : 'Troop', 'active' : True},
                                            related_name="+", blank=True, null=True)

    user_changed = CurrentUserField()
    historical = HistoricalRecords()

    def save(self, force_insert=False, force_update=False, using=None):
        if self.date is None:
            self.date = date.today()
        super(Uprawnienie, self).save(force_insert, force_update, using)

    def clean(self):
        if self.srodowisko is None and self.druzyna is None:
            raise ValidationError(u"Musisz podać albo drużyne albo środowisko")

class Adress(models.Model):

    class Meta:
        verbose_name = "Adres"
        verbose_name_plural = "Adresy"

    name = models.CharField("Nazwa odbiorcy", max_length=CHAR_FIELD_MAX_LEN)

    no = models.CharField("Numer domu/mieszkania", max_length=CHAR_FIELD_MAX_LEN)
    street = models.CharField("Ulica", max_length=CHAR_FIELD_MAX_LEN)
    city = models.ForeignKey("Dictionary", verbose_name="Miasto", related_name='+', limit_choices_to={'type' : 'city', 'active' : True},)
    postalcode = models.CharField(verbose_name = "Kod pocztowy", max_length=CHAR_FIELD_MAX_LEN)

    user_changed = CurrentUserField()
    historical = HistoricalRecords()

    def __unicode__(self):
        return "Stree"

class Corresponcence(models.Model):
    class Meta:
        verbose_name = "Korespondencja przychodząca"
        verbose_name_plural = "Rejestr korespondencji przychodzącej"
        permissions = (
            ("can_be_correspondence_owner", u"Może być właścicielem korespondencji"),)


    number = models.AutoField(primary_key=True, verbose_name="Numer")
#    confidential = models.CharField("Tajność", choices=(('j', 'Jawne'), ('t', 'Tajne')), max_length=1, default='j', blank=False, null=False)
    data = models.DateField(u"Data rejestracji", help_text=u"Nie musisz wypełniać tego pola --- domyślnie będzie to dziś.", editable=True)
#    type = models.CharField("Typ dokumentu", choices=(('p', u'Przychodzący'), ('w', u'Wychodzący')), max_length=1, default='p', blank=False, null=False)
    adress = HistoricalForeignKey('Adress', verbose_name = 'Nadawca')
    subject = models.TextField(u"Temat wiadomości", blank=False, null=False)
    institution_no = models.CharField(u"Numer urzędowy", blank=True, null=True, help_text=u"Numer nadany przez nadawcę", max_length=CHAR_FIELD_MAX_LEN)
    remarks = models.TextField(u"Uwagi", blank=True, null=False)
    status = models.ForeignKey("Dictionary", related_name="+", limit_choices_to={"type" : 'corr-stat', 'active' : True}, verbose_name=u"Status przesyłki")
    responsible = models.ForeignKey("auth.User",
                                    related_name='+', verbose_name=u"Osoba odpowiedzialna",
                                    blank=True, null=True
    )

    user_changed = CurrentUserField()
    historical = HistoricalRecords()

    def save_base(self, raw=False, cls=None, origin=None, force_insert=False, force_update=False,
                  using=None):
        if self.data is None:
            self.data = date.today()
        super(Corresponcence, self).save_base(raw, cls, origin, force_insert, force_update, using)












