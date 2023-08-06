from django import forms
from django.contrib.auth import get_user_model

from .models import Comment
from .models import Article

User = get_user_model()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)  # Remove 'author' from the fields

    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image']  # Include 'image' field here
