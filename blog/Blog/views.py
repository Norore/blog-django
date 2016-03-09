from django import get_version
from django.shortcuts import render, HttpResponseRedirect
from models import *
from django.db.models import Count
from forms import *
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def base():
    links = Link.objects.all()
    cats = Category.objects.filter(article__published=True).annotate(nb_articles=Count('article__id')).order_by('name')
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
    comments = Comment.objects.filter(published=True, article__published=True).order_by('-article__creation_date')[:10]
    
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

def list_pages(request):
    try:
        pages = Page.objects.all().order_by('title')
    except:
        pages = {}

    context = base()
    context['pages'] = pages

    return render(request, "list_pages.html", context)

def add_page(request):
    if request.method == 'GET':
        form = PageForm(initial={'author': request.user})
    else:
        form = PageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            content = form.cleaned_data['content']
            published = form.cleaned_data['published']
            page = Page(title = title, \
                        author = author, \
                        content = content, \
                        published = published )
            page.save()
            return HttpResponseRedirect('/list_pages/')

    context = base()
    context['form'] = form

    return render(request, "add_page.html", context)

def edit_page(request, page):
    page = Page.objects.get(id=page)
    if request.method == 'GET':
        form = PageForm({'title': page.title, \
                         'author': page.author, \
                         'content': page.content, \
                         'published': page.published} )
    else:
        form = PageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            content = form.cleaned_data['content']
            published = form.cleaned_data['published']
            # update page
            page.title = title
            page.author = author
            page.content = content
            page.published = published
            page.edit_date = now()
            page.save()
            return HttpResponseRedirect('/list_pages/')

    context = base()
    context['form'] = form
    context['inpage'] = page

    return render(request, "edit_page.html", context)

def show_category(request, cat):
    try:
        category = Category.objects.get(id=cat)
        articles = Article.objects.filter(categorie=cat, published=True).order_by('-creation_date')
    except:
        categorie = {}
        articles = {}

    context = base()
    context['category'] = category
    context['articles'] = articles

    return render(request, "show_category.html", context)

def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
    else:
        form = CategoryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            # create category
            category = Category(name = name, description = description)
            category.save()
            return HttpResponseRedirect('/list_categories/')

    context = base()
    context['form'] = form

    return render(request, "add_category.html", context)

def edit_category(request, cat):
    category = Category.objects.get(id=cat)
    if request.method == 'GET':
        form = CategoryForm({'name': category.name, \
                             'description': category.description})
    else:
        form = CategoryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            # update category
            category.name = name
            category.description = description
            category.save()
            return HttpResponseRedirect('/list_categories/')
    
    context = base()
    context['category'] = category
    context['form'] = form
    return render(request, "edit_category.html", context)

def list_categories(request):
    try:
        categories = Category.objects.all().order_by('name')
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
                               creation_date = now() \
                               )
            comment.save()
            return HttpResponseRedirect("/a/"+art)

    context['form'] = form

    return render(request, "show_article.html", context)
    
def add_article(request):
    if request.method == 'GET':
        form = ArticleForm(initial={'author': request.user,'creation_date': now})
    else:
        form = ArticleForm(request.POST)
        
        if form.is_valid():
            author = form.cleaned_data['author']
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            published = form.cleaned_data['published']
            tags = form.cleaned_data['tags']
            article = Article( author = author, \
                               category = category, \
                               title = title, \
                               content = content, \
                               published = published, \
                               creation_date = now())
            article.save()
            for tag in tags:
                article.tags.add(tag)
            return HttpResponseRedirect('/')
            
    context = base()
    context['form'] = form
    
    return render(request, "add_article.html", context)

def show_tag(request, tag):
    articles = Article.objects.filter(tags__slug=tag)
    tag = Tags.objects.get(slug=tag)

    context = base()
    context['articles'] = articles
    context['tag'] = tag

    return render(request, "tag.html", context)

def add_tag(request):
    if request.method == 'GET':
        form = TagForm()
    else:
        form = TagForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            slug = form.cleaned_data['slug']
            tag = Tags( title = title, slug = slug )
            tag.save()
            return HttpResponseRedirect('/list_tags/')

    context = base()
    context['form'] = form

    return render(request, "add_tag.html", context)

def edit_tag(request, tag):
    tag = Tags.objects.get(id=tag)
    if request.method == 'GET':
        form = TagForm({'title': tag.title, 'slug': tag.slug})
    else:
        form = TagForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            slug = form.cleaned_data['slug']
            tag.title = title
            tag.slug = slug
            tag.save()
            return HttpResponseRedirect('/list_tags/')

    context = base()
    context['form'] = form
    context['tag'] = tag

    return render(request, "edit_tag.html", context)

def list_tags(request):
    try:
        tags = Tags.objects.all().order_by('title')
    except:
        tags = {}

    context = base()
    context['tags'] = tags

    return render(request, "list_tags.html", context)


