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
    url(r'^$', views.login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(
        r'^logout/',
        views.logout,
        name='logout',
    ),
    url(r'^main/search', views.search, name='search'),
    url(r'^main', views.main, name='main'),
    url(r'^book/borrow/(?P<borrow>.+)', views.borrow, name='borrow'),
    url(r'^book/return/(?P<return_book>.+)/', views.return_book_complete, name='return_book_complete'),
    url(r'^seminar$', views.seminar, name='seminar'),
    url(r'^seminar/(?P<slug>.+)$', views.reservation, name='reservation'),
    url(r'^staff$', views.staff, name='staff'),
    url(r'^return$', views.return_book, name='return'),
    url(r'^main_staff', views.main, name='main_staff'),
    url(r'^book_staff$', views.book_staff, name='book_staff'),
    url(r'^seminar_staff$', views.seminar_staff, name='seminar_staff'),
    url(r'^book_staff/(?P<book>.+)/accept', views.book_staff_accept, name='book_staff_accept'),
    url(r'^book_staff/(?P<book>.+)/decline', views.book_staff_decline, name='book_staff_decline'),
    url(r'^seminar_staff/(?P<client>.+)/(?P<seminar>.+)/accept', views.seminar_staff_accept, name='seminar_staff_accept'),
    url(r'^seminar_staff/(?P<client>.+)/(?P<seminar>.+)/decline', views.seminar_staff_decline, name='seminar_staff_decline'),
    url(r'^seminar_show/', views.seminar_show, name='seminar_show'),
    url(r'^seminar_confirm/(?P<client>.+)/(?P<seminar>.+)', views.seminar_confirm, name='seminar_confirm'),
    url(r'^request', views.request_book, name='request'),

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
