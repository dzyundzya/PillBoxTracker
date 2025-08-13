from http import HTTPStatus as http

from pytest_django.asserts import assertRedirects


from pillbox.models import Comment


form_data = {
    'comment': {'text': 'New text'},
}


def test_author_can_edit_comment(
    user_client, pill_detail_url, edit_comment_url, comment, pill, user
):
    response = user_client.post(edit_comment_url, form_data['comment'])
    assertRedirects(response, pill_detail_url)
    comment.refresh_from_db()
    assert comment.text == form_data['comment']['text'], (
        'Текст комментария не обновился после редактирования. '
        f'Ожидаемый текст: {form_data["comment"]["text"]}, '
        f'фактический текст: {comment.text}'
    )
    assert comment.author == user, (
        'Автор комментария изменился после редактирования. '
        f'Ожидаемый автор: {user}, фактический автор: {comment.author}'
    )
    assert comment.pill == pill, (
        'Комментируемый препарат изменился после редактирования. '
        f'Ожидаемый препарат: {pill}, фактический препарат: {comment.pill}'
    )


def test_another_users_cant_edit_comment(
    another_user_client, edit_comment_url, comment
):
    response = another_user_client.post(edit_comment_url, form_data['comment'])
    assert response.status_code == http.FOUND
    new_comment = Comment.objects.get(id=comment.pk,)
    assert new_comment.text == comment.text, (
        'Текст комментария изменился при попытке редактирования '
        f'чужим пользователем. Ожидаемый текст: {comment.text}, '
        f'фактический текст: {new_comment.text}'
    )
    assert new_comment.author == comment.author, (
        'Автор комментария изменился при попытке редактирования '
        f'чужим пользователем. Ожидаемый автор: {comment.author}, '
        f'фактический автор: {new_comment.author}'
    )
    assert new_comment.pill == comment.pill, (
        'Комментируемый препарат изменился при попытке редактирования '
        f'чужим пользователем. Ожидаемый препарат: {comment.pill}, '
        f'фактический препарат: {new_comment.pill}'
    )
