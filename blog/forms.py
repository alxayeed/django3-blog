from django import forms


class emailForm(forms.Form):
    name = forms.CharField(max_length=20)
    your_email = forms.EmailField()
    recipient_email = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea)
