from django.db import models
from django.utils import unittest
from entityfk.entityfk import EntityForeignKey, entity_label, \
    entity_instance, entity_model
from entityfk.managers import EntityFKManager

class AuthorTag(models.Model):
    """ 
    Fake models to use for testing
    """
    
    objects = EntityFKManager()
    
    tag_name = models.CharField(max_length=32)    
    entity_object = EntityForeignKey()
    entity = models.CharField(max_length=32, null=False)
    entity_id = models.PositiveIntegerField(null=False)
    
class Book(models.Model):
    name = models.CharField(max_length=128)
    

class EntityFKTestCase(unittest.TestCase):
    
    def setUp(self):

        self.book1 = Book.objects.create(name="A great book")
        
    def test_mapping(self):
        
        # Get label from instance and convert back to class
        label = entity_label(self.book1)
        _Book = entity_model(label)
        self.assertEqual(Book, _Book)
        
        book = entity_instance(label, self.book1.id)
             
    def test_entityfk(self):
        
        # Save author tag, then retrieve it
        author_tag = AuthorTag.objects.create(tag_name="tag1", entity_object=self.book1)
        tag_id = author_tag.id
        
        _author_tag = AuthorTag.objects.get(pk=tag_id)
        _book1 = _author_tag.entity_object
        self.assertEqual(self.book1, _book1)
        
        # Try the queryset filter
        tags = AuthorTag.objects.filter(entity_object=self.book1).all()
        self.assertEqual(tags[0].entity_object, self.book1)
        
        # Try querying against the entity
        tags2 = AuthorTag.objects.filter(entity=Book).all()
        self.assertEqual(tags[0].entity_object, self.book1)
        
