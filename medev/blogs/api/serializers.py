from re import I
from rest_framework import serializers

from ..models import Post
from users.api.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'content', 'slug', 'author')
        read_only_fields = ('slug', 'author')
        lookup_fied = 'slug'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        return post
