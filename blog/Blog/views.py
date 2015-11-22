from django.shortcuts import render
from models import *

# Create your views here.
def index(request):
    links = Link.objects.all()
    cats = Categorie.objects.all().order_by('id')
    articles = Article.objects.filter(published=True).order_by('-creation_date')[:10]
    pages = Page.objects.all().order_by('title')
    context = {'links': links,
               'cats': cats,
               'articles': articles,
               'pages': pages}
    return render(request, "home.html", context)
