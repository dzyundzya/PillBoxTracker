from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse

from .models import Comment, Pill, Pillbox


class OnlyAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('pages:homepage')
        return super().dispatch(request, *args, **kwargs)


class OnlyAuthorPillboxMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff or not self.request.user.is_authenticated:
            return redirect(
                'pages:homepage',
            )
        return super().dispatch(request, *args, **kwargs)


class PillSuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            'pillbox:pill_detail',
            kwargs={'pill_id': self.kwargs.get('pill_id')}
        )


class PillBoxSuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            'pillbox:pillbox_detail',
            kwargs={'pillbox_id': self.kwargs.get('pillbox_id')}
        )


class CommentMixin(PillSuccessUrlMixin, LoginRequiredMixin, View):
    model = Comment
    template_name = 'pillbox/comment.html'
    pk_url_kwarg = 'comment_id'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return redirect(
                'pillbox:pill_detail',
                pill_id=self.kwargs['pill_id']
            )
        return super().dispatch(request, *args, **kwargs)


class UserSuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            'pillbox:profile', kwargs={'username': self.request.user.username}
        )


class PillBoxMixin(OnlyAuthorPillboxMixin, View):
    model = Pillbox
    template_name = 'pillbox/pillbox_create.html'
    pk_url_kwarg = 'pillbox_id'


class PillMixin(OnlyAdminMixin, View):
    model = Pill
    pk_url_kwarg = 'pill_id'
    template_name = 'pillbox/pill_create.html'
