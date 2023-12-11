from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

# Create your models here.


class AbstractModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True, verbose_name=(_("Is Active")))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=(_("Created at")))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=(_("Updated at")))
