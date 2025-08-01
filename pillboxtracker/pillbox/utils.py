from django.db.models import Count
from django.utils import timezone


def comment_count(self):
    return self.annotate(comment_count=Count('comments'))


def pill_filter(self):
    return self.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
