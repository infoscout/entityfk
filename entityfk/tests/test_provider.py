from __future__ import absolute_import

import unittest

from mock import patch

from entityfk import providers
from entityfk.tests.utils import AuthorTag, Book, Article
from entityfk.providers import TypeNotSupported


class DjangoModelProviderTestCase(unittest.TestCase):

    def setUp(self):
        with patch.object(providers.apps, 'get_models', return_value=[AuthorTag, Book, Article]):
            self.provider = providers.DjangoModelProvider()

    def test_to_ref_class(self):
        self.assertEquals(self.provider.to_ref(Book), ("tests.book", None))

    def test_to_ref_object(self):
        self.assertEquals(self.provider.to_ref(Book(pk=1)), ("tests.book", 1))

    def test_to_ref_fail(self):
        with self.assertRaises(TypeNotSupported):
            self.provider.to_ref("something")

    def test_to_object(self):
        with patch.object(Book.objects, 'get', return_value=None) as getter:
            self.provider.to_object(('tests.book', 1))
            getter.assert_called_once_with(pk=1)

    def test_to_model(self):
        self.assertEquals(self.provider.to_model("tests.book"), Book)

    def test_custom_pk_fromentity(self):
        self.assertEquals(self.provider.to_ref(Article(pk=1, name="Text")), ("tests.article", "Text"))

    def test_custom_pk_toentity(self):
        with patch.object(Article.objects, 'get', return_value=None) as getter:
            self.provider.to_object(('tests.article', "Text"))
            getter.assert_called_once_with(name="Text")


if __name__ == "__main__":
    unittest.main()
