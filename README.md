# EntityFK Django App

[![CircleCI](https://circleci.com/gh/infoscout/entityfk.svg?style=svg)](https://circleci.com/gh/infoscout/entityfk)

EntityFK (Entity Forieign Key) is a django app that allows you to easily add a generic foreign key to any (not just django, see section 'Providers') model.

The app is a lightweight & modified version of the [ContentType](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/) framework built into django. The primary difference is entityfk stores a string label to associate the model, while the ContentType framework saves a content_type_id. This key change allows you to easily use entityfk for django projects across multi-dbs.

## Implementation

Add a entity foreign key to a django model:

    # models.py
    from entityfk import entityfk
    from entityfk.managers import EntityFKManager

    class AuthorTag(models.Model):
        tag_name = models.CharField(max_length=32)

        entity_object = entityfk.EntityForeignKey()
        entity = models.CharField(max_length=32, null=False)
        entity_id = models.PositiveIntegerField(null=False)

      objects = EntityFKManager()

Save a entity object:

    book = Book.objects.get(pk=1)

    author_tag = AuthorTag.objects.create(tag_name="first_book", entity_object=book)

See how the entity is stored:

    >>> author_tag.entity
    'app_label.book'
    >>> author_tag.entity_id
    1

Query a table for an entity object. To do so, need to add `EntityFKManager` as managers object:

    >>> tags = AuthorTag.objects.filter(entity_object=book)
    ['book']

If you want to query a table for all records with an entity class, you can simply pass in the Class:

    >>> tags = AuthorTag.objects.filter(entity=Book)

Other useful methods, return a label provided an model instance or class

    >>> from entityfk import entityfk
    >>> label = entity_label(book)
    'app_label.book'

With a label, return the django model class

    >>> entityfk.entity_model(label)
    <class 'app.models.Book'>

## Primary keys
By default, for Django models, the pk is used as the entity_id. If you want to override it, you should define a `EntityFKMeta` class inside the modelclass, specifying the field to be used.

    class MyModel(models.Model):
        mypk = models.CharField(...)
        class EntityFKMeta(object):
            pk = "mypk"

## Providers

The providers module enables extensibility beyond Django. By default the DjangoModelProvider is the only active provider, so by default, entityfk works as if it would be for just Django models.

### Implementation

Providers have to implement 3 methods that enable extensibility. You can subclass `BaseProvider` for this matter. First and foremost, if a provider is not recognizing an object or reference, you should throw `TypeNotSupported`, thus the framework would move on and search for another provider... If based on the reference, you cannot find an object, throw `CannotUnserialize`.

#### to_model
Given a label (e.g.:`"rdl.receipt"`) it returns the model class (e.g.: `Receipt`), or throws `TypeNotSupported` if it is unknown.

#### to_object
Given a reference-tuple (e.g.: `("rdl.receipt", 1)`) it returns the object referred to by the tuple.
Should throw `TypeNotSupported` if the label part of the tuple (`"rdl.receipt"`) is not known.
Should throw `CannotUnserialize` if the model class cannot be instantiated. (e.g.: looked up by the id)

#### to_ref
Given a model object or a model class, it returns a reference-tuple to it (e.g.: `("rdl.receipt", 1)`).
Should throw `TypeNotSupported` if the model cannot be handled by this provider.
Should word with both objects and the class of the model.

### Adding providers

    from entityfk import providers
    providers.providers = [MyProvider1(), MyProvider2()]

## Future enhancements

* Support for reverse lookups, similar to the integration in the [ContentType](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#reverse-generic-relations) framework
