# EntityFK Django App

EntityFK (Entity Forieign Key) is a django app that allows you to easily add a generic foreign key to a django model. 

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
	
	
## Future enhancements

* Support for reverse lookups, similar to the integration in the [ContentType](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/#reverse-generic-relations) framework
	