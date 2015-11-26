from django import get_version
from django.shortcuts import render
from models import *

# Create your views here.
def base():
    links = Link.objects.all()
    cats = Categorie.objects.all().order_by('name')
    pages = Page.objects.all().order_by('title')

    context = { 'version': get_version(),
                'links': links,
                'cats': cats,
                'pages': pages,
              }
    return context

def index(request):
    context = base()
    articles = Article.objects.filter(published=True).order_by('-creation_date')[:10]
    comments = Article.objects.order_by('comment__id').filter(published=True).filter(comment__published=True).order_by('-creation_date')[:10]
    context['articles'] = articles
    context['comments'] = comments
    return render(request, "home.html", context)

def show_page(request, page):
#    page = Page.objects.filter(id=page).first()
    page = Page.objects.get(id=page)

    context = base()
    context['page'] = page

    return render(request, "show_page.html", context)
