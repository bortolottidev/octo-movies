from django import forms

# Form per la feature "Contattaci!"
class ContactForm(forms.Form):
    soggetto = forms.CharField(max_length = 100)
    messaggio = forms.CharField(max_length = 2000, widget=forms.Textarea)
    email = forms.EmailField()
    invia_copia = forms.BooleanField(required=False)
