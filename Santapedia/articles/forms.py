from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='Email')
    subject = forms.CharField(max_length=150, label='Assunto')
    message = forms.CharField(widget=forms.Textarea ,label='Mensagem')

