from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import Count, Max
from photo.models.soft_delete_model import SoftDeleteModel
from photo.models.user import User
from photo.models.picture import Picture
from utils.enums import ContestInternalStates
from photo.fixtures import (
    CANT_VOTE_SUBMISSION,
    CONTEST_CLOSED,
    OUTDATED_SUBMISSION_ERROR_MESSAGE,
    REPEATED_VOTE_ERROR_MESSAGE,
    UNIQUE_SUBMISSION_ERROR_MESSAGE,
    VALID_USER_ERROR_MESSAGE,
    VOTE_UPLOAD_PHASE_NOT_OVER,
    VOTING_DRAW_PHASE_OVER,
    VOTING_PHASE_OVER,
    VOTING_SELF,
)


class Contest(SoftDeleteModel):
    title = models.TextField()
    description = models.TextField()
    cover_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    prize = models.TextField(null=True, blank=True)
    automated_dates = models.BooleanField(default=True)
    upload_phase_start = models.DateTimeField(default=timezone.now)
    upload_phase_end = models.DateTimeField(null=True, blank=True)
    voting_phase_end = models.DateTimeField(null=True, blank=True)
    voting_draw_end = models.DateTimeField(null=True, blank=True)
    internal_status = models.TextField(
        choices=ContestInternalStates.choices, default=ContestInternalStates.OPEN
    )
    winners = models.ManyToManyField(User, related_name="contest_winners", blank=True)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        related_name="contest_created_by",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def validate_user(self):
        if not (
            self.created_by
            and User.objects.filter(email=self.created_by.email).exists()
        ):
            raise ValidationError(VALID_USER_ERROR_MESSAGE)

    def reset_votes(self):
        for submission in ContestSubmission.objects.filter(contest=self):
            submission.votes.clear()

    def close_contest(self):
        self.voting_phase_end = timezone.now()
        max_votes = ContestSubmission.objects.annotate(
            num_votes=Count("votes")
        ).aggregate(max_votes=Max("num_votes"))["max_votes"]
        submissions_with_highest_votes = ContestSubmission.objects.annotate(
            num_votes=Count("votes")
        ).filter(num_votes=max_votes, contest=self)

        if self.internal_status == ContestInternalStates.DRAW:
            self.winners.clear()
        for submission in submissions_with_highest_votes:
            self.winners.add(submission.picture.user)

        if self.winners.count() > 1:
            self.internal_status = ContestInternalStates.DRAW
            self.reset_votes()
        elif self.winners.count() == 0:
            self.internal_status = ContestInternalStates.DRAW
            all_submissions = ContestSubmission.objects.filter(contest=self)
            for submission in all_submissions:
                self.winners.add(submission.picture.user)
            self.reset_votes()
        else:
            self.internal_status = ContestInternalStates.CLOSED
        self.save()
        return self

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.validate_user()
        super(Contest, self).save(*args, **kwargs)
