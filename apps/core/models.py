from django.db import models


class BaseCategory(models.Model):
    """Model definition for Category."""
    name = models.CharField("نام برچسب",max_length=110)
    description = models.TextField("توضیح برچسب",blank=True,null=True)
    

    class Meta:
        """Meta definition for Category."""

        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"
        abstract = True


    def __str__(self):
        """Unicode representation of Category."""
        return f"{self.name}"


class BaseComment(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, verbose_name="کاربر")
    content = models.TextField(blank=True,null=True,verbose_name="محتوا")

    class Meta:
        """Meta definition for Comment."""

        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        abstract = True

    def __str__(self):
        """Unicode representation of Comment."""
        return f"نظر شماره {self.id}"

class LinkModel(models.Model):
    name = models.CharField(verbose_name="نام",max_length=110)
    def __str__(self):
        return self.name
class BaseLink(models.Model):
    """Model definition for BaseLink."""
    link_type = models.ForeignKey(LinkModel,on_delete=models.CASCADE)
    link_name = models.CharField(verbose_name="نام لینک",)
    link_url = models.URLField(verbose_name="مکان لینک")
    class Meta:
        """Meta definition for BaseLink."""

        verbose_name = 'BaseLink'
        verbose_name_plural = 'BaseLinks'
        abstract = True

    def __str__(self):
        """Unicode representation of BaseLink."""
        return f"{self.link_name}"
