from factory.django import DjangoModelFactory
from .models import Profile, Tweet, Comment

class FakeProfile(DjangoModelFactory):
    class Meta:
        model = Profile
    
    name = factory.Faker("name")
    lastname = factory.Faker("lastname")

class FakeTweet(DjangoModelFactory):
    class Meta:
        model = Tweet

    author = factory.SubFactory(FakeProfile):
    content = factory.Faker("content")

class FakeComment(DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(FakeProfile)
    tweet = factory.SubFactory(FakeTweet)
    content = factory.Faker("content")


