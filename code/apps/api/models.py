from django.db import models
import secrets
import hashlib
from apps.accounts.models import CustomUser

class ApiModel(models.Model):
    api_name = models.CharField(verbose_name="نام رابط",max_length=110)
    key = models.CharField(
        verbose_name="توکن",
        max_length=128,
        unique=True,
        editable=False
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="تاریخ ایجاد",auto_now_add=True)
    revoked_date = models.DateTimeField(verbose_name="تاریخ بازیابی",blank=True,null=True)
    
    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode()).hexdigest()

    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...,*args,**kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(64)
            self.hash_token(raw_token=self.key)
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(64)