from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Student, Teacher, classrooms, Enroll_Courses)


class Create_User_Serializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}


    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError('Password donot matching')
        else:
            return data

class Registered_user_update_delete_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'last_login', 'password']


class Add_Course_by_Teacher_Serializer(serializers.ModelSerializer):

    class Meta:
        model = classrooms
        # fields = ['id', 'course_name', 'course_img', 'description', 'add_on']
        exclude = ['teacher']

    def validate(self, data):
        course_name = data.get('course_name')

        if classrooms.objects.filter(course_name=course_name):
            raise serializers.ValidationError('Opps!!! Same Course Exists in Classrooms')
        else:
            return data

class Enroll_Class_by_Student_Serializer(serializers.ModelSerializer):
    enter_course_id = serializers.IntegerField()
    class Meta:
        model = Enroll_Courses
        fields = ['enter_course_id']