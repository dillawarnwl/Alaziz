from django import forms
from .models import DonorRegister  # Import your Register model here

class RegisterForm(forms.ModelForm):
    bgroup = forms.ChoiceField(label='Blood Group', 
                               choices=[('--------------', '--------------'), 
                                        ('A+', 'A+'), ('A-', 'A-'),('B+','B+'),
                                        ('B-','B-'),('O+','O+'),('O-','O-'),
                                        ('AB+','AB+'),('AB-','AB-')], 
                                        widget=forms.Select(attrs={'class':'form-control col-lg-10'}))
    
    class Meta:
        model = DonorRegister
        fields = ['fname', 'lname', 'city', 'phone', 'donorid', 'bgroup', 'dob', 'ldonation', 'img', 'more']
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name',
            'city': 'Your Residential City',
            'phone': 'Phone Number',
            'donorid': 'Your CNIC',
            'more': 'Additional Information',
            'dob': 'Date of Birth',
            'ldonation': 'Last Donation',
            'img': 'Profile Image',
        }

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control col-lg-10'}),
            'lname': forms.TextInput(attrs={'class': 'form-control col-lg-10'}),
            'city': forms.TextInput(attrs={'class': 'form-control col-lg-10'}),
            'phone': forms.TextInput(attrs={'class': 'form-control col-lg-10'}),
            'donorid': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'XXXXX-XXXXXXX-X',
                                              'pattern': r'\d{5}-\d{7}-\d{1}', 'title': 'Enter a valid CNIC format'}),
            'more': forms.Textarea(attrs={'class': 'form-control col-lg-10'}),
            'dob': forms.DateInput(attrs={'class': 'form-control col-lg-10'}),
            'ldonation': forms.DateInput(attrs={'class': 'form-control col-lg-10'}),
            'img': forms.FileInput(attrs={'class': 'form-control col-lg-10'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}))
