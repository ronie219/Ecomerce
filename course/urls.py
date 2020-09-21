from django.urls import path
from .views import courseDetailView, courseListView, lessonDetailView
app_name = 'course'

urlpatterns = [
    path('', courseListView.as_view(), name='list'),
    path('<slug>', courseDetailView.as_view(), name='detail'),
    path('<course_slug>/<lesson_slug>', lessonDetailView.as_view(), name='lesson_detail')
]
