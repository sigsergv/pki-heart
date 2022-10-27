from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), label='Username',  max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=100, required=True)
    redirect = forms.CharField(widget=forms.HiddenInput)
