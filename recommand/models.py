from django.db import models
from django_mysql.models import ListCharField


# Create your models here.

class Repositories(models.Model):
    class Meta:
        db_table = "repositories"
    keyword = models.CharField(max_length=30, null=False, blank=False)
    repo_id = models.IntegerField(unique=True)
    repo_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    created = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    stars = models.IntegerField()
    forks = models.IntegerField()
    subscribers = models.IntegerField()
    topics = ListCharField(
        base_field = models.CharField(max_length=255),
        max_length = (6*11)
    )


