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
from .forms import RegisterForm, ContactForm, OrganizationRegistrationForm
from .models import DonorRegister, OrganizationRegister
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # for pagination


class HomeView(TemplateView):
    template_name = "home.html"
    model = OrganizationRegister

class AboutView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = OrganizationRegister.objects.all()
        return context



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
        # Check if donorid already exists
        donorid = form.cleaned_data['donorid']
        if DonorRegister.objects.filter(donorid=donorid).exists():
            messages.error(self.request, 'Error: Donor ID already exists. Please choose a different Donor ID.')
            return render(self.request, self.template_name, {'form': form})

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("donorlist")
    
@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class OrganizationRegistrationView(CreateView):
    model = OrganizationRegister
    form_class = OrganizationRegistrationForm
    template_name = 'register_organization.html'
    success_url = reverse_lazy('about')

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can perform additional actions here if needed
        return response

    
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
            return redirect('register-donor')
        

    
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
    paginate_by = 25  # Number of donors to display per page

    def get_context_data(self, **kwargs):
        context = super(DonorListView, self).get_context_data(**kwargs)
        donors = context['donors']

        # Paginate the donor list
        paginator = Paginator(donors, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            donors = paginator.page(page)
        except PageNotAnInteger:
            # If the page is not an integer, deliver the first page.
            donors = paginator.page(1)
        except EmptyPage:
            # If the page is out of range (e.g., 9999), deliver the last page.
            donors = paginator.page(paginator.num_pages)

        context['donors'] = donors
        return context
 

    def get_queryset(self):
        name_or_city = self.request.GET.get('q', '')
        blood_group = self.request.GET.get('p', '')

        form_submitted = any([name_or_city, blood_group])

        if form_submitted:
            if name_or_city and blood_group:
                queryset = DonorRegister.objects.filter(
                    Q(city__icontains=name_or_city) |
                    Q(village__icontains=name_or_city) |
                    Q(fname__icontains=name_or_city) |
                    Q(lname__icontains=name_or_city),
                    Q(bgroup__icontains=blood_group),
                    Q(ldonation__lte=timezone.now() - timedelta(days=90))
                ).order_by('-dob')
            else:
                if name_or_city:
                    queryset = DonorRegister.objects.filter(
                        Q(city__icontains=name_or_city) |
                        Q(village__icontains=name_or_city) |
                        Q(fname__icontains=name_or_city) |
                        Q(lname__icontains=name_or_city),
                        Q(ldonation__lte=timezone.now() - timedelta(days=90))
                    ).order_by('-dob')
                else:
                    queryset = DonorRegister.objects.filter(
                        Q(bgroup__icontains=blood_group),
                        Q(ldonation__lte=timezone.now() - timedelta(days=90))
                    ).order_by('-dob')
        else:
            queryset = DonorRegister.objects.filter(
                Q(ldonation__lte=timezone.now() - timedelta(days=90))
            ).order_by('-dob')

        return queryset
