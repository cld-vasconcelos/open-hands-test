from django.test import TestCase
from photo.models import User, Picture, PictureComment, Collection, Contest, ContestSubmission

class TimestampedFieldsTest(TestCase):
    def test_user_model_has_timestamped_fields(self):
        user = User.objects.create(email='test@example.com')
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_picture_model_has_timestamped_fields(self):
        user = User.objects.create(email='test@example.com')
        picture = Picture.objects.create(user=user)
        self.assertIsNotNone(picture.created_at)
        self.assertIsNotNone(picture.updated_at)

    def test_picture_comment_model_has_timestamped_fields(self):
        user = User.objects.create(email='test@example.com')
        picture = Picture.objects.create(user=user)
        comment = PictureComment.objects.create(user=user, picture=picture, text='Nice photo!')
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)

    def test_collection_model_has_timestamped_fields(self):
        user = User.objects.create(email='test@example.com')
        collection = Collection.objects.create(name='My Collection', user=user)
        self.assertIsNotNone(collection.created_at)
        self.assertIsNotNone(collection.updated_at)

    def test_contest_model_has_timestamped_fields(self):
        contest = Contest.objects.create(title='Photo Contest', description='A fun contest')
        self.assertIsNotNone(contest.created_at)
        self.assertIsNotNone(contest.updated_at)

    def test_contest_submission_model_has_timestamped_fields(self):
        user = User.objects.create(email='test@example.com')
        picture = Picture.objects.create(user=user)
        contest = Contest.objects.create(title='Photo Contest', description='A fun contest')
        submission = ContestSubmission.objects.create(contest=contest, picture=picture)
        self.assertIsNotNone(submission.created_at)
        self.assertIsNotNone(submission.updated_at)
