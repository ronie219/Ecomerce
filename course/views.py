from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from Membership.models import UserMembership
from course.models import Course, Lesson


class courseListView(ListView):
    model = Course


class courseDetailView(DetailView):
    model = Course


class lessonDetailView(View):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()
        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        context = {
            'lesson': None
        }
        user_membership = UserMembership.objects.filter(user=request.user).first()
        user_membership_type = user_membership.membership.membership_type
        course_allowed_membership = course.allowed_membership.all()

        if course_allowed_membership.filter(membership_type=user_membership_type).exists():
            context = {
                'lesson': lesson
            }
        return render(request, 'course/lesson_detail.html', context)
