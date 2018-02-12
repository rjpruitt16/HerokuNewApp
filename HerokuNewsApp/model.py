from django.db import models
from django.contrib.postgres.fields import ArrayField

class ArticleScheme(models.Model):
    title = models.CharField(max_length=30)
    newsoutlet = models.CharField(max_length=10)
    url = models.CharField(max_length=30)
    date_joined = models.DateField()
    text = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=3)
    keywords = ArrayField(models.CharField(max_length=10), blank=True)
