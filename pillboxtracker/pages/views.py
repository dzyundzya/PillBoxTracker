from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from .constants import PagesConstants as const
from .models import Accordion
from pillbox.models import Pill
from pillbox.utils import comment_count, pill_filter


class HomePage(ListView):
    model = Pill
    template_name = 'pages/homepage.html'
    paginate_by = const.PAGINATION

    def get_queryset(self):
        return comment_count(pill_filter(Pill.objects)).order_by('-pub_date')


class Rules(TemplateView):
    template_name = 'pages/rules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"] = Accordion.objects.all()
        return context


class About(TemplateView):
    template_name = 'pages/about.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
