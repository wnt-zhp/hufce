# -*- coding: utf-8 -*-
__author__ = 'jb'


def try_initialize_south():
    try:
        import south
    except ImportError:
        # No south in pypath
        return
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^current_user\.models\.CurrentUserField"])

