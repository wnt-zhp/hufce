# -*- coding: utf-8 -*-
__author__ = 'jb'

from django.test import TestCase

import unittest

from django.db import models

import models as hmodels

class TestHistorySimple(models.Model):
    test_field = models.CharField(max_length=250)
    history = hmodels.HistoricalRecords()

class TestRelatedTo(models.Model):
    test_field = models.CharField(max_length=250)
    history = hmodels.HistoricalRecords()

class TestParent(models.Model):
    test_field = models.CharField(max_length=250)
    history = hmodels.HistoricalRecords()
    related = hmodels.HistoricalForeignKey("TestRelatedTo")


class TestGetModelClass(unittest.TestCase):

    def test1(self):
        self.assertEquals(hmodels.get_history_parent(TestHistorySimple), TestHistorySimple)

    def test2(self):
        self.assertEquals(hmodels.get_history_parent(hmodels.get_model('historical', "HistoricalTestHistorySimple")), TestHistorySimple)

    def test3(self):
        self.assertEquals(hmodels.get_history_parent(hmodels.get_model('historical', "HistoricalTestHistorySimple")()), TestHistorySimple)

    def test4(self):
          self.assertEquals(hmodels.get_history_parent(TestHistorySimple()), TestHistorySimple)

    def test5(self):
        self.assertEquals(hmodels.get_history_parent('HistoricalTestHistorySimple', 'historical'), TestHistorySimple)

    def test6(self):
        self.assertEquals(hmodels.get_history_parent('HistoricalTestHistorySimple', 'historical'), TestHistorySimple)


class TestGetHistoryClass(unittest.TestCase):

    def setUp(self):
        self.history_model = hmodels.get_model('historical', "HistoricalTestHistorySimple")

    def test1(self):
        self.assertEquals(hmodels.get_history_model(TestHistorySimple), self.history_model)

    def test2(self):
        self.assertEquals(hmodels.get_history_model(hmodels.get_model('historical', "HistoricalTestHistorySimple")), self.history_model)

    def test3(self):
        self.assertEquals(hmodels.get_history_model(hmodels.get_model('historical', "HistoricalTestHistorySimple")()), self.history_model)

    def test4(self):
          self.assertEquals(hmodels.get_history_model(TestHistorySimple()), self.history_model)

    def test5(self):
        self.assertEquals(hmodels.get_history_model('HistoricalTestHistorySimple', 'historical'), self.history_model)

    def test6(self):
        self.assertEquals(hmodels.get_history_model('HistoricalTestHistorySimple', 'historical'), self.history_model)



class HistorySimpleTest(TestCase):

    def setUp(self):
        super(HistorySimpleTest, self).setUp()

    def test_meta_model(self):
        test = TestHistorySimple()
        test._history_meta.HistoryModel

    def test_meta_model_name(self):
        test = TestHistorySimple()
        test._history_metahistory_model_name

    def test_meta_model_name(self):
        test = TestHistorySimple()
        test._history_meta.history_manager_name

    def test_create(self):
        test = TestHistorySimple()
        test.save()
        self.assertGreater(len(TestHistorySimple._history_meta.HistoryModel.objects.all()), 0)

    def test_create_2(self):
        test = TestHistorySimple()
        test.save()
        test.save()
        self.assertEquals(len(TestHistorySimple._history_meta.HistoryModel.objects.all()),2)

    def test_current_parent(self):
        test = TestHistorySimple()
        test.save()
        historic = test.history.all()[0]
        self.assertEquals(hmodels.get_current_parent(historic), test)


class TestHistoryForeignKey1(TestCase):

    def setUp(self):
        self.related_to_1 = TestRelatedTo(test_field = 'baz')
        self.related_to_2 = TestRelatedTo(test_field = 'bar')
        self.related_to_1.save()
        self.related_to_2.save()
        self.test_parent = TestParent(test_field = "foo")
        self.test_parent.related = self.related_to_1
        self.test_parent.save()

    def test_foreign_key(self):
        self.assertEquals(self.related_to_1, self.test_parent.related)

    def test_foreign_back(self):
        history_instance = self.test_parent.history.all()[0]
        self.assertTrue(isinstance(history_instance.related, TestRelatedTo._history_meta.HistoryModel))

    def test_history_size(self):
        self.assertEquals(1, len(self.test_parent.history.all()))
        self.assertEquals(1, len(self.related_to_1.history.all()))
        self.assertEquals(1, len(self.related_to_2.history.all()))
