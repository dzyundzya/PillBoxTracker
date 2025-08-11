import pytest
from django.test.client import Client
from django.urls import reverse
from mixer.backend.django import mixer as _mixer

from pillbox.models import Comment, Pill, Pillbox


@pytest.fixture()
def mixer():
    return _mixer


@pytest.fixture
def unlogged_client(client):
    return client


@pytest.fixture
def user(django_user_model, mixer):
    return mixer.blend(django_user_model)


@pytest.fixture
def user_client(user):
    client = Client()
    client.force_login(user)
    return client



@pytest.fixture
def another_user(django_user_model, mixer):
    return mixer.blend(django_user_model)


@pytest.fixture
def another_user_client(another_user):
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def staff_user(django_user_model, mixer):
    return mixer.blend(
        django_user_model,
        is_staff=True
    )


@pytest.fixture
def staff_user_client(staff_user):
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture
def pill(staff_user, mixer):
    return mixer.blend(Pill, author=staff_user, is_published=True)


@pytest.fixture
def comment(user, pill, mixer):
    return mixer.blend(Comment, pill=pill, author=user)


@pytest.fixture
def homepage_url():
    return reverse('pages:homepage')


@pytest.fixture
def about_url():
    return reverse('pages:about')


@pytest.fixture
def rules_url():
    return reverse('pages:rules')


@pytest.fixture
def registration_url():
    return reverse('users:registration')


@pytest.fixture
def login_url():
    return reverse('login')


@pytest.fixture
def logout_url():
    return reverse('logout')


@pytest.fixture
def create_pill_url():
    return reverse('pillbox:create_pill')


@pytest.fixture
def edit_pill_url(pill):
    return reverse('pillbox:edit_pill', args=(pill.pk,))


@pytest.fixture
def delete_pill_url(pill):
    return reverse('pillbox:delete_pill', args=(pill.pk,))


@pytest.fixture
def pill_detail_url(pill):
    return reverse('pillbox:pill_detail', args=(pill.pk,))


@pytest.fixture
def admin_profile_url(staff_user):
    return reverse('pillbox:admin_profile', args=(staff_user.username,))


@pytest.fixture
def profile_url(user):
    return reverse('pillbox:profile', args=(user.username,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('pillbox:edit_comment', args=(comment.pk, comment.pill.pk))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('pillbox:delete_comment', kwargs={
        'comment_id': comment.pk, 'pill_id': comment.pill.pk
    })
