from  django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage,name='frontpage'),
    path('home/',views.home,name='event_home'),
    path('event_type/<str:event_type>/',views.eventype,name='app_event_type'),
    path('about/',views.About,name='about'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)