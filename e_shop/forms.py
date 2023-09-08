from django import forms
from .models import *

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-2 px-4 rounded-xl border'
            })
        }