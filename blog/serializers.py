from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'embed_link', 'content', 'date_posted',
                  'author', 'language', 'tags', 'number_of_favorites',
                  'number_of_comments')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'content', 'date_posted', 'post_connected')
