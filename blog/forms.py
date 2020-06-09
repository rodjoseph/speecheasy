from django import forms
from .models import Comment, Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'embed_link',
            # 'tags',
        ]
        
class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
