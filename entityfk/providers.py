from django.db import models
from django.db.models.base import Model
import inspect
from django.core.exceptions import ObjectDoesNotExist

class TypeNotSupported(Exception):
    """The provided instance or label is not supported by this provider"""
    pass

class CannotUnserialize(Exception):
    """The provider could not find the instance based on the reference"""
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
        try:
            obj = ModelClass.objects.get(pk=entity_id)
        except ObjectDoesNotExist:
            raise CannotUnserialize()
        return obj
    
    def to_ref(self, obj):
        if not isinstance(obj, Model) and not (inspect.isclass(obj) and issubclass(obj, Model)):
            raise TypeNotSupported()
        label = "%s.%s" % (obj._meta.app_label, obj._meta.object_name)
        entity_label = label.lower()
        entity_id = isinstance(obj, Model) and obj._get_pk_val()
        return (entity_label, entity_id)

providers = None

def get_providers():
    """Retrieve entityfk providers"""
    global providers
    if providers is None:
        success = False
        try:
            from django.conf import settings
            loader = getattr(settings, "ENTITYFK_GET_PROVIDERS", None)
            if loader and inspect.isfunction(loader):
                providers = loader()
            success = True
        except Exception:
            pass
        if not success:
            providers = [DjangoModelProvider()]
    return providers