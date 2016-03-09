from django import forms
from models import *
from django.contrib.auth import update_session_auth_hash

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('published', 'creation_date', 'article')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('creation_date', 'edit_date',)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ()

class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        exclude = ()
