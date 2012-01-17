# -*- coding: utf-8 -*-
__author__ = 'jb'

from django.test import TestCase

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


class TestHistorySimple(TestCase):

    def setUp(self):
        super(TestHistorySimple, self).setUp()

    def test_meta_model(self):
        test = hmodels.TestHistorySimple()
        test._history_meta.HistoryModel

    def test_meta_model_name(self):
        test = hmodels.TestHistorySimple()
        test._history_metahistory_model_name

    def test_meta_model_name(self):
        test = hmodels.TestHistorySimple()
        test._history_meta.history_manager_name

    def test_create(self):
        test = hmodels.TestHistorySimple()
        test.save()
        self.assertGreater(len(hmodels.TestHistorySimple._history_meta.HistoryModel.objects.all()), 0)

    def test_create_2(self):
            test = hmodels.TestHistorySimple()
            test.save()
            test.save()
            self.assertEquals(len(hmodels.TestHistorySimple._history_meta.HistoryModel.objects.all()),2)


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
