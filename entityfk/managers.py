from __future__ import absolute_import
from django.db.models import Manager
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from entityfk.entityfk import EntityForeignKey, entity_label, entity_ref
from entityfk import entityfk
import operator
import itertools

class EntityFKManager(Manager):
    """
    A manager that returns a GFKQuerySet instead of a regular QuerySet.

    """
    def filter_entities(self, entities, entity_field_name=None):
        """
        Filter for tags of entities
        Usefull for prefetching 
        """
        if not entities: return self.filter()
        entity_field_mapping = _get_entity_field_mapping(self.model)
        if not entity_field_mapping:
            raise ValueError("Model does not have EntityForeignKey field")
        if entity_field_name and entity_field_name not in entity_field_mapping:
            raise ValueError("Model does not have the EntityForeignKey field provided")
        entity_field_name = entity_field_name or entity_field_mapping.keys()[0]
        entity_field = entity_field_mapping[entity_field_name]
        
        refs = [entityfk.entity_ref(entity) for entity in entities]
        refs = sorted(refs, key=operator.itemgetter(0))
        qfilter = Q()
        for k, g in itertools.groupby(refs, operator.itemgetter(0)):
            qfilter |= Q(**{entity_field.entity_field:k, entity_field.fk_field+"__in":list(g)})
        return self.filter(qfilter)    
    
    def get_query_set(self):
        return EntityFKQuerySet(self.model)


def _get_entity_field_mapping(model):
    """
    Create a mapping of dict EntityForeignKey object fields
    present in django class
    """
    entity_field_mapping = {}
    for key, value in model.__dict__.items():
        if not key.startswith("__") and isinstance(value, EntityForeignKey):    
            entity_field_mapping[key] = value
    return entity_field_mapping

class EntityFKQuerySet(QuerySet):
    
    def _filter_or_exclude(self, negate, *args, **kwargs):
        """
        Shortcut allowing us to filter using entity_object
        filter param instead of having to define entity 
        and entity_id for every filter/exclude
        """
        entity_field_mapping = _get_entity_field_mapping(self.model)

        # Reiterate back through the mapping
        for key, value in entity_field_mapping.items():
            
            # Check the entity_field, if an a django Class object is passed
            # in and not a string... convert to a string
            if value.entity_field in kwargs.keys():
                if not isinstance(kwargs[value.entity_field], basestring):
                    kwargs[value.entity_field] = entity_label(kwargs[value.entity_field])
            
            # Check if entity_object passed in, if so populate the entity_field
            # and fk_field params
            if key in kwargs.keys():
                entity_obj = kwargs[key]
                entity_label_, entity_id = entity_ref(entity_obj)
                kwargs[value.entity_field] = entity_label_
                kwargs[value.fk_field] = entity_id
                del kwargs[key]
        
        return super(EntityFKQuerySet, self)._filter_or_exclude(False, *args, **kwargs)
        
