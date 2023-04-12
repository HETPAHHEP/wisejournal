"""wisejournal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [
    # админка
    path('admin/', admin.site.urls),

    # debug
    path('__debug__/', include('debug_toolbar.urls')),

    # главная страница с постами
    path("", include("posts.urls")),

    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),

    # регистрация и авторизация
    path("auth/", include("users.urls")),

    # если не нашлось нужного шаблона для /auth в файле users.urls --
    # ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),
]

# flatpages
urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about-spec'),
]
