import random

from django.core.management import BaseCommand

from authentication.models import User

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
           "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2",
           "3", "4", "5", "6", "7", "8", "9"]
company = ["@gmail.com", "@naver.com", "@daum.com", "@kakao.com", "@kaist.ac.kr", "@abc.ac.kr", "@yahoo.com"]


def username_random_generator() -> str:
    global letters

    user_name = "".join(random.sample(letters, 20))

    return user_name


def email_random_generator() -> str:
    global letters, company

    front = "".join(random.sample(letters, 10))
    back = random.choice(company)
    return front + back


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_cnt = 50000

        for i in range(0, user_cnt, 100):
            User.objects.bulk_create(
                [
                    User(
                        email=email_random_generator(),
                        username=username_random_generator(),
                        is_active=random.choice([True, False]),
                        is_verified=random.choice([True, False])
                    ) for j in range(1, 101)
                ]
            )
