"""
URL configuration for santapedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from articles import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), 
    path('', views.redirect_to_home),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('articles/', include("articles.urls")),
    path('saints/', views.saints, name='saints'),
    path('prayers/', views.prayers, name='prayers'),
    path('santapedia/', views.santapedia, name='santapedia'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('aleatory/', views.aleatory, name='aleatory'),
    path('patronized_cities/', views.patronized_cities, name='patronized_cities'),
    path("ajax/get-cities/", views.get_cities_by_state, name="get_cities_by_state"),
    path("ajax/get-states/", views.get_states_by_country, name="get_states_by_country"),
    path("calendar/", views.calendar, name="calendar"),
    path("ajax/calendar-data/", views.calendar_data, name="calendar_data"),
    path("ajax/saints-by-month/", views.saints_by_month, name="saints_by_month"),
    path('', lambda request: redirect('/home')),
)

if settings.DEBUG:  # só no desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)