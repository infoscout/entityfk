from __future__ import absolute_import
from mock import patch
import unittest
from entityfk import providers
from entityfk.tests.utils import AuthorTag, Book
from entityfk.providers import TypeNotSupported


class ApiClientTestCase(unittest.TestCase):
    
    def setUp(self):
        with patch.object(providers.models, 'get_models', return_value=[AuthorTag, Book]):
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
        

if __name__ == "__main__":
    unittest.main()

