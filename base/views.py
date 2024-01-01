from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import CreateView, TemplateView, ListView
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView, FormView
from .forms import RegisterForm, ContactForm
from .models import DonorRegister
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone



class HomeView(TemplateView):
    template_name = "home.html"

class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']

        sender_email = email

        recipient_email = 'dillawar612@gmail.com'

        send_mail(
            subject,
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
            sender_email,  
            [recipient_email],  
            fail_silently=False,
        )

        messages.success(self.request, 'Message sent successfully.')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your submission. Please check the form and try again.')

        return super().form_invalid(form)

class ConfirmView(TemplateView):
    template_name = "confirmation.html"

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class RegisterView(CreateView):
    template_name = "volunteer-registration.html"
    form_class = RegisterForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("donorlist")

    
class UpdateView(UpdateView):
    template_name = "volunteer-registration.html"
    model = DonorRegister
    success_url = '/donorlist/'
    form_class = RegisterForm

    
class DeleteView(DeleteView):
    model = DonorRegister
    success_url = '/donorlist/'
    template_name = 'donor-delete.html'

class ProfileView(View):
    template_name = "volunteer-profile.html"

    def get(self, request):
        try:
            donor = DonorRegister.objects.get(user=request.user)
            context = {'donor': donor}
            return render(request, self.template_name, context)
        except:
            return redirect('register')
        

    
class DonorView(View):
    template_name = "volunteer-profile.html"

    def get(self, request, pk):
        donor = DonorRegister.objects.get(pk=pk)
        context = {'donor': donor}
        return render(request, self.template_name, context)
    
class HealthTipsView(TemplateView):
    template_name = "health-tips.html"


class DonorListView(ListView):
    template_name = "donor-list.html"
    model = DonorRegister
    context_object_name = 'donors'  

    def get_queryset(self):
        name_or_city = self.request.GET.get('q', '')
        blood_group = self.request.GET.get('p', '')

        form_submitted = any([name_or_city, blood_group])

        if form_submitted:
            if name_or_city and blood_group:
                queryset = DonorRegister.objects.filter(
                    Q(city__icontains=name_or_city) |
                    Q(fname__icontains=name_or_city) |
                    Q(lname__icontains=name_or_city),
                    Q(bgroup__icontains=blood_group),
                    Q(ldonation__lte=timezone.now() - timedelta(days=56))
                ).order_by('-dob')
            else:
                if name_or_city:
                    queryset = DonorRegister.objects.filter(
                        Q(city__icontains=name_or_city) |
                        Q(fname__icontains=name_or_city) |
                        Q(lname__icontains=name_or_city),
                        Q(ldonation__lte=timezone.now() - timedelta(days=56))
                    ).order_by('-dob')
                else:
                    queryset = DonorRegister.objects.filter(
                        Q(bgroup__icontains=blood_group),
                        Q(ldonation__lte=timezone.now() - timedelta(days=56))
                    ).order_by('-dob')
        else:
            queryset = DonorRegister.objects.filter(
                Q(ldonation__lte=timezone.now() - timedelta(days=56))
            ).order_by('-dob')

        return queryset
