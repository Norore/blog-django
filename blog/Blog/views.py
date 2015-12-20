from django import get_version
from django.shortcuts import render, HttpResponseRedirect
from models import *
from django.db.models import Count
from forms import *
from datetime import datetime

# Create your views here.
def base():
    links = Link.objects.all()
    cats = Categorie.objects.filter(article__published=True).annotate(nb_articles=Count('article__id')).order_by('name')
    pages = Page.objects.filter(published=True).order_by('title')
    archives = Article.objects.filter(published=True)
    nb_comments = Comment.objects.filter(published=False)

    context = { 'version': get_version(),
                'links': links,
                'cats': cats,
                'pages': pages,
                'archives': archives,
                'nb_comments': nb_comments,
              }
    return context

def index(request):
    context = base()

    articles = Article.objects.filter(published=True).annotate(nb_comments=Count('comment__id')).order_by('-creation_date')[:10]
    comments = Comment.objects.filter(published=True, article__published=True).order_by('-article__creation_date')[:10].values()
    
    context['articles'] = articles
    context['comments'] = comments
    
    return render(request, "home.html", context)

def show_page(request, page):
    try:
        page = Page.objects.get(id=page)
    except:
        page = {}

    context = base()
    context['page'] = page

    return render(request, "show_page.html", context)

def show_categorie(request, cat):
    try:
        categorie = Categorie.objects.get(id=cat)
        articles = Article.objects.filter(categorie=cat, published=True).order_by('-creation_date')
    except:
        categorie = {}
        articles = {}

    context = base()
    context['categorie'] = categorie
    context['articles'] = articles

    return render(request, "show_categorie.html", context)

def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
    else:
        form = CategoryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = Categorie(name = name, description = description)
            category.save()
            return HttpResponseRedirect('/list_categories/')
        else:
            context = base()
            context['form'] = form
            return render(request, "add_category.html", context)

    context = base()
    context['form'] = form

    return render(request, "add_category.html", context)

def list_categories(request):
    try:
        categories = Categorie.objects.all().order_by('name')
    except:
        categories = {}

    context = base()
    context['categories'] = categories

    return render(request, "list_categories.html", context)

def show_article(request, art):
    try:
        article = Article.objects.get(id=art)
        comments = Comment.objects.filter(article__id=art, published=True)
    except:
        article = {}
        comments = {}

    context = base()
    context['article'] = article
    context['comments'] = comments

    """
    Form part for new comment submission
    """

    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)

        if form.is_valid():
            pseudo = form.cleaned_data['pseudo']
            site = form.cleaned_data['site']
            content = form.cleaned_data['commentaire']
            comment = Comment( article_id = art, \
                               pseudo = pseudo, \
                               site = site, \
                               comment = content, \
                               creation_date = datetime.now() \
                               )
            comment.save()
            return HttpResponseRedirect("/a/"+art)

    context['form'] = form

    return render(request, "show_article.html", context)
