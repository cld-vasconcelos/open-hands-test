import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from photo.models.UserManager import UserManager
from photo.models.SoftDeleteModel import SoftDeleteModel

class User(AbstractUser, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.TextField(unique=True)
    username = models.CharField("username", max_length=150, null=True)
    name_first = models.TextField(blank=True, null=True)
    name_last = models.TextField(blank=True, null=True)
    profile_picture = models.ForeignKey(
        "Picture",
        on_delete=models.SET_NULL,
        related_name="user_picture",
        blank=True,
        null=True,
    )
    profile_picture_updated_at = models.DateTimeField(blank=True, null=True)
    user_handle = models.TextField(unique=True, null=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_deleted="False"),
                name="user_email",
            )
        ]

    def validate_profile_picture(self):
        if not self._state.adding:
            old_picture = User.objects.filter(email=self.email).first().profile_picture
            if old_picture and self.profile_picture.id != old_picture.id:
                self.profile_picture_updated_at = timezone.now()
        if self.profile_picture and self.profile_picture.user.email != self.email:
            raise ValidationError(
                "The user's profile picture must be owned by the same user."
            )

    def save(self, *args, **kwargs):
        self.validate_profile_picture()
        super(User, self).save(*args, **kwargs)
