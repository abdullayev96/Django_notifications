from django.db import models
from notifications.models import User
from notifications.utils import create_notification


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            create_notification(
                recipient=self.following,
                actor=self.follower,
                verb=f"started following you",
                target=self.follower,
                notification_type='follow'
            )
