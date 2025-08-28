from django.contrib.auth import get_user_model
from django.utils import timezone
import pytest


User = get_user_model()


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'birthday, expected',
    (
        (timezone.now() - timezone.timedelta(days=750), 2),
        (timezone.now() - timezone.timedelta(days=725), 1),
    )
)
def test_user_get_age(birthday, expected):
    obj = User.objects.create(
        username='username',
        email='email@email.com',
    )
    obj.birthday = birthday
    age = obj.get_age()
    assert age == expected
