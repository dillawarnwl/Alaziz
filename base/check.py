from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import *
from .forms import NotesForm
# Create your views here.
class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/notes/list/'
    template_name = 'notes/notes_delete.html'

class NotesUpdateView(UpdateView):
    model = Notes
    success_url = '/notes/list/'
    form_class = NotesForm

class NotesCreateView(CreateView):
    model = Notes
    success_url = '/notes/list/'
    form_class = NotesForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes' # for rendering data from Notes.objects.all()
    login_url = 'login'

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'
    template_name = 'notes/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publishers"] = Publisher.objects.order_by('name')
        return context

