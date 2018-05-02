from __future__ import absolute_import

from contextlib import contextmanager

from django.test import TestCase
from mock import patch

from entityfk import providers, entityfk
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


class EntityFKMethodsTestCase(TestCase):

    def test_entity_label(self):
        with mock_ourmodels():
            self.assertEqual(entityfk.entity_label(Book(pk=1)), "tests.book")

    def test_entity_label_fail(self):
        with mock_ourmodels():
            with self.assertRaises(ValueError):
                entityfk.entity_label("apple")

    def test_entity_ref(self):
        with mock_ourmodels():
            self.assertEqual(entityfk.entity_ref(Book(pk=1)), ("tests.book", 1))

    def test_entity_ref_fail(self):
        with mock_ourmodels():
            with self.assertRaises(ValueError):
                entityfk.entity_ref("kisnyul")

    def test_entity_model(self):
        with mock_ourmodels():
            self.assertEqual(entityfk.entity_model('tests.book'), Book)

    def test_entity_model_fail(self):
        with mock_ourmodels():
            with self.assertRaises(Exception):
                entityfk.entity_model('tests.book2')

    def test_entity_instance(self):
        with mock_ourmodels():
            with patch.object(Book.objects, 'get', return_value=None) as getter:
                entityfk.entity_instance("tests.book", 1)
                getter.assert_called_once_with(pk=1)

    def test_entity_instance_fail(self):
        with mock_ourmodels():
            with self.assertRaises(Exception):
                entityfk.entity_instance("tests.books", 1)

if __name__ == "__main__":
    unittest.main()
