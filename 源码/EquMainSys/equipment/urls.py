from django.urls import path,include
from . import views,equ_views,other_views

urlpatterns = [
    # path('addtest/',views.addtest),
    path('stuman/', views.stuman),
    path('adminman/', views.adminman),
    path('adel/', views.adel),
    path('adch/', views.adch),
    path('adsearch/', views.adsearch),
    path('addadmin/', views.addadmin),

    path('stuch/', views.stuch),
    path('studel/', views.studel),
    path('addstu/', views.addstu),
    path('stusearch/', views.stusearch),

    path('equinfo/', equ_views.equinfo),
    path('equmansearch/', equ_views.equmansearch),
    path('equinfosearch/', equ_views.equinfosearch),
    path('equinfodel/', equ_views.equinfodel),
    path('equinfoch/', equ_views.equinfoch),
    path('addequinfo/', equ_views.addequinfo),

    path('equman/', equ_views.equman),
    # path('equmanote/', equ_views.equmanote),
    path('equmandel/', equ_views.equmandel),
    path('equmanbeizhu/', equ_views.equmanbeizhu),
    path('mansearch/', equ_views.mansearch),


    path('badequ/', equ_views.badequ),
    path('badequdel/', equ_views.badequdel),
    path('badsearch/', equ_views.badsearch),

    path('remindman/', other_views.remindman),
    path('remindch/', other_views.remindch),
    path('remindel/', other_views.remindel),
    path('addremind/', other_views.addremind),
    path('remindsearch/', other_views.remindsearch),


    path('recent/', other_views.recent),
    path('recentdel/', other_views.recentdel),
    path('recentsearch/', other_views.recentsearch),







]