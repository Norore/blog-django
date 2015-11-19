from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from datetime import datetime
import os

# Create your models here.
class Author(models.Model):
    author = models.OneToOneField(User)
    site = models.URLField(max_length=200)
    avatar = models.ImageField(upload_to="authors/", default="authors/anonymous.png")
    def __unicode__(self):
        return self.author.username

class Categorie(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    categorie = models.ForeignKey(Categorie)
    content = models.TextField()
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField(blank=True, null=True)
    tags = models.SlugField()
    def __unicode__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    content = models.TextField()
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article)
    pseudo = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    site = models.URLField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    creation_date = models.DateTimeField()
    def __unicode__(self):
        df = DateFormat(self.creation_date)
        return self.pseudo+" le "+df.format('Y/m/d')+" a "+df.format('H:m:s')
