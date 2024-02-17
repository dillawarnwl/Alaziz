from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.views import View
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token

User = get_user_model()

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Thank you for your email confirmation. Now you can log in to your account.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid!")
        return redirect('home')

class UserLoginView(View):
    def post(self, request):
        get_email = request.POST.get('email')
        get_password = request.POST.get('password')

        if get_email and get_password:
            myuser = authenticate(username=get_email, password=get_password)
            if myuser is not None:
                login(request, myuser)
                messages.success(request, 'User logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials!')
                return redirect('login')
        else:
            messages.error(request, 'Both email and password are required.')
            return redirect('login')

    def get(self, request):
        return render(request, 'login.html')
    
class UserSignUpView(View):
    def post(self, request):
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')

        if not get_password or not get_confirm_password:
            messages.error(request, 'Password is required')
            return redirect('signup')

        if get_password != get_confirm_password:
            messages.error(request, 'Password and Confirm Password do not match')
            return redirect('signup')

        try:
            if User.objects.get(email=get_email):
                messages.error(request, 'Email already exists')
                return redirect('signup')
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username=get_email, password=get_password)
        user.is_active = False
        user.save()
        self.send_activation_email(request, user, get_email)
        return redirect('confirm')

    def get(self, request):
        return render(request, 'signup.html')

    def send_activation_email(self, request, user, to_email):
        try:
            mail_subject = "Activate your Account"
            message = render_to_string("template_activate_account.html", {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            "protocol": 'https' if request.is_secure() else 'http'
            })
        
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
        
            messages.success(request, f'Dear <b>Donor!</b>, please go to your email <b>{to_email}</b> inbox and click on the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    
        except Exception as e:
        
            messages.error(request, f'There was a problem sending the activation email. Please try again later or contact support.{e}')
 

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'User Logout Successfully!')
        return render(request, 'login.html')
