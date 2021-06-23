from django.db.models import base
from rest_framework import urlpatterns
from rest_framework.routers import SimpleRouter

from .api.views import PostViewSet


router = SimpleRouter()

router.register('posts', PostViewSet, basename='post')

urlpatterns = router.urls