from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.html import format_html

from teacher.models import Group, GroupLikes, GroupSpec, Lesson, LessonFiles, ReadMore, Score_Attendance, Skill, Student, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

        widgets = {
            "group": forms.CheckboxSelectMultiple
        }


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'gender', 'created_at']
    ordering = ("id", "first_name", "last_name")
    sortable_by = ("gender",)
    list_display_links = ['id', 'first_name', 'last_name', 'email']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

        widgets = {
            'skills': forms.CheckboxSelectMultiple
        }


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm
    list_display = ["id", "first_name", "last_name", 'email', 'phone']
    list_display_links = ("id", "first_name", "last_name")

    def save_model(self, request, obj, form, change):
        print(obj.groups.all())
        
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password)
        # obj.save()
        # if 'skills' in form.cleaned_data:
        #     obj.skills.set(form.cleaned_data['skills'])
        return super().save_model(request, obj, form, change)


class LessonFilesAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "lesson"]


class Score_AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'lesson', 'mark', 'is_present']


class DeparmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',"description"]


class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course_code', 'f_description', 'start_from', 'duration', 'formatted_price', 'teacher', 'max_student', 'contact_number', 'lang', 'group_photo']
    
    def formatted_price(self, obj):
        color = "red" if obj.price > 1800000 else "green"
        return format_html(f'<span style="color: {color};">{obj.price:,.2f}</span>')

    def f_description(self, obj):
        return f'{obj.description[:50]}...'


class ReadMoreAdmin(admin.ModelAdmin):
    list_display = ['language', ]
    

class GroupLikesAdmin(admin.ModelAdmin):
    list_display = ['id', 'f_group', 'user_id']

    def f_group(self, obj):
        return f'{obj.group.name} {obj.group.get_lang_display()}'


# Register your models here.
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson)
admin.site.register(Score_Attendance, Score_AttendanceAdmin)
admin.site.register(Skill)
admin.site.register(GroupLikes, GroupLikesAdmin)
admin.site.register(LessonFiles, LessonFilesAdmin)
admin.site.register(GroupSpec,DeparmentAdmin)
admin.site.register(ReadMore, ReadMoreAdmin)
