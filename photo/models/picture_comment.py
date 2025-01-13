from django.db import models
from photo.models.soft_delete_model import SoftDeleteModel
from photo.models.user import User
from photo.models.picture import Picture


class PictureComment(SoftDeleteModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    picture = models.ForeignKey(
        "Picture",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
