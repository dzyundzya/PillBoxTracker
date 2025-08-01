from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse

from .forms import CommentForm, PillForm
from .mixins import CommentMixin, OnlyAdminMixin
from .models import Comment, Pill
from .utils import comment_count, pill_filter


class PillDetailView(DetailView):
    model = Pill
    template_name = 'pillbox/pill_detail.html'
    pk_url_kwarg = 'pill_id'

    def get_object(self, queryset=None):
        post = get_object_or_404(Pill, id=self.kwargs.get('pill_id'))
        if self.request.user.is_staff:
            return post
        return get_object_or_404(
            pill_filter(self.get_queryset()), id=self.kwargs.get('pill_id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class PillCreateView(LoginRequiredMixin, CreateView):
    model = Pill
    form_class = PillForm
    template_name = 'pillbox/pill_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.is_staff
        return super().form_valid(form)


class PillUpdateView(OnlyAdminMixin, UpdateView):
    model = Pill
    form_class = PillForm
    template_name = 'pillbox/pill_create.html'
    pk_url_kwarg = 'pill_id'


class PillDeleteView(OnlyAdminMixin, DeleteView):
    model = Pill
    pk_url_kwarg = 'pill_id'
    template_name = 'pillbox/pill_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PillForm(
            instance=self.object
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    pill_object = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.pill_object = get_object_or_404(Pill, pk=kwargs.get('pill_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pill = self.pill_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'pillbox:pill_detail', kwargs={'pill_id': self.pill_object.pk}
        )


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    pass
