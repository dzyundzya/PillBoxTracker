import pytest
from pytest_lazyfixture import lazy_fixture as lf

from pillbox.forms import CommentForm, PillForm, PillBoxForm
from pillbox.constants import PillboxConstants as const
from users.forms import CustomUserUpdateForm


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, pagination, test_data',
    (
        (
            lf('homepage_url'), lf('staff_user_client'),
            const.PAGINATION.PILL, lf('few_pills')
        ),
        (
            lf('profile_url'), lf('user_client'),
            const.PAGINATION.PILLBOX, lf('few_pillboxes')
        ),
        (
            lf('admin_profile_url'), lf('staff_user_client'),
            const.PAGINATION.PILL, lf('few_pills')
        ),
    ),
)
def test_pagination_on_different_pages(
    reverse_url, parametrized_client, pagination, test_data
):
    response = parametrized_client.get(reverse_url)
    pills_count = response.context['object_list'].count()
    assert pills_count == pagination, (
        f'Убедитесь, что пагинация страницы - {reverse_url}, '
        f'ровна {pagination}, а не {pills_count}.'
    )


def test_comments_ordering(user_client, few_comments, pill_detail_url):
    response = user_client.get(pill_detail_url)
    pill = response.context['pill']
    all_comments = pill.comments.all()
    all_timestamp = [comment.created_at for comment in all_comments]
    sotred_timestamp = sorted(all_timestamp)
    assert all_timestamp == sotred_timestamp, (
        'Убедитесь, что комментарии отсортированы от старых к новым.'
    )


@pytest.mark.parametrize(
    'reverse_url, parametrized_client, forms',
    (
        (lf('create_pill_url'), lf('staff_user_client'), PillForm),
        (lf('edit_pill_url'), lf('staff_user_client'), PillForm),
        (lf('delete_pill_url'), lf('staff_user_client'), PillForm),
        (lf('create_pillbox_url'), lf('user_client'), PillBoxForm),
        (lf('edit_pillbox_url'), lf('user_client'), PillBoxForm),
        (lf('delete_pillbox_url'), lf('user_client'), PillBoxForm),
        (lf('add_comment_url'), lf('user_client'), CommentForm),
        (lf('edit_comment_url'), lf('user_client'), CommentForm),
        (lf('edit_profile_url'), lf('user_client'), CustomUserUpdateForm),
        (lf('edit_profile_url'), lf('staff_user_client'), CustomUserUpdateForm),
    )
)
def test_another_user_has_form(reverse_url, parametrized_client, forms):
    response = parametrized_client.get(reverse_url)
    assert 'form' in response.context, (
        f"Форма отсутствует в контексте для URL: {reverse_url}. "
        f"Клиент: {response.wsgi_request.user.username}"
    )
    assert isinstance(response.context['form'], forms), (
        f"Неверный тип формы для URL: {reverse_url}. "
        f"Клиент: {response.wsgi_request.user.username}"
    )


@pytest.mark.parametrize(
    'reverse_url, parametrized_client',
    (
        (lf('create_pill_url'), lf('user_client')),
        (lf('edit_pill_url'), lf('user_client')),
        (lf('delete_pill_url'), lf('user_client')),
        (lf('create_pillbox_url'), lf('staff_user_client')),
        (lf('edit_pillbox_url'), lf('staff_user_client')),
        (lf('delete_pillbox_url'), lf('staff_user_client')),
        (lf('add_comment_url'), lf('unlogged_client')),
        (lf('edit_comment_url'), lf('unlogged_client')),
    )
)
def test_another_user_has_not_form(reverse_url, parametrized_client):
    response = parametrized_client.get(reverse_url)
    assert 'form' not in response.context, (
        f"Форма присутствует в контексте для URL: {reverse_url}. "
        f"Клиент: {response.wsgi_request.user.username}"
    )
