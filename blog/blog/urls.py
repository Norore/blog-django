"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Pages
    url(r'p/(?P<page>[0-9]+)/$', views.show_page),
    url(r'list_pages/$', views.list_pages),
    url(r'add_page/$', views.add_page),
    url(r'edit_page/(?P<page>[0-9]+)/$', views.edit_page),
    # Categories
    url(r'c/(?P<cat>[0-9]+)/$', views.show_category),
    url(r'list_categories/$', views.list_categories),
    url(r'add_category/$', views.add_category),
    url(r'edit_category/(?P<cat>[0-9]+)/$', views.edit_category),
    # Articles
    url(r'a/(?P<art>[0-9]+)/$', views.show_article),
    url(r'add_article/$', views.add_article),
    # Tags
    url(r'tag/(?P<tag>[a-z]+)/$', views.show_tag),
    url(r'list_tags/$', views.list_tags),
    url(r'add_tag/$', views.add_tag),
    url(r'edit_tag/(?P<tag>[0-9]+)/$', views.edit_tag),
    # Administration
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
