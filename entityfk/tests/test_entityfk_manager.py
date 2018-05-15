from __future__ import absolute_import
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from contextlib import contextmanager

from django.apps import apps
from django.contrib import admin
from django.test import TestCase

from mock import patch

from entityfk import managers, providers, entityfk
from entityfk.tests.models import AuthorTag, Book, AuthorTagNoEntityFK


class EntityFKManagerTestCase(TestCase):

    def test_filter_by_instance(self):
        book = Book.objects.create(pk=1)
        book_2 = Book.objects.create(pk=2)
        author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
        author_tag_2 = AuthorTag.objects.create(tag_name="wow", entity_object=book_2)
        tags = AuthorTag.objects.filter_entity(book)
        self.assertEqual(len(tags), 1)
        self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_none(self):
        book = Book.objects.create(pk=1)
        author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
        book_2 = Book.objects.create(pk=2)
        author_tag_2 = AuthorTag.objects.create(tag_name="wow", entity_object=book_2)
        tags = AuthorTag.objects.filter_entities(None)
        self.assertIs(type(tags), managers.EntityFKQuerySet)
        self.assertEqual(len(tags), 2)

    def test_filter_no_fkentity_field(self):
        with self.assertRaises(ValueError):
            author_tag = AuthorTagNoEntityFK.objects.create(tag_name="nice")
            book = Book.objects.create(pk=34)
            tags = AuthorTagNoEntityFK.objects.filter_entity(book)

    def test_no_fkentity_field_no_fieldname(self):
        with self.assertRaises(ValueError):
            book = Book.objects.create(pk=1)
            author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
            tags = AuthorTag.objects.filter_entity(book, "nonexistent_field")

    def test_filter_with_entity_object(self):
        book = Book.objects.create(pk=1)
        author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
        tags = AuthorTag.objects.filter(entity_object=book)
        self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_ref(self):
        book = Book.objects.create(pk=1)
        ref = entityfk.entity_ref(book)
        author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
        tags = AuthorTag.objects.filter_entity(ref, refs_provided=True)
        self.assertIs(type(tags), managers.EntityFKQuerySet)

    def test_filter_with_obj(self):
        book = Book.objects.create(pk=1)
        author_tag = AuthorTag.objects.create(tag_name="cool_tag", entity_object=book)
        tags = AuthorTag.objects.filter(entity=book)
        self.assertIs(type(tags), managers.EntityFKQuerySet)
