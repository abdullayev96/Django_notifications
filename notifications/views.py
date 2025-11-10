from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Notification
from django.db.models import Prefetch
from blog.models import Post

@login_required
@require_http_methods(["POST"])
def mark_as_read(request, notification_id):
    """Mark a single notification as read."""
    try:
        notification = Notification.objects.get(
            id=notification_id,
            recipient=request.user
        )
        notification.is_read = True
        notification.save()

        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


@login_required
@require_http_methods(["POST"])
def mark_all_read(request):
    """Mark all notifications as read."""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        'success': True,
        'count': count
    })


@login_required
@require_http_methods(["GET"])
def notification_list(request):
    """Return unread notifications for current user."""
    # notifications = Notification.objects.filter(
    #     recipient=request.user,
    #     is_read=False
    # ).select_related('actor', 'content_type')[:20]

    notifications = Notification.objects.filter(
        recipient=request.user, is_read=False).select_related(
        'actor',  # ForeignKey - use select_related
        'content_type'
    ).prefetch_related(
        # Prefetch the actual objects
        Prefetch(
            'content_type__model_class',
            queryset=Post.objects.all()
        )
    )[:20]

    data = {
        'count': notifications.count(),
        'notifications': [
            {
                'id': n.id,
                'actor': {
                    'username': n.actor.username,
                    'avatar': n.actor.profile.avatar.url if hasattr(n.actor, 'profile') else None
                },
                'verb': n.verb,
                'type': n.notification_type,
                'created_at': n.created_at.isoformat(),
                'url': get_notification_url(n),
            }
            for n in notifications
        ]
    }

    return JsonResponse(data)


def get_notification_url(notification):
    """Generate URL based on notification type."""
    if notification.notification_type in ['like', 'comment']:
        return f"/posts/{notification.object_id}/"
    elif notification.notification_type == 'follow':
        return f"/profile/{notification.actor.username}/"
    return "/"