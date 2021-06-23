from django.db.models import query
from django.db.models.base import Model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError

from ..models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Filters the queryset by:
            title - title, icontains (case insensitve, contains)\n
            tag - tags, filters by tags, can filter by multiple tags,
            e.g. (\n
                localhost:8000/api/articles?tags=python&tags=backend\n
                Will return articles that has the tags 'python' and/or 'backend'.
            )
        """
        queryset = Post.objects.all()

        user = self.request.query_params.get('user', None)

        if user:
            queryset = queryset.filter(author__slug=user)
            return queryset

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return queryset
            
        raise ValidationError(detail={'error':'must specify a user.'})

