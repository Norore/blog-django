from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat
from django.utils.safestring import mark_safe
import markdown
from datetime import datetime
import os

# Create your models here.
class Author(models.Model):
    author = models.OneToOneField(User)
    site = models.URLField(max_length=200)
    description = models.TextField()
    avatar = models.ImageField(upload_to="authors/", default="authors/anonymous.png")
    def __unicode__(self):
        return self.author.username

class Categorie(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    def __unicode__(self):
        return self.name
    def desc_markdown(self):
        return mark_safe(markdown.markdown(self.description))

class Tags(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    categorie = models.ForeignKey(Categorie)
    content = models.TextField()
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags)
    def __unicode__(self):
        return self.title
    def content_markdown(self):
        return mark_safe(markdown.markdown(self.content))

class Page(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    content = models.TextField()
    published = models.BooleanField(default=False)
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return self.title
    def content_markdown(self):
        return mark_safe(markdown.markdown(self.content))

class Comment(models.Model):
    article = models.ForeignKey(Article)
    pseudo = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    site = models.URLField(max_length=200, blank=True, null=True)
    comment = models.TextField()
    creation_date = models.DateTimeField()
    published = models.BooleanField(default=False)
    def __unicode__(self):
        df = DateFormat(self.creation_date)
        return self.pseudo+" le "+df.format('Y/m/d')+" a "+df.format('H:m:s')
    def content_markdown(self):
        return mark_safe(markdown.markdown(self.comment))

class Link(models.Model):
    link = models.URLField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=140)
    published = models.BooleanField()

    def __unicode__(self):
        return self.name
