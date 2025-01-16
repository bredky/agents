from django import forms
from .models import Comment

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your reply...', 'rows': 2}),
        }