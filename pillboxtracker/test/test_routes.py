from http import HTTPStatus as http

import pytest
from django.test.client import Client
# from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from pillbox.models import Pill

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    (
        (lf('homepage_url'), lf('unlogged_client'), http.OK),
        (lf('about_url'), lf('unlogged_client'), http.OK),
        (lf('rules_url'), lf('unlogged_client'), http.OK),
        (lf('login_url'), lf('unlogged_client'), http.OK),
        (lf('logout_url'), lf('unlogged_client'), http.OK),
        (lf('registration_url'), lf('unlogged_client'), http.OK),
        (lf('create_pill_url'), lf('staff_user_client'), http.OK),
        (lf('create_pill_url'), lf('user_client'), http.FOUND),
        (lf('edit_pill_url'), lf('staff_user_client'), http.OK),
        (lf('edit_pill_url'), lf('user_client'), http.FOUND),
        (lf('delete_pill_url'), lf('staff_user_client'), http.OK),
        (lf('delete_pill_url'), lf('user_client'), http.FOUND),
        (lf('admin_profile_url'), lf('staff_user_client'), http.OK),
        (lf('profile_url'), lf('user_client'), http.OK),
        (lf('profile_url'), lf('staff_user_client'), http.FOUND),
        (lf('admin_profile_url'), lf('user_client'), http.FOUND),
        (lf('edit_comment_url'), lf('user_client'), http.OK),
        (lf('delete_comment_url'), lf('user_client'), http.OK),
        (lf('edit_comment_url'), lf('another_user_client'), http.FOUND),
        (lf('delete_comment_url'), lf('another_user_client'), http.FOUND),
    ),
)
def test_pages_availability_for_different_user(
    reverse_url, parametrized_client, expected_status,
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status
