from django.db import models
from photo.models.SoftDeleteModel import SoftDeleteModel
from photo.models.User import User
from photo.models.Picture import Picture

class Collection(SoftDeleteModel):
    name = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    pictures = models.ManyToManyField(
        Picture, related_name="collection_pictures", blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="collection_pk")
        ]

    def add_picture(self, picture):
        if picture not in self.pictures.filter(id=picture):
            self.pictures.add(picture)
            self.save()
        return self
