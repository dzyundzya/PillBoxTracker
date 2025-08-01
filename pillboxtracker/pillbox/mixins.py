from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse

from .models import Comment


class OnlyAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return redirect(
                'pillbox:pill_detail',
                post_id=self.kwargs.get('pill_id')
            )
        return super().dispatch(request, *args, **kwargs)


class PillSuccessUrlMixin:
    def get_success_url(self):
        return reverse(
            'pillbox:pill_detail',
            kwargs={'pill_id': self.kwargs.get('pill_id')}
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
                post_id=self.kwargs['pill_id']
            )
        return super().dispatch(request, *args, **kwargs)
