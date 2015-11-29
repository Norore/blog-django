from django import get_version
from django.shortcuts import render
from models import *

# Create your views here.
def base():
    links = Link.objects.all()
    cats = Categorie.objects.all().order_by('name')
    pages = Page.objects.all().order_by('title')
    archives = Article.objects.all().filter(published=True)

    context = { 'version': get_version(),
                'links': links,
                'cats': cats,
                'pages': pages,
                'archives': archives,
              }
    return context

def index(request):
    context = base()
    articles = Article.objects.filter(published=True).order_by('-creation_date')[:10]
    comments = Comment.objects.filter(published=True, article__published=True).order_by('-article__creation_date')[:10].values()
    context['articles'] = articles
    context['comments'] = comments
    return render(request, "home.html", context)

def show_page(request, page):
    page = Page.objects.get(id=page)

    context = base()
    context['page'] = page

    return render(request, "show_page.html", context)

def show_categorie(request, cat):
    categorie = Categorie.objects.get(id=cat)
    articles = Article.objects.filter(categorie=cat, published=True).order_by('-creation_date')

    context = base()
    context['categorie'] = categorie
    context['articles'] = articles

    return render(request, "show_categorie.html", context)

def show_article(request, art):
    article = Article.objects.get(id=art)
    comments = Comment.objects.filter(article__id=art)

    context = base()
    context['article'] = article
    context['comments'] = comments

    return render(request, "show_article.html", context)
