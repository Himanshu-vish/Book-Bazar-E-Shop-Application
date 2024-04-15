# helper file for model

from django.db import models
import uuid

class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True   # Django model na samajh ke as a class treate kare