from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, PictureComment, User
from photo.tests.factories import PictureCommentFactory


class PictureCommentTest(TransactionTestCase):
    def setUp(self):
        self.picture_comment = PictureCommentFactory.create()

    def test_factory_create(self):
        self.assertEqual(PictureComment.objects.count(), 1)
        self.assertEqual(PictureComment.objects.first(), self.picture_comment)
        self.assertEqual(Picture.objects.count(), 1)
        self.assertEqual(Picture.objects.first(), self.picture_comment.picture)
        self.assertEqual(User.objects.count(), 2)

    def test_factory_null(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(user=None)
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(picture=None)

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            PictureCommentFactory(id=self.picture_comment.id)

    def test_timestamps(self):
        self.assertIsNotNone(self.picture_comment.created_at)
        self.assertIsNotNone(self.picture_comment.updated_at)
        self.assertTrue(self.picture_comment._meta.get_field('created_at').null)
        self.assertTrue(self.picture_comment._meta.get_field('updated_at').null)
