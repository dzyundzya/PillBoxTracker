from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse

from .constants import PillboxConstants as const
from .forms import CommentForm, PillForm
from .mixins import CommentMixin, OnlyAdminMixin, PillSuccessUrlMixin, UserSuccessUrlMixin
from .models import Category, Comment, Pill
from .utils import comment_count, pill_filter
from users.forms import CustomUserUpdateForm


User = get_user_model()


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


class PillCreateView(PillSuccessUrlMixin, LoginRequiredMixin, CreateView):
    model = Pill
    form_class = PillForm
    template_name = 'pillbox/pill_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
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


class CategoryListView(ListView):
    model = Pill
    template_name = 'pillbox/category.html'
    paginate_by = const.PAGINATION

    def get_queryset(self):
        self.pill_category = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug'), is_published=True,
        )
        posts = comment_count(
            pill_filter(self.pill_category.posts)).order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.pill_category
        return context


class AdminProfileView(ListView):
    model = User
    template_name = 'pillbox/admin_profile.html'
    context_object_name = 'profile'
    paginate_by = const.PAGINATION

    def get_queryset(self):
        return comment_count(Pill.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context
    

class ProfileView(ListView):
    model = User
    template_name = 'pillbox/profile.html'
    context_object_name = 'profile'
    paginate_by = const.PAGINATION

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(UserSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'pillbox/user.html'

    def get_object(self, queryset=None):
        return self.request.user
