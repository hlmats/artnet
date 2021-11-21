from django import forms
from .models import Image
from .models import Comment


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'description', 'style')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
