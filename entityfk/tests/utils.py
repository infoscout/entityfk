from django.db import models
from entityfk.entityfk import EntityForeignKey
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

class Article(models.Model):
    name = models.CharField(max_length=128)
    class EntityFKMeta(object):
        pk = "name"
