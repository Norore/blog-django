from django import forms

class CommentForm(forms.Form):
    pseudo = forms.CharField(max_length=20)
    email = forms.EmailField()
    site = forms.URLField()
    commentaire = forms.CharField(widget=forms.Textarea)

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=60)
    description = forms.CharField(widget=forms.Textarea)

class PageForm(forms.Form):
    title = forme.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    published = forms.BooleanField(default=False)
    creation_date = forms.DateField()
