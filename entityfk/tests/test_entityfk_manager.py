from __future__ import absolute_import

from contextlib import contextmanager

from django.test import TestCase
from mock import patch
from django.apps import apps
from django.contrib import admin

from entityfk import managers, providers, entityfk
from entityfk.tests.models import AuthorTag, Book, AuthorTagNoEntityFK


@contextmanager
def mock_ourmodels():
    with patch.object(providers.apps, 'get_models', return_value=[AuthorTag, Book, AuthorTagNoEntityFK]):
        try:
            old_providers = providers.providers
            providers.providers = [providers.DjangoModelProvider()]
            yield
        finally:
            providers.providers = old_providers

class EntityFKManagerTestCase(TestCase):

    def test_filter_by_instance(self):
        with mock_ourmodels():
            b = Book.objects.create(pk=1)
            a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
            tags = AuthorTag.objects.filter_entity(b)
            self.assertIsNotNone(tags)
            self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_none(self):
        with mock_ourmodels():
            b = Book.objects.create(pk=1)
            a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
            tags = AuthorTag.objects.filter_entities(None)
            self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_no_fkentity_field(self):
        with mock_ourmodels():
            with self.assertRaises(ValueError):
                a = AuthorTagNoEntityFK.objects.create(tag_name="nice")
                book_1 = Book.objects.create(pk=34)
                tags = AuthorTagNoEntityFK.objects.filter_entity(book_1)

    def test_no_fkentity_field_fieldname(self):
        with mock_ourmodels():
            with self.assertRaises(ValueError):
                b = Book.objects.create(pk=1)
                a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
                tags = AuthorTag.objects.filter_entity(b,"entity_thing")

    def test_filter_with_entity_object(self):
        with mock_ourmodels():
            b = Book.objects.create(pk=1)
            a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
            tags = AuthorTag.objects.filter(entity_object=b)
            self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_ref(self):
        with mock_ourmodels():
            b = Book.objects.create(pk=1)
            ref = entityfk.entity_ref(b)
            a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
            tags = AuthorTag.objects.filter_entity(ref, refs_provided=True)
            self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_obj(self):
        with mock_ourmodels():
            b = Book.objects.create(pk=1)
            a = AuthorTag.objects.create(tag_name="cool_tag", entity_object=b)
            tags = AuthorTag.objects.filter(entity=b)
            self.assertIs(type(tags), managers.EntityFKQuerySet)
