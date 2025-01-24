import graphene
from graphene_django import DjangoObjectType
from .models import Contest, Submission, User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class SubmissionType(DjangoObjectType):
    class Meta:
        model = Submission
        fields = ("id", "user", "contest", "content")

class ContestType(DjangoObjectType):
    class Meta:
        model = Contest
        fields = ("id", "title", "description", "end_date", "winners")

    winners = graphene.List(UserType)

class Query(graphene.ObjectType):
    all_contests = graphene.List(ContestType)
    contest_winners = graphene.List(ContestType)

    def resolve_all_contests(root, info):
        return Contest.objects.all()

    def resolve_contest_winners(root, info):
        return Contest.objects.filter(winners__isnull=False).order_by("-end_date")

schema = graphene.Schema(query=Query)
import strawberry
from strawberry.schema.config import StrawberryConfig

from photo.mutations import Mutation
from photo.queries import Query

schema = strawberry.Schema(
    query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False)
)
