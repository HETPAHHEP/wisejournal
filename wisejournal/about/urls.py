from django.urls import path

from . import views

urlpatterns = [
    path('about-author/', views.AboutAuthorView.as_view(), name='about-author'),
    path('about-spec/', views.AboutSpecView.as_view(), name='about-spec')
]
