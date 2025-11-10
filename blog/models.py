from django.db import models
from notifications.utils import create_notification
from notifications.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def add_like(self, user):
        like, created = Like.objects.get_or_create(
            post=self,
            user=user
        )
        if created:
            # Create notification
            create_notification(
                recipient=self.author,
                actor=user,
                verb=f"liked your post '{self.title}'",
                target=self,
                notification_type='like'
            )

        return like


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Notify post author
            create_notification(
                recipient=self.post.author,
                actor=self.author,
                verb=f"commented on your post '{self.post.title}'",
                target=self.post,
                notification_type='comment'
            )
