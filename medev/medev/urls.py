from django.contrib import admin
from django.urls import include, path

from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    UserDetailsView
)


auth_urls = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path(
        'password-change/',
        PasswordChangeView.as_view(),
        name='rest_password_change'
    ),
    path(
        'password-reset/',
        PasswordResetView.as_view(),
        name='rest_password_reset'
    ),
    path('', include('users.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls))
]
