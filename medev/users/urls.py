from django.urls import path

from .api.views import PasswordResetConfirmView


urlpatterns = [
    path(
        'password/reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    )
]
