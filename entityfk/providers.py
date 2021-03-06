# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import Model

from entityfk.entityfk import CannotUnserialize, TypeNotSupported


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
        for model in apps.get_models():
            model_label = "{}.{}".format(
                model._meta.app_label,
                model._meta.object_name
            )
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
            pk = "pk"
            try:
                pk = ModelClass.EntityFKMeta.pk
            except AttributeError:
                pass
            obj = ModelClass.objects.get(**{pk: entity_id})
        except ObjectDoesNotExist:
            raise CannotUnserialize()
        return obj

    def to_ref(self, obj):
        if (
            not isinstance(obj, Model)
            and not (inspect.isclass(obj) and issubclass(obj, Model))
        ):
            raise TypeNotSupported()
        label = "{}.{}".format(
            obj._meta.app_label,
            obj._meta.object_name
        )
        entity_label = label.lower()
        pk_getter = lambda obj: obj._get_pk_val()  # noqa: E731
        try:
            pk = obj.EntityFKMeta.pk
            pk_getter = lambda obj: getattr(obj, pk)  # noqa: E731
        except AttributeError:
            pass
        entity_id = pk_getter(obj) if isinstance(obj, Model) else None
        return (entity_label, entity_id)


providers = []


def register_provider(provider):
    global providers
    providers.append(provider)


def get_providers():
    """Retrieve entityfk providers"""
    global providers
    return providers
