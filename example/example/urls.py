from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', 'example.views.example_view', name='example'),
]

urlpatterns += staticfiles_urlpatterns()
