# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import signals
from django.db.models.fields.related import RelatedField


class TypeNotSupported(Exception):

    """The provided instance or label is not supported by this provider"""
    pass


class CannotUnserialize(Exception):

    """The provider could not find the instance based on the reference"""
    pass


class EntityForeignKey(RelatedField):

    """
    Provides a generic relation to any django object
    through entity_label/entity_id fields
    """

    column = None

    # Field flags
    many_to_many = False
    many_to_one = True
    one_to_many = False
    one_to_one = False
    concrete = False

    def __init__(self, entity_field="entity", fk_field="entity_id", **kwargs):
        self.entity_field = entity_field
        self.fk_field = fk_field
        super(EntityForeignKey, self).__init__(**kwargs)

    def contribute_to_class(self, cls, name):
        self.name = self.attname = name
        self.model = cls
        self.cache_attr = "_%s_cache" % name
        try:
            cls._meta.private_fields.append(self)
        except AttributeError:  # Django < 1.10
            cls._meta.virtual_fields.append(self)

        # For some reason I don't totally understand,
        # using weakrefs here doesn't work.
        signals.pre_init.connect(
            self.instance_pre_init,
            sender=cls,
            weak=False
        )
        # Connect myself as the descriptor for this field
        setattr(cls, name, self)

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        """
        Handles initializing an object with the generic FK instaed of
        content-type/object-id fields.
        """
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            entity_label, entity_id = entity_ref(value)
            kwargs[self.entity_field] = entity_label
            kwargs[self.fk_field] = entity_id

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

            if entity:
                entity_id = getattr(instance, self.fk_field)
                try:
                    rel_obj = entity_instance(entity, entity_id)
                # silently fail: contenttype fw does the same, not sure if smart
                except CannotUnserialize:
                    # TODO: add logging
                    pass
            setattr(instance, self.cache_attr, rel_obj)
            return rel_obj

    def __set__(self, instance, value):
        entity = None
        fk = None
        if value is not None:
            entity, fk = entity_ref(value)

        setattr(instance, self.entity_field, entity)
        setattr(instance, self.fk_field, fk)
        setattr(instance, self.cache_attr, value)


def entity_label(obj):
    """
    Returns label representing a django model instance.

    @param obj: model instance or model class
    @return: String
    """
    return entity_ref(obj, incomplete=True)[0]


def entity_ref(obj, incomplete=False):
    """
    Get the (label, id) reference pair for the object

    @param obj: The obj to be serialized
    @param incomplete: Internal parameter
    @return: Tuple of (entity_label, entity_id)
    """
    from entityfk.providers import get_providers
    for provider in get_providers():
        try:
            result = provider.to_ref(obj)
            if result[1] is None and not incomplete:
                # You either provided a class or the provider implementation
                # is broken. It should throw an exception if the key field
                # used for the entity_id is not available.
                raise ValueError("entity_id is not available for obj")
            return result
        except TypeNotSupported:
            pass
    raise ValueError("Cannot serialize object")


def entity_model(label):
    """
    Returns a model class provided entity_label
    @param entity_label: Example: "rdl.receipt"
    @return: Model class
    """
    from entityfk.providers import get_providers
    for provider in get_providers():
        try:
            return provider.to_model(label)
        except TypeNotSupported:
            pass
    raise Exception(
        (
            "Model {} could not be found"
            "and is not a registered model"
        ).format(label)
    )


def entity_instance(entity_label, entity_id):
    """
    Returns a model instance provided entity_label and
    entity_id

    @param entity_label: Example: "rdl.receipt"
    @param entity_id: Primary key for object
    @return: Model instance
    """
    from entityfk.providers import get_providers
    desc = (entity_label, entity_id)
    for provider in get_providers():
        try:
            return provider.to_object(desc)
        except TypeNotSupported:
            pass
    raise Exception(
        (
            "Model {} could not be found and"
            "is not a registered model"
        ).format(entity_label)
    )
