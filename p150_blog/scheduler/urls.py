from django.urls import path
from .views import (
    CalendarView,
    EventView,
    EventListView,
    EventCreateView,
    EventDeleteView,
    EventUpdateView,
    EventCommentDeleteView,
    EventCommentUpdateView
)

urlpatterns = [
    path('', CalendarView.as_view(), name='calendar-home'),
    path('event/', EventListView.as_view(), name='event-home'),
    path('event/<int:pk>/', EventView.as_view(), name='event-detail'),
    path('event/new/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(),
         name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(),
         name='event-delete'),
    path('event/<int:pk_event>/comment/<int:pk_comment>/delete',
         EventCommentDeleteView.as_view(), name='event-comment-delete'),
    path('event/<int:pk_event>/comment/<int:pk_comment>/update',
         EventCommentUpdateView.as_view(), name='event-comment-update')
]
