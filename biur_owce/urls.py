"""biur_owce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rezerwacje import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^room/(?P<id_>(\d)+)$', views.room),
    url(r'^reserve/(?P<id_>(\d)+)$', views.reserve),
    url(r'^$', views.room_list),
    url(r'^add_room/$', views.add_room),
    url(r'^edit/(?P<id>(\d)+)/$', views.edit_room),
    url(r'^delete/(?P<id>(\d)+)/$', views.del_room),
    url(r'^search/', include('search.urls')),
]
