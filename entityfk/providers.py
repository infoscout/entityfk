from django.db import models
from django.db.models.base import Model

class TypeNotSupported(Exception):
    pass

class BaseProvider(object):
    def to_model(self, label):
        """
        Returns the model class given an entity label
        
        @param desc: Example "rdl.receipt"
        @return: model class
        """
        raise NotImplementedError()
    
    def to_object(self, desc):
        """
        Returns the model object given an entity descriptor
        
        @param desc: Example ("rdl.receipt", "123124")
        @return: model instance
        """
        raise NotImplementedError()
    
    def to_ref(self, obj_or_class):
        """
        Returns the entity descriptor for an object/class
        
        If obj_or_class is a class the entity_id is None 
        
        @param obj: Object e.g.: A Django model instance
        @return: entity descriptor (tuple of entity_label, and entity_id)
        """
        raise NotImplementedError()

class DjangoModelProvider(BaseProvider):
    
    def __init__(self):
        model_mapping = {}
        for model in models.get_models():
            model_label = "%s.%s" % (model._meta.app_label, model._meta.object_name)
            model_mapping[model_label.lower()] = model
        self.model_mapping = model_mapping

    def to_model(self, label):
        if label not in self.model_mapping:
            raise TypeNotSupported()
        return self.model_mapping[label]

    def to_object(self, desc):
        entity_label, entity_id = desc
        ModelClass = self.to_model(entity_label)
        obj = ModelClass.objects.get(pk=entity_id)
        return obj
    
    def to_ref(self, obj):
        if not isinstance(obj, Model) and not issubclass(obj, Model):
            raise TypeNotSupported()
        label = "%s.%s" % (obj._meta.app_label, obj._meta.object_name)
        entity_label = label.lower()
        entity_id = isinstance(obj, Model) and obj._get_pk_val()
        return (entity_label, entity_id)

providers = [DjangoModelProvider()]

def get_providers():
    """Retrieve entityfk providers"""
    global providers
    return providers