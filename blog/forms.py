from .models import Post, Comment, Category
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ArchiveYearForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['date_posted']


