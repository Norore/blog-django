from django.contrib import admin
from Blog.models import *

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'site', 'avatar')

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['categorie', 'author', 'creation_date', 'edit_date', 'published']
    list_display = ('title', 'categorie', 'author', 'creation_date', 'edit_date', 'published')

class PageAdmin(admin.ModelAdmin):
    list_filter = ['author', 'creation_date', 'edit_date', 'published']
    list_display = ('title', 'author', 'creation_date', 'edit_date', 'published')

class CommentAdmin(admin.ModelAdmin):
    list_filter = ['pseudo', 'email', 'site', 'creation_date', 'published']
    list_display = ('article', 'pseudo', 'email', 'site', 'creation_date', 'published')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Tags)
admin.site.register(Link)
