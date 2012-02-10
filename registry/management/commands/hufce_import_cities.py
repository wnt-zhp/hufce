# -*- coding: utf-8 -*-
__author__ = 'jb'
from django.core.management.base import NoArgsCommand

import codecs
from registry import models

class Command(NoArgsCommand):



    def handle_noargs(self, **options):
        with codecs.open('registry/data/cities.txt', encoding='utf-8') as f:
            for line in f:
                models.Dictionary.objects.get_or_create(
                    type = 'city',
                    name = line.strip()
                )

