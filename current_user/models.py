# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from _south import try_initialize_south

try_initialize_south()

import registration

class CurrentUserField(models.ForeignKey):
    def __init__(self, **kwargs):
        kwargs['null'] = True
        kwargs['to'] = User
        super(CurrentUserField, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        super(CurrentUserField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry()
        registry.add_field(cls, self)
