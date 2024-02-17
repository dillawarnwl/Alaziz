from django import forms
# Import your Register model here
from .models import DonorRegister, OrganizationRegister


class RegisterForm(forms.ModelForm):
    bgroup = forms.ChoiceField(label='Blood Group',
                               choices=[('--------------', '--------------'),
                                        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'),
                                        ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'),
                                        ('AB+', 'AB+'), ('AB-', 'AB-')],
                               widget=forms.Select(attrs={'class': 'form-control col-lg-10'}))

    organization = forms.ModelChoiceField(
        queryset=OrganizationRegister.objects.all(),
        empty_label="None",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control col-lg-10'})
    )

    certification = forms.BooleanField(
        label='',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = DonorRegister
        fields = ['fname', 'lname', 'village', 'city', 'phone', 'donorid',
                  'bgroup', 'dob', 'ldonation', 'img', 'organization', 'more']
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name',
            'village': 'Your Village',
            'city': 'Your Residential City',
            'phone': 'Phone Number',
            'donorid': 'Your CNIC',
            'more': 'Additional Information',
            'dob': 'Date of Birth',
            'ldonation': 'Last Donation',
            'img': 'Profile Image',
            'organization': 'Organization',
        }

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder':'Your First Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Your Last Name',}),
            'village': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Your Village/Town/Mohallah',}),
            'city': forms.TextInput(attrs={'class': 'form-control col-lg-10','placeholder': 'Your City',}),
            'phone': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': '03000000000',}),
            'donorid': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'XXXXX-XXXXXXX-X',
                                              'pattern': r'\d{5}-\d{7}-\d{1}', 'title': 'Enter a valid CNIC format'}),
            'more': forms.Textarea(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Enter your donor experince...',}),
            'dob': forms.DateInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'YYYY-MM-DD',}),
            'ldonation': forms.DateInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'YYYY-MM-DD',}),
            'img': forms.FileInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Your profile image',}),
        }


class OrganizationRegistrationForm(forms.ModelForm):
    class Meta:
        model = OrganizationRegister
        fields = ['org_name', 'org_head', 'org_email',
                  'head_ph', 'org_logo', 'org_address']
        labels = {
            'org_name': 'Organization Name',
            'org_head': 'Head of Organization',
            'org_email': 'Organization Official Email',
            'head_ph': 'Concern Person',
            'org_logo': 'Organization Logo',
            'org_address': 'Organization Address',
        }

        widgets = {
            'org_name': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Enter organization name'}),
            'org_head': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Name of organization head'}),
            'org_email': forms.EmailInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Organization official email'}),
            'head_ph': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Concern person phone'}),
            'org_logo': forms.FileInput(attrs={'class': 'form-control col-lg-10'}),
            'org_address': forms.TextInput(attrs={'class': 'form-control col-lg-10', 'placeholder': 'Organization address...'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter subject'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter your message'}))

