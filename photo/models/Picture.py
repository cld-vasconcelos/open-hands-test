from django.db import models
from photo.models.SoftDeleteModel import SoftDeleteModel
from photo.models.User import User
from photo.storages_backend import PublicMediaStorage, picture_path

class Picture(SoftDeleteModel):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="picture_user"
    )
    name = models.TextField(blank=True, null=True)
    file = models.ImageField(
        storage=PublicMediaStorage(),
        upload_to=picture_path,
    )
    likes = models.ManyToManyField(User, related_name="picture_likes", blank=True)

    def __str__(self):
        return self.name

    def like_picture(self, user):
        if user not in self.likes.filter(id=user):
            self.likes.add(user)
            self.save()
        return self
