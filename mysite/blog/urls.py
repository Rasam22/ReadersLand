from django.conf.urls import url
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.registration, name='registration'),
    url(r'registration/$', views.registration, name='registration'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    # url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.activate, name='activate'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),name="reset_password"),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(),name="password_change"),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(),name="password_change_done"),
    url(r'getsimilar/$', views.getsimilar, name='getsimilar'),
    url(r'home/$',views.home,name='home'),
    url(r'getBooks/$',views.getBooks,name='getBooks'),
    url(r'getInfo/$', views.getInfo, name='getInfo'),
    url(r'getNames/$', views.getNames, name='getNames'),
    url(r'getTitles/$',views.getTitles,name='getTitles'),
    url(r'getDetails/$',views.getDetails,name='getDetails'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)