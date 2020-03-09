from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.forms import CommentForm
from blog.models import Comment
from .forms import EventForm
from django.http import HttpResponse
from blog.views import CommentDeleteView, CommentUpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar
import calendar


class CalendarView(ListView):
    model = Event
    template_name = 'scheduler/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#def event(request, event_id=None):
#    instance = Event()
#    if event_id:
#        instance = get_object_or_404(Event, pk=event_id)
#    else:
#        instance = Event()
#
#    form = EventForm(request.POST or None, instance=instance)
#    if request.POST and form.is_valid():
#        form.save()
#        return redirect('calendar-home')
#    return render(request, 'scheduler/event.html', {'form': form})

class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'scheduler/events_home.html'
    ordering = ['-start_time']
    paginate_by = 3

class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'event': self.object, 'author':
                                              self.request.user})
        return context

class EventCommentView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'scheduler/event_detail.html'
    form_class = CommentForm
    model = Event

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.event = self.object
        comment.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('event-detail', kwargs={'pk': self.object.pk})

class EventView(View):
    def get(self, request, *args, **kwargs):
        view = EventDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventCommentView.as_view()
        return view(request, *args, **kwargs)

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'scheduler/event_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author

    def get_success_url(self, **kwargs):
        return reverse('event-home')

class EventCommentDeleteView(CommentDeleteView):
    template_name = 'scheduler/event_confirm_delete.html'
    def get_success_url(self, **kwargs):
        return reverse('event-detail', kwargs={'pk': self.kwargs['pk_event']})

class EventCommentUpdateView(CommentUpdateView):
    def get_post(self):
        return self.get_object().event

    def get_success_url(self, **kwargs):
        return reverse('event-detail', kwargs={'pk': self.kwargs['pk_event']})

