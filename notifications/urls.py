from django.urls import path
from . import views


urlpatterns = [
    path('api/list/', views.notification_list, name='list'),
    path('api/<int:notification_id>/read/', views.mark_as_read, name='mark_read'),
    path('api/read-all/', views.mark_all_read, name='mark_all_read'),

]