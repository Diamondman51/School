from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import Group as GroupType

from teacher.forms import AddCourseForm, AddDepartmentForm, AddLessonForm, AddProfessorForm, AddSkillForm, EditLessonForm, EditProfessorForm, AddStudentForm, EditSkillForm, EditStudentForm, StudentsAttendanceFormSet
from teacher.models import Group, GroupLikes, GroupSpec, Lesson, LessonFiles, Score_Attendance, Skill, Student, Teacher

# Create your views here.


User = get_user_model()


class AllProfessorsViewset(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        """
        Renders a page with a list of all professors.

        :param request: Request object
        :return: TemplateResponse object
        """
        teachers = User.objects.filter(groups=GroupType.objects.get(name='Teacher'))
        context = {"teachers": teachers}
        return TemplateResponse(request, 'all-professors.html', context)


class AddProfessorViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.add_teacher'
    
    def get(self, request):
        """
        Renders a page with a form to add a new professor.

        :param request: Request object
        :return: TemplateResponse object
        """
        form = AddProfessorForm()
        context = {
            'form': form,
        }
        return TemplateResponse(request, "add-professor.html", context)
    
    def post(self, request):
        
        """
        Handles the POST request of adding a new professor.

        Checks if the form is valid, if so it saves the form and redirects to the all professors page.
        If the form is not valid, it renders the same page with the form errors displayed.

        :param request: Request object
        :return: TemplateResponse object
        """
        form = AddProfessorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("all_professors")
        context = {'form': form}
        print(form.errors)
        print(form.data)
        return TemplateResponse(request, "add-professor.html", context)


class EditProfessorViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.change_teacher'

    def get(self, request, professor_id):
        """
        Renders a page with a form to edit an existing professor.

        :param request: Request object
        :param professor_id: int, the id of the professor to edit
        :return: TemplateResponse object
        """
        teacher = get_object_or_404(User, id=professor_id)
        form = EditProfessorForm(instance=teacher)
        context = {
            'form': form,
            "teacher": teacher,
        }
        # print(form.as_p())
        print('caafaw ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd  ')
        return TemplateResponse(request, 'edit-professor.html', context)
    
    def post(self, request, professor_id):
        
        """
        Handles the POST request of editing an existing professor.

        Checks if the form is valid, if so it saves the form and redirects to the all professors page.
        If the form is not valid, it renders the same page with the form errors displayed.

        :param request: Request object
        :param professor_id: int, the id of the professor to edit
        :return: TemplateResponse object
        """
        teacher = get_object_or_404(User, id=professor_id)
        form = EditProfessorForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('all_professors')
        context = {
            'form': form,
            'teacher': teacher,
        }
        print(form.errors)
        return TemplateResponse(request, "edit-professor.html", context)


class ProfessorProfileViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, professor_id):
        """
        Handles the GET request of the professor profile page.

        Retrieves the professor with the given id and renders the professor profile page.

        :param request: Request object
        :param professor_id: int, the id of the professor
        :return: TemplateResponse object
        """
        professor = get_object_or_404(User, id=professor_id)
        context = {
            'professor': professor,
        }
        return TemplateResponse(request, 'professor-profile.html', context)


class DeleteProfessorViewset(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = 'login'
    permission_required = ["teacher.delete_teacher"]

    def get(self, request, professor_id=None):
        """
        Handles the GET request of the delete professor page.

        Retrieves the professor with the given id, deletes it and redirects to the previous page.

        :param request: Request object
        :param professor_id: int, the id of the professor to delete
        :return: HttpResponseRedirect object
        """
        if professor_id:
            teacher = get_object_or_404(User, id=professor_id)
            teacher.delete()
            # professor_id += 1
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))
            # return HttpResponseRedirect(request.path_info) # Does not work properly


class AllStudentsViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        # print(type(GroupType(request.user.groups.all())), GroupType(request.user.groups.all()), ''.join([group.name for group in request.user.groups.all()]) == GroupType.objects.get(name="Teacher"), GroupType.objects.get(name="Teacher"), type(GroupType.objects.get(name="Teacher")), 'User groups ===============================')
        # print([group.name for group in request.user.groups.all()])
        """
        Handles the GET request of the all students page.

        Retrieves all students, either of the teacher that is logged in or of all students if the user is a manager.

        :param request: Request object
        :return: TemplateResponse object
        """
        if 'Teacher' in [group.name for group in request.user.groups.all()]:
            students = Student.objects.filter(group__teacher__first_name=request.user.first_name)
        else:
            print("Manger ================================")
            students = Student.objects.all()

        context = {
            "students": students,
        }
        return TemplateResponse(request, 'all-students.html',context)


class AddStudentViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.add_student'

    def get(self, request):
        """
        Handles the GET request of the add student page.

        Retrieves an empty form to add a new student.

        :param request: Request object
        :return: TemplateResponse object
        """
        form = AddStudentForm()
        context = {
            'form': form,
        }
        return TemplateResponse(request, "add-student.html",context)

    def post(self, request,):
        '''
        Handles the POST request of the add student page.

        Checks if the form is valid, if so it saves the form and redirects to the all students page.
        If the form is not valid, it renders the same page with the form errors displayed.

        :param request: Request object
        :return: TemplateResponse object
        '''
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("all_students")
        context = {'form': form}
        print(form.errors)
        return TemplateResponse(request, "add-student.html", context)
    

class EditStudentViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.change_student'

    def get(self, request,student_id):
        """
        Handles the GET request of the edit student page.

        Retrieves the student with the given student_id and an empty form to edit the student.

        :param request: Request object
        :param student_id: The id of the student to edit
        :return: TemplateResponse object
        """
        student = get_object_or_404(Student, id=student_id)
        form = EditStudentForm(instance=student)
        context = {
            "form":form,
            "student":student,
        }
        return TemplateResponse(request, 'edit-student.html',context)

    def post(self, request, student_id):
        """
        Handles the POST request of the edit student page.

        Retrieves the student with the given student_id, updates the student with the data from the form, and saves the student.

        If the form is valid, it redirects to the all students page, otherwise it renders the same page with the form errors displayed.

        :param request: Request object
        :param student_id: The id of the student to edit
        :return: TemplateResponse object
        """
        student = get_object_or_404(Student, id=student_id)
        form = EditStudentForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            return redirect('all_students')
        form.group = student.group
        print(form.errors)
        context = {
            "form": form,
            "student":student,
        }
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",form.errors)
        return TemplateResponse(request, 'edit-student.html',context)
    

class DeleteStudentViewset(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = 'login'
    permission_required = ['teacher.delete_student']

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        return redirect("all_students")


class StudentProfileViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        context = {
            "student":student,
        }
        return TemplateResponse(request, 'about-student.html',context)


class AllCoursesViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        # print([group.name for group in request.user.groups.all()])
        if 'Teacher' in [group.name for group in request.user.groups.all()]:
            courses = Group.objects.filter(teacher__id=request.user.id)
        elif request.user.is_admin:
            courses = Group.objects.all()
        else:
            courses = None
        context = {
            "courses": courses
            }
        return TemplateResponse(request, 'all-courses.html', context)


class AddCoursesViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.add_course'

    def get(self, request):
        form = AddCourseForm()
        context = {
            "form": form
            }
        return TemplateResponse(request, 'add-courses.html', context)
    
    def post(self, request):
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("all_courses")
        context = {
            'form': form
        }
        print(form.errors)
        print(form.data)
        return TemplateResponse(request, "add-courses.html", context)
        

class EditCoursesViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.edit_course'

    def get(self, request, course_id):
        course = get_object_or_404(Group, id=course_id)
        form = AddCourseForm(instance=course)
        context = {
            'form': form,
            'course': course
        }
        return TemplateResponse(request, 'edit-courses.html', context)
    
    def post(self, request, course_id):
        course = get_object_or_404(Group, id=course_id)
        form = AddCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('all_courses')
        context = {
            'form': form,
            'course': course
        }
        print(form.errors)
        print(form.data)
        return TemplateResponse(request, 'edit-courses.html', context)


class DeleteCoursesViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.delete_course'

    def get(self, request, course_id):
        course = get_object_or_404(Group, id=course_id)
        course.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))


class AllLessonsViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.view_lesson'
    def get(self, request):
        if 'Teacher' in [group.name for group in request.user.groups.all()]:
            lessons = Lesson.objects.filter(group__teacher__first_name=request.user.first_name)
        else:
            lessons = Lesson.objects.all()
        context = {
            'lessons': lessons
        }
        return TemplateResponse(request, 'all-lessons.html', context)
    

class AddLessonViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.add_lesson'

    def get(self, request):
        form = AddLessonForm()
        context = {
            'form': form
        }
        return TemplateResponse(request, 'add-lesson.html', context)

    def post(self, request):
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            files = request.FILES.getlist("files", None)
            if files:
                for file in files:
                    LessonFiles.objects.create(
                        file=file,
                        lesson=lesson
                    )
            return redirect('all_lessons')

        context = {
            "form": form
        }
        return TemplateResponse(request, 'add-lesson.html', context)


class EditLessonViewset(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = 'login'
    permission_required = ''

    def get(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        files = LessonFiles.objects.filter(lesson=lesson)
        form = EditLessonForm(instance=lesson)
        # print(files)
        context = {
            'form': form,
            'files': files,
            'lesson': lesson,
        }
        return TemplateResponse(request, 'edit-lesson.html', context)

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        form = EditLessonForm(request.POST, instance=lesson)
        print('--------------------------------------------')
        print(form)
        print('--------------------------------------------')

        if form.is_valid():
            lesson = form.save()
            # old_files = LessonFiles.objects.filter(lesson=lesson)
            # old_files.delete()
            files = request.FILES.getlist('files', None)
            if files:
                for file in files:
                    LessonFiles.objects.create(
                        lesson=lesson,
                        file=file,
                    )
            return redirect('all_lessons')
        files = LessonFiles.objects.filter(lesson=lesson)
        context = {
            "form": form,
            'files': files,
            'lesson': lesson,
        }
        return TemplateResponse(request, 'edit-lesson.html', context)


def delete_lesson_file(request, lesson_file_id):
    print("+++++++++++++++++++++++++++++++++++++++++++")
    lesson_file = get_object_or_404(LessonFiles, id=lesson_file_id)
    lesson_id = lesson_file.lesson.id
    lesson_file.file.delete()
    # os.pa
    lesson_file.delete()
    return redirect("edit_lesson", lesson_id=lesson_id)


class AboutCoursesViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, course_id):
        course = get_object_or_404(Group, id=course_id)
        courses = Group.objects.all().exclude(id=course_id)
        print(course.duration)
        context = {
            'course': course,
            'courses': courses
        }
        return TemplateResponse(request, 'about-courses.html', context)


class ViewCoursesViewset(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, course_id):
        course = Group.objects.get(id=course_id)
        lessons = Lesson.objects.filter(group=course)
        context = {
            'lessons': lessons
        }
        return TemplateResponse(request, "view-lessons.html", context)
    

class Attendance(LoginRequiredMixin, View):
    # permission_required = 'teacher.change_score_attendance'
    login_url = "login"
    def get(self, request, lesson_id):
        print('88888888888888888888888888888888888888888888888888')
        print(request.user.get_all_permissions())
        print('88888888888888888888888888888888888888888888888888')
        lesson = Lesson.objects.get(id=lesson_id)
        group = lesson.group
        students = group.student_set.all()
        print(students)
        print(lesson.score_attendance_set.filter(lesson=lesson, student__in=students))
        print('88888888888888888888888888888888888888888888888888')
        
        # if not lesson.score_attendance_set.filter(lesson=lesson, student__in=students):
        Score_Attendance.objects.bulk_create(
            Score_Attendance(lesson=lesson, student=student) for student in students
            if not Score_Attendance.objects.filter(lesson=lesson, student=student).exists()
        )
        # formset = StudentsAttendanceFormSet(queryset=Score_Attendance.objects.filter(
        #     created_at__exact=datetime.date.today())
        # )
        # for att in Score_Attendance.objects.filter(lesson)
        formset = StudentsAttendanceFormSet(queryset=Score_Attendance.objects.filter(lesson=lesson, student__in=students))
        print(lesson.score_attendance_set.filter(lesson=lesson, student__in=students))
        context = {
            'formset': formset,
            'lesson': lesson,
            'group': group
        }
        return TemplateResponse(request, "yoqlama.html", context)

    def post(self, request, lesson_id):
        lesson = Lesson.objects.get(id=lesson_id)
        group = lesson.group
        students = group.student_set.all()
        queryset = Score_Attendance.objects.filter(lesson=lesson, student__in=students)
        formset = StudentsAttendanceFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            # print("//////////////////////////////////////////////")
            # print(formset)
            # print("//////////////////////////////////////////////")
            instances = formset.save(commit=False)

            for form, student in zip(instances, students):
                form.lesson = lesson
                form.student = student
                form.save()

            return redirect('view_course', group.id)
        
        for form, student in zip(formset.forms, students):
            form.instance.student = student

        context = {
            'formset': formset,
            'lesson': lesson,
            'group': group
        }
        print(queryset)
        # print(formset)
        print(formset.errors)
        return TemplateResponse(request, 'yoqlama.html', context)


class AllDepartmentViewset(View):

    def get(self, request):
        departments = GroupSpec.objects.all()
        context = {
            "departments": departments
            }
        return TemplateResponse(request, 'all-departments.html', context)


class AddDepartmentViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ["teacher.add_department"]
    login_url = 'login'
    def get( self, request ):
        form = AddDepartmentForm()
        context = {
            "form": form
        }
        return TemplateResponse(request, "add-departments.html",context)
    def post( self, request ):
        form = AddDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("department")
        context = {
            'form':form 
        }
        print("99999999999999999999999999999999999999999999",form.errors)
        print("00000000000000000000000000000000000000000000",form.data)
        return TemplateResponse(request,"add-departments.html",context)
    


class EditDepartmentViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.edit_department'

    def get(self, request, department_id):
        department = get_object_or_404(GroupSpec, id=department_id)
        form = AddDepartmentForm(instance=department)
        context = {
            'form': form,
            'department': department
        }
        return TemplateResponse(request, 'edit-department.html', context)
    
    def post(self, request, department_id):
        department = get_object_or_404(GroupSpec, id=department_id)
        form = AddDepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department')
        context = {
            'form': form,
            'department': department
        }
        print(form.errors)
        print(form.data)
        return TemplateResponse(request, 'edit-department.html', context)
    
class DeleteDepartmentViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.delete_department'

    def get(self, request, department_id):
        department = get_object_or_404(GroupSpec, id=department_id)
        department.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))



class AllSkillsViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.all_skill'

    def get(self,request):
        skills = Skill.objects.all()
        context = {
            'skills':skills
        }
        return TemplateResponse(request, "all-skills.html",context)
    

class AddSkillViewset(LoginRequiredMixin,View):
    login_url = 'login'
    def get( self, request ):
        form = AddSkillForm()
        context = {
            "form": form
        }
        return TemplateResponse(request, "add-skill.html",context)
    def post( self, request ):
        form = AddSkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_skills")
        context = {
            'form':form 
        }
        print("99999999999999999999999999999999999999999999",form.errors)
        print("00000000000000000000000000000000000000000000",form.data)
        return TemplateResponse(request,"add-skill.html",context)
    
class DeleteSkillViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.delete_skill'
    def get(self, request, skill_id):
        skill = get_object_or_404(Skill, id=skill_id)
        skill.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))
    
class EditSkillViewset(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'login'
    permission_required = 'teacher.edit_skill'

    def get(self, request, skill_id):
        skill = get_object_or_404(Skill, id=skill_id)
        form =  EditSkillForm(instance=skill)
        context = {
            'form': form,
            'skill': skill
        }
        return TemplateResponse(request, 'edit-skill.html', context)
    
    def post(self, request, skill_id):
        skill = get_object_or_404(Skill, id=skill_id)
        form = EditSkillForm(request.POST, request.FILES, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('all_skills')
        context = {
            'form': form,
            'skill': skill
        }
        print(form.errors)
        print(form.data)
        return TemplateResponse(request, 'edit-skill.html', context)
    

class AddLikeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        print('Get request------------------------')
        user = Teacher.objects.get(id=request.user.id)
        like= GroupLikes.objects.filter(group=group, user_id=user)
            
        if like:
            liked = True
        
        if not like:
            liked = False

        likes = group.grouplikes_set.count()
        return JsonResponse({'likes': likes, 'liked': liked})

    def post(self, request, group_id):
        try:
            group = get_object_or_404(Group, id=group_id)
            user = Teacher.objects.get(id=request.user.id)

            like, created = GroupLikes.objects.get_or_create(group=group, user_id=user)
            
            if created:
                like.save()
                liked = True
            
            if not created:
                like.delete()
                liked = False

            likes = group.grouplikes_set.count()
            return JsonResponse({'liked': liked, 'likes': likes})

        except:
            return HttpResponse(status=404)
