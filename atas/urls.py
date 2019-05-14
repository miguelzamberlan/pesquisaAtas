"""atas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from atas import settings
from django.views.static import serve
from django.conf.urls.static import static
from pesquisa.views import relatorio
from pesquisa.views import busca
#from pesquisa.views import upload_file

urlpatterns = [
    url(r'^$', busca, name='busca'),
    url(r'^relatorio/', relatorio, name='relatorio'),
    #url(r'^upload$', upload_file, name='upload_file'),
    path('admin/', admin.site.urls),
    #url(r'^static/(?P<path>/*)$', serve, {'document_root':settings.STATIC_ROOT}),
    url(r'^atas/static/(?P<path>/*)$', serve, {'document_root':settings.STATIC_ROOT}),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

