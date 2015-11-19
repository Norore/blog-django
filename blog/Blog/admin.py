from django.contrib import admin
from Blog.models import Author, Page, Categorie, Article, Comment

# Register your models here.
admin.site.register(Author)
admin.site.register(Categorie)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Page)
