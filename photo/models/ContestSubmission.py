from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from photo.models.SoftDeleteModel import SoftDeleteModel
from photo.models.User import User
from photo.models.Picture import Picture
from photo.models.Contest import Contest
from photo.fixtures import (
    OUTDATED_SUBMISSION_ERROR_MESSAGE,
    REPEATED_VOTE_ERROR_MESSAGE,
    UNIQUE_SUBMISSION_ERROR_MESSAGE,
    CANT_VOTE_SUBMISSION,
    CONTEST_CLOSED,
    VOTE_UPLOAD_PHASE_NOT_OVER,
    VOTING_DRAW_PHASE_OVER,
    VOTING_PHASE_OVER,
    VOTING_SELF,
)
from utils.enums import ContestInternalStates

class ContestSubmission(SoftDeleteModel):
    contest = models.ForeignKey(
        "Contest",
        on_delete=models.CASCADE,
    )
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name="submission_votes", blank=True)

    def validate_unique(self, *args, **kwargs):
        qs = ContestSubmission.objects.filter(
            contest=self.contest, picture__user=self.picture.user
        )

        if qs.exists() and self._state.adding:
            raise ValidationError(UNIQUE_SUBMISSION_ERROR_MESSAGE)

    def validate_vote(self):
        user_vote = ContestSubmission.objects.filter(
            contest=self.contest, votes=self.picture.user
        )

        if user_vote.exists() and self._state.adding:
            raise ValidationError(REPEATED_VOTE_ERROR_MESSAGE)

    def validate_submission_date(self):
        submission_date = (
            self.submission_date if self.submission_date else timezone.now()
        )
        if self.contest.upload_phase_end is not None and (
            not (
                self.contest.upload_phase_start
                <= submission_date
                <= self.contest.upload_phase_end
            )
        ):
            raise ValidationError(OUTDATED_SUBMISSION_ERROR_MESSAGE)

    def save(self, *args, **kwargs):
        self.validate_unique()
        if self._state.adding:
            self.validate_submission_date()
        super(ContestSubmission, self).save(*args, **kwargs)

    def add_vote(self, user):
        contest_submissions = ContestSubmission.objects.filter(contest=self.contest)
        user_vote = User.objects.filter(id=user).first()

        if self.picture.user.id == user_vote.id:
            raise ValidationError(VOTING_SELF)

        if self.contest.internal_status == ContestInternalStates.CLOSED:
            raise ValidationError(CONTEST_CLOSED)

        if self.contest.internal_status == ContestInternalStates.DRAW:
            if self.contest.voting_draw_end < timezone.now():
                raise ValidationError(VOTING_DRAW_PHASE_OVER)
            if self.picture.user not in self.contest.winners.all():
                raise ValidationError(CANT_VOTE_SUBMISSION)
        else:
            if (
                self.contest.upload_phase_end
                and self.contest.upload_phase_end > timezone.now()
            ):
                raise ValidationError(VOTE_UPLOAD_PHASE_NOT_OVER)
            if (
                self.contest.voting_phase_end
                and self.contest.voting_phase_end < timezone.now()
            ):
                raise ValidationError(VOTING_PHASE_OVER)

        for sub in contest_submissions:
            if user_vote in sub.votes.all():
                sub.votes.remove(user_vote)
        self.votes.add(user)
        self.save()
        return self
