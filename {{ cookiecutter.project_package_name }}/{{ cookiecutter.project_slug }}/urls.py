from django.urls import re_path

from {{ cookiecutter.project_slug }} import views


urlpatterns = [
    re_path(
        r'^(?P<slug>[A-Za-z0-9_\-]+)/$',
        views.{{ cookiecutter.project_class }}DetailView.as_view(),
        name='detail',
    ),
    re_path(
        r"^$",
        views.{{ cookiecutter.project_class }}ListView.as_view(),
        name='list'
    ),
]
