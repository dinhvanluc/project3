from django.urls import path
from . import api_views

urlpatterns = [
    path("auth/login/", api_views.api_login),
    path("auth/me/", api_views.api_user_info),

    path("subjects/", api_views.api_subjects),
    path("students/", api_views.api_students_by_course),

    path("result/add/", api_views.api_add_result),
    path("result/student/", api_views.api_student_results),
    path("result/sort/", api_views.api_sort_results),
]
