# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from entityfk import entityfk
from entityfk.tests.models import Book

from mock import patch


class EntityFKMethodsTestCase(TestCase):

    def test_entity_label(self):
        self.assertEqual(entityfk.entity_label(Book(pk=1)), "tests.book")

    def test_entity_label_fail(self):
        with self.assertRaises(ValueError):
            entityfk.entity_label("apple")

    def test_entity_ref(self):
        self.assertEqual(entityfk.entity_ref(Book(pk=1)), ("tests.book", 1))

    def test_entity_ref_fail(self):
        with self.assertRaises(ValueError):
            entityfk.entity_ref("kisnyul")

    def test_entity_model(self):
        self.assertEqual(entityfk.entity_model('tests.book'), Book)

    def test_entity_model_fail(self):
        with self.assertRaises(Exception):
            entityfk.entity_model('tests.book2')

    def test_entity_instance(self):
        with patch.object(Book.objects, 'get', return_value=None) as getter:
            entityfk.entity_instance("tests.book", 1)
            getter.assert_called_once_with(pk=1)

    def test_entity_instance_fail(self):
        with self.assertRaises(Exception):
            entityfk.entity_instance("tests.books", 1)
