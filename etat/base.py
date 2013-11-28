from django.db import models

class BaseModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    legacy_id = models.PositiveIntegerField(blank=True, null=True,
        editable=False, unique=True)

    class Meta:
        abstract = True
