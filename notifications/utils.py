from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import Notification


def create_notification(recipient, actor, verb, target, notification_type):
    if recipient == actor:
        return None

    content_type = ContentType.objects.get_for_model(target)

    # Prevent duplicate spam notifications
    time_threshold = timezone.now() - timedelta(minutes=5)

    existing = Notification.objects.filter(
        recipient=recipient,
        actor=actor,
        content_type=content_type,
        object_id=target.id,
        notification_type=notification_type,
        created_at__gte=time_threshold
    ).first()

    if existing:
        return existing

    return Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        content_type=content_type,
        object_id=target.id,
        notification_type=notification_type
    )


#
# def create_notification(recipient, actor, verb, target, notification_type):
#     if recipient == actor:
#         return  # O‘zi o‘ziga notification yubormasin
#
#     Notification.objects.create(
#         recipient=recipient,
#         actor=actor,
#         verb=verb,
#         notification_type=notification_type,
#         content_type=ContentType.objects.get_for_model(target),
#         object_id=target.id
#     )