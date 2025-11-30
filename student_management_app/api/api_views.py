from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from student_management_app.models import (
    CustomUser, Students, Staffs, Subjects, Courses,
    StudentResult
)
import json


# ---------------------------
#   API LOGIN
# ---------------------------
@csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Method not allowed"}, status=400)

    data = json.loads(request.body.decode("utf-8"))
    email = data.get("email")
    password = data.get("password")

    user = authenticate(username=email, password=password)

    if user is None:
        return JsonResponse({"status": False, "message": "Invalid email or password"})

    return JsonResponse({
        "status": True,
        "message": "Login success",
        "user_type": user.user_type,
        "user_id": user.id
    })


# ---------------------------
#   API: LẤY THÔNG TIN USER
# ---------------------------
def api_user_info(request):
    user_id = request.GET.get("user_id")

    try:
        user = CustomUser.objects.get(id=user_id)
    except:
        return JsonResponse({"status": False, "message": "User not found"})

    resp = {
        "status": True,
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "user_type": user.user_type
    }

    return JsonResponse(resp)


# ---------------------------
#   API: LẤY DANH SÁCH MÔN
# ---------------------------
def api_subjects(request):
    subjects = Subjects.objects.all()
    data = []

    for s in subjects:
        data.append({
            "id": s.id,
            "name": s.subject_name,
            "course": s.course_id.course_name,
            "staff_id": s.staff_id.id,
        })

    return JsonResponse({"status": True, "subjects": data})


# ---------------------------
#   API: LẤY DS SINH VIÊN THEO LỚP
# ---------------------------
def api_students_by_course(request):
    course_id = request.GET.get("course_id")

    students = Students.objects.filter(course_id__id=course_id)
    data = []

    for s in students:
        data.append({
            "id": s.id,
            "name": s.admin.username,
            "email": s.admin.email,
            "gender": s.gender,
        })

    return JsonResponse({"status": True, "students": data})


# ---------------------------
#   API: THÊM / SỬA ĐIỂM
# ---------------------------
@csrf_exempt
def api_add_result(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Method not allowed"}, status=400)

    data = json.loads(request.body.decode("utf-8"))

    student_id = data.get("student_id")
    subject_id = data.get("subject_id")
    exam = data.get("exam")
    assignment = data.get("assignment")

    try:
        student = Students.objects.get(id=student_id)
        subject = Subjects.objects.get(id=subject_id)

        result, created = StudentResult.objects.get_or_create(
            student_id=student,
            subject_id=subject
        )

        result.subject_exam_marks = float(exam)
        result.subject_assignment_marks = float(assignment)
        result.save()

        msg = "Created" if created else "Updated"

        return JsonResponse({"status": True, "message": msg})

    except Exception as e:
        return JsonResponse({"status": False, "message": str(e)})


# ---------------------------
#   API: LẤY ĐIỂM SINH VIÊN (nhiều môn)
# ---------------------------
def api_student_results(request):
    student_id = request.GET.get("student_id")

    results = StudentResult.objects.filter(student_id__id=student_id)

    data = []
    for r in results:
        data.append({
            "subject": r.subject_id.subject_name,
            "exam": r.subject_exam_marks,
            "assignment": r.subject_assignment_marks,
            "total": r.subject_exam_marks + r.subject_assignment_marks
        })

    return JsonResponse({"status": True, "results": data})


# ---------------------------
#   API: SẮP XẾP ĐIỂM (LOW → HIGH)
# ---------------------------
def api_sort_results(request):
    student_id = request.GET.get("student_id")

    results = StudentResult.objects.filter(
        student_id__id=student_id
    ).order_by("subject_exam_marks")

    data = []
    for r in results:
        data.append({
            "subject": r.subject_id.subject_name,
            "exam": r.subject_exam_marks,
            "assignment": r.subject_assignment_marks,
            "total": r.subject_exam_marks + r.subject_assignment_marks
        })

    return JsonResponse({"status": True, "sorted_results": data})
