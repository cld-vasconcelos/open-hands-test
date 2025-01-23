import uuid
from random import shuffle
from typing import List, Optional

import strawberry
import strawberry_django
from django.contrib.postgres.search import SearchVector
from rest_framework.authentication import TokenAuthentication
from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from photo.filters import (
    CollectionFilter,
    ContestFilter,
    ContestSubmissionFilter,
    PictureCommentFilter,
    PictureFilter,
)
from photo.models import (
    Collection,
    Contest,
    ContestSubmission,
    Picture,
    PictureComment,
    User,
)
from photo.permissions import IsAuthenticated
from photo.types import (
    CollectionType,
    ContestSubmissionType,
    ContestType,
    PictureCommentType,
    PictureType,
    UserType,
)
from utils.enums import ContestInternalStates


class Context(BaseContext):
    def user(self) -> User | None:
        if not self.request:
            return None
        authenticator = TokenAuthentication()
        return authenticator.authenticate(self.request)


Info = _Info[Context, RootValueType]


@strawberry.type
class Query:
    @strawberry.field
    def users(self, user: uuid.UUID = None) -> List[UserType]:
        return User.objects.filter(id=user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def get_authenticated_user(self, info: Info) -> UserType | None:
        return info.context.user()

    @strawberry.field
    def pictures(
        self, filters: Optional[PictureFilter] = strawberry.UNSET
    ) -> List[PictureType]:
        queryset = Picture.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def picture_comments(
        self, filters: Optional[PictureCommentFilter] = strawberry.UNSET
    ) -> List[PictureCommentType]:
        queryset = PictureComment.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def collections(
        self, filters: Optional[CollectionFilter] = strawberry.UNSET
    ) -> List[CollectionType]:
        queryset = Collection.objects.all()
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def contests(
        self, filters: Optional[ContestFilter] = strawberry.UNSET
    ) -> List[ContestType]:
        queryset = Contest.objects.all().exclude(
            internal_status=ContestInternalStates.DRAW, voting_draw_end=None
        )
        if getattr(filters, "search", strawberry.UNSET):
            queryset = Contest.objects.annotate(
                search=SearchVector("title", "description", "prize"),
            ).filter(search__icontains=filters.search)
        return strawberry_django.filters.apply(filters, queryset)

    @strawberry.field
    def contest_submissions(
        self,
        filters: Optional[ContestSubmissionFilter] = strawberry.UNSET,
        order: Optional[List[int]] = None,
    ) -> List[ContestSubmissionType]:
        queryset = ContestSubmission.objects.all()

        def set_order(element):
            return order.index(element.id)

        contest = None
        if filters and filters.contest:
            contest = Contest.objects.filter(id=filters.contest.id).first()

        if filters and filters.draw:
            contest = Contest.objects.filter(
                id=filters.contest.id, internal_status=ContestInternalStates.DRAW
            ).first()
            contest_winners = [user.id for user in contest.winners.all()]
            queryset = ContestSubmission.objects.filter(
                picture__user__id__in=contest_winners
            )

        query_results = list(strawberry_django.filters.apply(filters, queryset))

        if contest and contest.internal_status == ContestInternalStates.CLOSED:
            winner = [user.id for user in contest.winners.all()][0]
            winner_submission = ContestSubmission.objects.filter(
                picture__user__id=winner
            ).first()
            query_results.remove(winner_submission)
            query_results = [winner_submission] + query_results
        elif not order:
            shuffle(query_results)
        else:
            query_results.sort(key=set_order)
        return query_results

    @strawberry.field
    def winners(self) -> List[ContestType]:
        contests_with_winners = Contest.objects.filter(winners__isnull=False).distinct()
        contests_with_winners = contests_with_winners.order_by('-voting_phase_end')
        return [
            ContestType(
                id=contest.id,
                title=contest.title,
                description=contest.description,
                cover_picture=contest.cover_picture,
                prize=contest.prize,
                upload_phase_start=contest.upload_phase_start,
                upload_phase_end=contest.upload_phase_end,
                voting_phase_end=contest.voting_phase_end,
                voting_draw_end=contest.voting_draw_end,
                internal_status=contest.internal_status,
                winners=[
                    ContestSubmissionType(
                        id=submission.id,
                        contest=submission.contest,
                        picture=submission.picture,
                        submission_date=submission.submission_date,
                        votes=submission.votes.all()
                    )
                    for submission in ContestSubmission.objects.filter(contest=contest, picture__user__in=contest.winners.all())
                ]
            )
            for contest in contests_with_winners
        ]
