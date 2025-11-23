from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,verbose_name=_("email"))

    def __str__(self):
        return f"{self.username}" if self.get_full_name() is None else self.get_full_name() 