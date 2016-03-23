from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'stories.views.index', name='index'),
    url(r'^like/$', 'stories.views.like', name='like'),
]