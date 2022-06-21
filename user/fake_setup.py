import random

from django.db import transaction
from django.core.management.base import BaseCommand
from .models import Profile, Tweet, Comment
from .models import (FakeProfile, FakeTweet, FakeComment)


NUM_USER = 10
NUM_TWEETS = 20
COMMENT_PER_TWEET = 3
REPLY_PER_COMMENT = 3


# Need modification for generating fake data
class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Thread, Comment, Club]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")
        people = []
        for _ in range(NUM_USERS):
            person = UserFactory()
            people.append(person)

        # Add some users to clubs
        for _ in range(NUM_CLUBS):
            club = ClubFactory()
            members = random.choices(
                people,
                k=USERS_PER_CLUB
            )
            club.user.add(*members)

        # Create all the threads
        for _ in range(NUM_THREADS):
            creator = random.choice(people)
            thread = ThreadFactory(creator=creator)
            # Create comments for each thread
            for _ in range(COMMENTS_PER_THREAD):
                commentor = random.choice(people)
                CommentFactory(
                    user=commentor,
                    thread=thread
                )
