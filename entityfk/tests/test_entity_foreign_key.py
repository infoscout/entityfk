# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from mock import patch

from entityfk.tests.models import AuthorTag, Book


class EntityForeignKeyTestCase(TestCase):

    def test_set(self):
        b = AuthorTag()
        b.entity_object = Book(pk=1)
        self.assertEqual(b.entity, "tests.book")
        self.assertEqual(b.entity_id, 1)

    def test_set_with_entity_object_param(self):
        book = Book(pk=25)
        with patch.object(Book.objects, 'get', return_value=book):
            b = AuthorTag(entity_object=Book.objects.get())
            self.assertEquals(b.entity_object, book)

    def test_set_invalid(self):
        with self.assertRaises(ValueError):
            b = AuthorTag()
            b.entity_object = "apple"

    def test__get__none_instance(self):
        book = Book(pk=53)
        with patch.object(Book.objects, 'get', return_value=book):
            self.assertIsNotNone(AuthorTag.entity_object)

    def test_get_valid(self):
        book = Book(pk=53)
        with patch.object(Book.objects, 'get', return_value=book) as getter:
            b = AuthorTag()
            b.entity = "tests.book"
            b.entity_id = 53
            self.assertEquals(b.entity_object, book)
            getter.assert_called_once_with(pk=53)

    def test_get_invalid_id(self):
        with patch.object(Book.objects, 'get', side_effect=ObjectDoesNotExist):
            b = AuthorTag()
            b.entity = "tests.book"
            b.entity_id = -1
            self.assertEquals(b.entity_object, None)

    def test_get_invalid_label(self):
        with self.assertRaises(Exception):
            b = AuthorTag()
            b.entity = "tests.book2"
            b.entity_id = -1
            b.entity_object
