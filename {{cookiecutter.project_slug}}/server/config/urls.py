from django.conf import settings
from django.conf.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

API_PREFIX = ""

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),

    {%- if cookiecutter.use_graphql == 'y' %}
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    {%- endif %}
    {%- cookiecutter.use_rest == 'y' %}
    path(API_PREFIX, include("apps.users.routes")),
    {%- endif %}
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
