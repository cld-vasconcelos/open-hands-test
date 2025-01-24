from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from photo.models import Picture, User

class PhotoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com", username="testuser")
        self.client = Client()
        self.client.force_login(self.user)

    def test_picture_creation(self):
        picture = Picture.objects.create(
            user=self.user, name="Test Picture", file=SimpleUploadedFile("test.jpg", b"file_content")
        )
        self.assertEqual(picture.name, "Test Picture")
        self.assertEqual(picture.user, self.user)
def test_picture_model_has_timestamps(self):
        picture = Picture.objects.create(
            user=self.user, name="Test Picture", file=SimpleUploadedFile("test.jpg", b"file_content")
        )
        self.assertIsNotNone(picture.created_at)
        self.assertIsNotNone(picture.updated_at)
