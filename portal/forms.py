from django import forms
from django.contrib.auth.models import User

# Form per la feature "Contattaci!"
class ContactForm(forms.Form):
    soggetto = forms.CharField(max_length = 100)
    messaggio = forms.CharField(max_length = 2000, widget=forms.Textarea)
    email = forms.EmailField()
    invia_copia = forms.BooleanField(required=False)

# Form per le iscrizioni
class SignupForm(forms.ModelForm) :

	repeat_password = forms.CharField(max_length = 100, required=True)

	class Meta:
		model = User
		fields = ['username','password', 'repeat_password', 
			'email','first_name','last_name']