Tracing
=====

Tracing is a Django app to trace changes in models.

This is a fork for django-tracing. Original package in: https://github.com/dbsiavichay/django-tracing

Quick start
-----------

1. Add "tracing" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'tracing',
    ]

3. Run ``python manage.py migrate`` to create the tracing migrations.

4. Import the BaseModel class and add it to your models 

Example
-----------

```python
from tracing.models import BaseModel

class ExampleModel(BaseModel):
    pass
```

5. For detail audit, create Audit Rules for your models