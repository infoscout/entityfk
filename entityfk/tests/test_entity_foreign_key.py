from __future__ import absolute_import

from contextlib import contextmanager

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from mock import patch

from entityfk import providers
from entityfk.tests.utils import AuthorTag, Book


@contextmanager
def mock_ourmodels():
    with patch.object(providers.apps, 'get_models', return_value=[AuthorTag, Book]):
        try:
            old_providers = providers.providers
            providers.providers = [providers.DjangoModelProvider()]
            yield
        finally:
            providers.providers = old_providers


class EntityForeignKeyTestCase(TestCase):
    def test_set(self):
        with mock_ourmodels():
            b = AuthorTag()
            b.entity_object = Book(pk=1)
            self.assertEqual(b.entity, "tests.book")
            self.assertEqual(b.entity_id, 1)

    def test_set_with_entity_object_param(self):
        with mock_ourmodels():
            with patch.object(Book.objects, 'get', return_value=Book(pk=25)) as getter:
                b = AuthorTag(entity_object=Book.objects.get())
                self.assertEquals(b.entity_object, Book(pk=25))

    def test_set_invalid(self):
        with mock_ourmodels():
            with self.assertRaises(ValueError):
                b = AuthorTag()
                b.entity_object = "apple"

    def test__get__none_instance(self):
        with mock_ourmodels():
            with patch.object(Book.objects, 'get', return_value=Book(pk=53)) as getter:
                self.assertIsNotNone(AuthorTag.entity_object)

    def test_get_valid(self):
        with mock_ourmodels():
            with patch.object(Book.objects, 'get', return_value=Book(pk=53)) as getter:
                b = AuthorTag()
                b.entity = "tests.book"
                b.entity_id = 53
                self.assertEquals(b.entity_object, Book(pk=53))
                getter.assert_called_once_with(pk=53)

    def test_get_invalid_id(self):
        with mock_ourmodels():
            with patch.object(Book.objects, 'get', side_effect=ObjectDoesNotExist):
                b = AuthorTag()
                b.entity = "tests.book"
                b.entity_id = -1
                self.assertEquals(b.entity_object, None)

    def test_get_invalid_label(self):
        with mock_ourmodels():
            with self.assertRaises(Exception):
                b = AuthorTag()
                b.entity = "tests.book2"
                b.entity_id = -1
                b.entity_object
