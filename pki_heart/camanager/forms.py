from django import forms
from pki_heart.utils import supported_private_key_algorithms

class CertificationAuthorityForm(forms.Form):
    name = forms.CharField(label='Certification authority name',  max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}), label='Description', max_length=2048, required=False)

    hints = {
        'name': 'Descriptive human readable name.',
    }


class NewCACertForm(forms.Form):
    name = forms.CharField(label='Certificate name',  max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}), label='Description', max_length=2048, required=False)
    allow_issue = forms.BooleanField(label='Allow issuing new client certificates', required=False)
    subject = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}), label='Subject', max_length=2048, required=True)
    issuer = forms.ChoiceField(label='Issuer', choices=[('self-signed', 'Self signed')])
    private_key_algorithm = forms.ChoiceField(label='Private key algorithm', choices=[(x.get('id'),x.get('label')) for x in supported_private_key_algorithms()])
    # TODO: signature_algorithm

    hints = {
        'name': 'Descriptive human readable name.',
        'subject': 'Certificate subject DN fields, one element per line, each line must start with DN element name (e.g. <b>CN</b> or <b>L</b>) or OID (e.g. <b>{2.5.4.3}</b>) followed by <b>=</b> and element value. For example, <b>CN=Demo Root CA</b> or <b>{1.2.643.100.3}=123-456-789-01</b>.'
    }


class EditCACertForm(forms.Form):
    name = forms.CharField(label='Certification authority name',  max_length=200, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}), label='Description', max_length=2048, required=False)

    hints = {
        'name': 'Descriptive human readable name.',
    }

