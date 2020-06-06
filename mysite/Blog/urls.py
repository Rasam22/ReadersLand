from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('basepage/',views.basepage,name='basepage'),
    path('booklist/',views.booklist,name='booklist'),
    path('about/', views.about,name='Blog-about'),
    path('search/',views.search, name='search'),
    path('book/<int:id>', views.bookdetail, name='bookdetail'),
    path('writerlist/',views.writerlist,name='writerlist'),
    path('writer/<int:id>', views.writerdetail, name='writerdetail'),
    path('book/<int:id>/comment/', views.comments, name='comments'),
    path('Genres/<int:id>', views.Genres, name='Genres'),
    path('contact/',views.contact,name='contact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
