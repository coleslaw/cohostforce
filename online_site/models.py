from django.db import models
from elasticsearch_dsl import Document, Text, InnerDoc, Integer, Object
from elasticsearch_dsl.connections import connections

# Create your models here.

class Profile(models.Model):
    name = models.CharField(verbose_name="name", max_length=255)
    rating = models.IntegerField("rating")
    max_rating = models.IntegerField("max_rating")
    title = models.CharField(verbose_name="title", max_length=255)
    best_title = models.CharField(verbose_name="best_title", max_length=255)

    def __str__(self):
        return self.name
    
class ContestResult(models.Model):
    name = models.CharField(verbose_name="contest_name", max_length=255)
    rating_change = models.IntegerField(verbose_name="rating_change")
    new_rating = models.IntegerField(verbose_name="new_rating")
    title_change = models.CharField(verbose_name="title_change", max_length=255)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contests")

    def __str__(self):
        return self.name