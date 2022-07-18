from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin

API_PREFIX = ""

urlpatterns = [
    re_path(settings.ADMIN_URL, admin.site.urls),

    {%- if cookiecutter.use_graphql == 'y' %}
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    {%- endif %}
    {%- if cookiecutter.use_rest == 'y' %}
    path(API_PREFIX, include("apps.users.routes")),
    {%- endif %}
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
