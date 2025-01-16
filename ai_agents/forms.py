from django import forms
from .models import CustomBot

class CustomBotForm(forms.ModelForm):
    class Meta:
        model = CustomBot
        fields = ['name', 'short_description', 'long_description', 'likes', 'dislikes', 'fears']
        widgets = {
            'short_description': forms.TextInput(attrs={'placeholder': 'E.g., ENFP. Energetic. Outgoing.'}),
            'long_description': forms.Textarea(attrs={'placeholder': 'Describe the bot\'s personality, approach, and demeanor...'}),
            'likes': forms.Textarea(attrs={'placeholder': 'E.g., Books, nature, art, collaboration.'}),
            'dislikes': forms.Textarea(attrs={'placeholder': 'E.g., Negativity, conflict, dishonesty.'}),
            'fears': forms.Textarea(attrs={'placeholder': 'E.g., Failure, rejection, being misunderstood.'}),
        }
        labels = {
            'name': 'Bot Name',
            'short_description': 'Short Description (Traits & Personality Type)',
            'long_description': 'Detailed Description',
            'likes': 'Likes',
            'dislikes': 'Dislikes',
            'fears': 'Fears',
        }
