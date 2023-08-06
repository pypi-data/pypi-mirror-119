# Django-DB-Helper

> Package contain necessary tools to complement your Django ORM usage.


## Install

```
$  pip install django-db-helper
```


## Usage

### Get Object or None
> Model.objects.get() is widely use in getting a single record from the database. A DoesNotExist exception is thrown when the record is not found. get_object_or_none returns None when no matching record is found. This method is very helpful because most developers do not handle DoesNotExist exception from Model.objects.get() since it is used in anticipation that a single matching record is available.


```python
from django_db_helper.get_object_or_none import get_object_or_none

#### Format
get_object_or_none(Model,key1=value1,key2=value2,..)

#### Getting User Object from User Model with an available username

user = get_object_or_none(User,username="andrewsxx")

//=> user object


#### Getting User Object from User Model with an available username

user = get_object_or_none(User,username="andrewsxx1234")

//=> None

```

## License

MIT © [Andrews Agyemang Opoku]
