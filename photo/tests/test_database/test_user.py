from django.db import IntegrityError
from django.test import TransactionTestCase

from photo.models import Picture, User
from photo.tests.factories import UserFactory


class UserTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_factory(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), self.user)
        self.assertEqual(Picture.objects.count(), 1)

    def test_integity(self):
        self.assertEqual(
            User.objects.first().email, User.objects.first().profile_picture.user.email
        )
        self.assertEqual(
            Picture.objects.first().file,
            User.objects.first().profile_picture.file,
        )

    def test_factory_pk(self):
        with self.assertRaises(IntegrityError):
            UserFactory(id=self.user.id)

    def test_created_at(self):
        self.assertIsNotNone(self.user.created_at)

    def test_updated_at(self):
        old_updated_at = self.user.updated_at
        self.user.name_first = "Updated Name"
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)
