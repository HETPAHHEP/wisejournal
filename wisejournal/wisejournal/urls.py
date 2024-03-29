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
from django.conf import settings
from django.conf.urls import handler404, handler500  # noqa
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# собственные страницы ошибок
handler404 = 'posts.views.page_not_found' # noqa
handler500 = 'posts.views.server_error'  # noqa

urlpatterns = [
    # админка
    path('admin/', admin.site.urls),

    # debug
    path('__debug__/', include('debug_toolbar.urls')),

    # главная страница с постами
    path("", include("posts.urls")),

    # собственные flatpages
    path('about/', include('about.urls')),

    # регистрация и авторизация
    path("auth/", include("users.urls")),

    # если не нашлось нужного шаблона для /auth в файле users.urls --
    # ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
