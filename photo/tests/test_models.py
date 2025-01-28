from django.test import TestCase
from django.utils import timezone
from photo.models import User, Picture, PictureComment, Collection, Contest, ContestSubmission


class TimestampedModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.picture = Picture.objects.create(user=self.user)
        self.comment = PictureComment.objects.create(user=self.user, picture=self.picture, text="Nice photo!")
        self.collection = Collection.objects.create(name="My Collection", user=self.user)
        self.contest = Contest.objects.create(title="Photo Contest", description="A test contest", created_by=self.user)
        self.submission = ContestSubmission.objects.create(contest=self.contest, picture=self.picture)

    def test_user_timestamps(self):
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

    def test_picture_timestamps(self):
        self.assertIsNotNone(self.picture.created_at)
        self.assertIsNotNone(self.picture.updated_at)

    def test_comment_timestamps(self):
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)

    def test_collection_timestamps(self):
        self.assertIsNotNone(self.collection.created_at)
        self.assertIsNotNone(self.collection.updated_at)

    def test_contest_timestamps(self):
        self.assertIsNotNone(self.contest.created_at)
        self.assertIsNotNone(self.contest.updated_at)

    def test_submission_timestamps(self):
        self.assertIsNotNone(self.submission.created_at)
        self.assertIsNotNone(self.submission.updated_at)
