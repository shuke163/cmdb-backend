from django.db import models


# Create your models here.


class common(models.Model):
    """
    common model
    """
    create_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CMDB(common):
    """
    """
    id = models.AutoField(primary_key=True)
    data = models.JSONField(blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "cmdb"
        db_table = "cmdb"

    def __str__(self):
        return self.data
