from django import forms

class CertificationAuthorityForm(forms.Form):
    name = forms.CharField(label='Certification authority name',  max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea, label='Description', max_length=2048, required=False)
    check_one = forms.BooleanField(label='Checkbox example', required=False)
