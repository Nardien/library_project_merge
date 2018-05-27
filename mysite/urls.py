"""mysite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views  # 이 줄 추가.
from django.conf import settings
from library import views
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(
        r'^logout/',
        views.logout,
        name='logout',
    ),
    url(r'^main/search/', views.search, name='search'),
    url(r'^main/', views.main, name='main'),
    url(r'^book/borrow/(?P<borrow>.+)/$', views.borrow, name='borrow'),

]

"""url(
    r'^',
    auth_views.login,
    name='login',
    kwargs={
        'template_name': 'login.html'
    }
),"""
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]
