from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from django.db import models


class EntityForeignKey(object):
    """
    Provides a generic relation to any django object 
    through entity_label/entity_id fields
    """

    def __init__(self, entity_field="entity", fk_field="entity_id"):
        self.entity_field = entity_field
        self.fk_field = fk_field

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name
        cls._meta.add_virtual_field(self)

        # For some reason I don't totally understand, using weakrefs here doesn't work.
        signals.pre_init.connect(self.instance_pre_init, sender=cls, weak=False)

        # Connect myself as the descriptor for this field
        setattr(cls, name, self)

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        """
        Handles initializing an object with the generic FK instaed of
        content-type/object-id fields.
        """
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            _entity_label = entity_label(value)
            kwargs[self.entity_field] = _entity_label
            kwargs[self.fk_field] = value._get_pk_val()

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            return getattr(instance, self.cache_attr)
        except AttributeError:
            rel_obj = None

            # Make sure to use ContentType.objects.get_for_id() to ensure that
            # lookups are cached (see ticket #5570). This takes more code than
            # the naive ``getattr(instance, self.ct_field)``, but has better
            # performance when dealing with GFKs in loops and such.
            f = self.model._meta.get_field(self.entity_field)
            entity = getattr(instance, f.get_attname(), None)
            #if ct_id:
                
            if entity:
                entity_id = getattr(instance, self.fk_field)
                try:
                    rel_obj = entity_instance(entity, entity_id)
                except ObjectDoesNotExist:
                    pass
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError(u"%s must be accessed via instance" % self.related.opts.object_name)

        entity = None
        fk = None
        if value is not None:
            entity = entity_label(value)
            #ct = self.get_content_type(obj=value)
            fk = value._get_pk_val()

        setattr(instance, self.entity_field, entity)
        setattr(instance, self.fk_field, fk)
        setattr(instance, self.cache_attr, value)


def entity_label(obj):
    """
    Returns label representing a django model instance.
    
    @param obj: Django model instance or model class
    @return: String
    """ 
    
    label = "%s.%s" % (obj._meta.app_label, obj._meta.object_name)
    return label.lower()


model_mapping = None

def entity_model(label):
    """
    Returns the django model class given an entity label
    
    @param label: Example "rdl.receipt"
    @return: Django class
    """
    global model_mapping
    if not model_mapping:
        model_mapping = {}
        for model in models.get_models():
            model_label = "%s.%s" % (model._meta.app_label, model._meta.object_name)
            model_mapping[model_label.lower()] = model
        
    if label not in model_mapping:
        raise Exception("Model %s could not be found and is not a registered django model" % label)
    
    return model_mapping[label]
    
    
def entity_instance(entity_label, entity_id):
    """
    Returns a django model instance provided entity_label and 
    entity_id
    
    @param entity_label: Example: "rdl.receipt"
    @param entity_id: Primary key for object
    @return: Django model instance  
    """
    
    ModelClass = entity_model(entity_label)
    obj = ModelClass.objects.get(pk=entity_id)
    return obj
    
    