from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import SnippetSitemap, StaticViewSitemap


sitemaps = {'static': StaticViewSitemap, 'snippet': SnippetSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    path('account/', include('account.urls')),
    path('account/', include('django.contrib.auth.urls')),
]
