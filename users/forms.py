from django import forms
from django.core.exceptions import ValidationError
from .models import registrationmodel
import re

class registrationmodelmodelform(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Name','autocomplete':'off'}), max_length=20, required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter Valid Email To Get Emails Ex:abcdef@gmail.com '}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Create Your Password'}), max_length=20, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your Password'}), max_length=20, required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Mobile Number'}), max_length=20, required=True)
    status = forms.CharField(widget=forms.HiddenInput(), initial='waiting', max_length=100, required=False)

    class Meta:
        model = registrationmodel
        fields = ['name', 'email', 'password', 'confirm_password', 'mobile', 'status']

    def __init__(self, *args, **kwargs):
        # Check if it's an update form (i.e., instance is passed)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        
        # If it's an update, remove the password fields
        if instance and instance.pk:
            self.fields.pop('password', None)
            self.fields.pop('confirm_password', None)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if password:
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long.")
            if not re.search(r"[A-Z]", password):
                errors.append("Password must contain at least one uppercase letter A-Z.")
            if not re.search(r"[a-z]", password):
                errors.append("Password must contain at least one lowercase letter a-z.")
            if not re.search(r"[0-9]", password):
                errors.append("Password must contain at least one digit 0-9.")
            if not re.search(r"[!@#$%^&*()_+]", password):
                errors.append("Password must contain at least one special character @,!,#.....")

        if errors:
            raise ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        mobile = cleaned_data.get("mobile")
        if mobile and not re.match(r'^\d{10}$', mobile):
            self.add_error('mobile', "Invalid Mobile number.")

        return cleaned_data




from django import forms

class HateSpeechForm(forms.Form):
    sentence = forms.CharField(label='Enter sentence', max_length=1000, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40,'placeholder': 'Enter the sentence for hate speech prediction...',}))
