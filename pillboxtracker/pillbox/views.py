from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse

from .constants import PillboxConstants as const
from .forms import CommentForm, PillForm, PillBoxForm
from .mixins import CommentMixin, OnlyAdminMixin, PillSuccessUrlMixin, UserSuccessUrlMixin, PillBoxMixin
from .models import Category, Comment, Pill, Pillbox
from .utils import comment_count, pill_filter
from users.forms import CustomUserUpdateForm


User = get_user_model()


class PillDetailView(DetailView):
    """Представление для отображения детальной информации о препарате."""
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


class PillCreateView(PillSuccessUrlMixin, OnlyAdminMixin, CreateView):
    """
    Представление для создание нового препарата.

    Класс предоставляет интерфейс для создания новых записей о препаратах.
    Доступ к созданию имеют только пользователи с правами администратора.
    """
    model = Pill
    form_class = PillForm
    template_name = 'pillbox/pill_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PillUpdateView(OnlyAdminMixin, UpdateView):
    """
    Представление для обновления существующего препарата.

    Класс предоставляет интерфейс для редактирования записей о препаратах.
    Доступ к редактированию имеют только пользователи с правами администратора.
    """
    model = Pill
    form_class = PillForm
    template_name = 'pillbox/pill_create.html'
    pk_url_kwarg = 'pill_id'


class PillDeleteView(OnlyAdminMixin, DeleteView):
    """
    Представление для удаления препарата.

    Класс предоставляет интерфейс для удаления записей о препаратах.
    Доступ к удалению имеют только пользователи с правами администратора.
    Перед удалением отображается форма подтверждения.
    """
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
    """
    Представления для создания нового комментария к препарату.

    Класс представляет интерфейс для создания комментариев.
    Доступ к комментированию имеют только авторизованные пользователи.
    Автоматический устанавливает автора комментария, связывает с препаратом.
    """
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
    """
    Представления для обновления комментария.

    Класс представляет интерфейс для редактирования комментариев.
    Доступ к редактированию комментариев имеет только автор комментария.
    """
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    """
    Представления для удаления комментария.

    Класс представляет интерфейс для удаления комментариев.
    Доступ к удалению комментариев имеет только автор комментария.
    Перед удалением отображается форма подтверждения.
    """
    pass


class CategoryListView(ListView):
    """
    Представление для отображения списка препаратов по категории.

    Класс предоставляет интерфейс для просмотра препаратов,
    отфильтрованных по выбранной категории.
    """
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
    """
    Представление для административного профиля пользователя.

    Класс предоставляет интерфейс для просмотра профилей пользователей
    с административными правами. Отображает список всех препаратов
    с подсчетом комментариев и пагинацией.
    """
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
    """
    Представление для пользовательского профиля.

    Класс представляет интерфейс для просмотра профиля пользователя,
    включая его таблеточницу.
    """
    model = User
    template_name = 'pillbox/profile.html'
    context_object_name = 'profile'
    paginate_by = 3

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Pillbox.objects.filter(user__username=username).select_related(
            'pill__manufacturer', 'pill__medicine_form',
        ).prefetch_related(
            'pill__active_substance', 'reminder_time'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class ProfileUpdateView(UserSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    """
    Предстваление для обновления профиля пользователя.

    Класс представляет интерфейс для редактирования профиля.
    Пользовтель может редактировать только свой профиль.
    """
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'pillbox/user.html'

    def get_object(self, queryset=None):
        return self.request.user


class PillBoxCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой таблеточницы.

    Класс предоставляет интерфейс для создания таблеточницы.
    Автомотический связывает таблеточницу с текущим пользователем.    
    """
    model = Pillbox
    form_class = PillBoxForm
    template_name = 'pillbox/pillbox_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PillBoxUpdateView(PillBoxMixin, UpdateView):
    """
    Представление для обновления таблеточницы.

    Класс предоставляет интерфейс для реадактирования таблеточницы.
    Доступ к редактированию таблеточницы имеет только автор таблеточницы.
    """
    form_class = PillBoxForm


class PillBoxDeleteView(PillBoxMixin, DeleteView):
    """
    Представление для удаления таблеточницы.

    Класс предоставляет интерфейс для удаления таблеточницы.
    Доступ к удалению таблеточницы имеет только автор таблеточницы.
    Перед удалением отображается форма подтверждения.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PillBoxForm(
            instance=self.object
        )
        return context

    def get_success_url(self):
        return reverse(
            'pillbox:profile', kwargs={'username': self.request.user.username}
        )
