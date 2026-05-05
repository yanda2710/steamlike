from django.contrib import admin
from django.urls import path, include

from library.views import health
from library.views import games, game_detailed, search_catalog, resolve_games

from auth_api.views import register, login_view, check_login, send_email


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/library/", include("core.urls")),
    path("api/health/", health),

    # Auth API
    path("api/auth/register/", register),
    path("api/auth/login/", login_view),
    path("api/users/me/", check_login),
    path("api/email/send/", send_email),
    
    # Library API
    path("api/library/entries/", games),
    path("api/library/entries/<str:external_game_id>/", game_detailed),
    path("api/catalog/search/", search_catalog), # type: ignore -> había un falso positivo de error
    path("api/catalog/resolve/", resolve_games), # type: ignore
]
