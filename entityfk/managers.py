from django.db.models import Manager
from django.db.models.query import QuerySet
from entityfk import EntityForeignKey, entity_label
from entityfk.entityfk import entity_ref

class EntityFKManager(Manager):
    """
    A manager that returns a GFKQuerySet instead of a regular QuerySet.

    """
    def get_query_set(self):
        return EntityFKQuerySet(self.model)


class EntityFKQuerySet(QuerySet):
    
    def _filter_or_exclude(self, negate, *args, **kwargs):
        """
        Shortcut allowing us to filter using entity_object
        filter param instead of having to define entity 
        and entity_id for every filter/exclude
        """
        
        # Create a mapping of dict EntityForeignKey object fields
        # present in django class
        entity_field_mapping = {}
        for key, value in self.model.__dict__.items():
            if not key.startswith("__") and isinstance(value, EntityForeignKey):    
                entity_field_mapping[key] = value 

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
        
