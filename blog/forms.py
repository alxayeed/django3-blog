from django import forms
from .models import Comment


class emailForm(forms.Form):
    name = forms.CharField(max_length=20)
    your_email = forms.EmailField()
    recipient_email = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        # exclude = ['created', 'active', Post]
