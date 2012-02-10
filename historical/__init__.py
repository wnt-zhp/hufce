# -*- coding: utf-8 -*-
"""
    This module implements generic method of preserving historical values of models.


    NOMENCLATURE
    ============

    I was having some problems with properly naming stuff so if you add field of type
    `HistoricalRecords` to a model this model is named *History Parent*, and generated
    on the fly class to hold historical values is called *History class*.


    Enabling history
    ================

    To enable mechanism of preserving historical values you need add special field to this class::
        class Model(models.Model)
            name_field = models.CharField(max_length=250)
            history = hmodels.HistoricalRecords()

    history attribute will also serve as a manager for historical values (it supports all
    usual manager methods and some more, please see :class:`HistoryManager`.

    Handling of ForeignKeys
    -----------------------

    ForeignKeys are treated in no special way --- primary key values are preserved in history.

    But, if both parent and child in `ForeignKey` relation have enabled history, and you use one
    of two special subclasses of `ForeignKey`, that is: :class:`HistoricalForeignKey` and
    :class:`ConvertToHistoryForeignKey` behaviour is changed.


    Handiling of HistoricalForeignKeys
    -----------------------------------

    Lets assume we have following models::

        class Foo(models.Model):
            history = hmodels.HistoricalRecords()
            related = hmodels.HistoricalForeignKey('Bar')

    In this case ValueError will be raised during model creation phase if preserving history is
    not enabled for 'Bar' model.

    Behaviour of parent is unchanged, but historical values of 'Foo' will relate to 'BarHistory'.
    New  historical records will have most current historical value assigned to them.

    TODO: At some point I might enable automatical save of new version of 'Foo' if 'Bar' it
    is related to is changed.




    AUTHOR
    ======

    This code is based on code from chapter 11 of Pro Django book by Andy Martin, but this code
    has been extended for sensible support of foreign keys in models with enabled history.

    Limitations
    ===========

    This module is not build to be very fast --- if you have milion of rows most probably you will
    need to enable faster alternative, that most probably needs lots of custom SQL.

    There is no automatical handling for OneToOne relations --- ie. they are treated as ForeignKeys
"""

__author__ = 'jb'

