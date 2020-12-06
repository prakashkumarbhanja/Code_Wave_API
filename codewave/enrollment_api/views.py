from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from .serializers import (Create_User_Serializer,
                          Registered_user_update_delete_Serializer
                          , Add_Course_by_Teacher_Serializer
                          ,Enroll_Class_by_Student_Serializer)
from .models import (Student, Teacher, classrooms, Enroll_Courses)


class Register_Api(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        all_user = User.objects.all()
        user_serializer = Registered_user_update_delete_Serializer(all_user, many=True)
        return Response(user_serializer.data, status=200)

    def post(self, request):
        user_serializer = Create_User_Serializer(data=request.data)
        if user_serializer.is_valid():
            if User.objects.filter(email=request.data.get('email')):
                return Response("Email ID alreday registered, try with differnt", status=400)
            else:
                user = User.objects.create_user(username=self.request.data.get('username'),
                                                email=self.request.data.get('email'),
                                                password = self.request.data.get('password'))
                return Response('User Created Successfully', status=201)
        else:
            return Response(user_serializer.errors, status=400)


class Registered_user_update_delete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            return Response("Searched User Doesnot Exists", status=400)

        serializer = Registered_user_update_delete_Serializer(user)
        return Response(serializer.data, status=200)


    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            return Response("Searched User Doesnot Exists", status=400)

        serializer = Registered_user_update_delete_Serializer(user, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            return Response("Searched User Doesnot Exists", status=400)

        user.delete()
        return Response("deleted Successfully", status=204)


class Add_Course_by_Teacher(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        course = classrooms.objects.all()
        serializer = Add_Course_by_Teacher_Serializer(course, many=True)
        return Response(serializer.data, status=200)


    def post(self, request):

        user = self.request.user
        serializer = Add_Course_by_Teacher_Serializer(data=self.request.data)
        if serializer.is_valid():
            teacher_user_id = Teacher.objects.all()

            try:
                teacher_user_id = Teacher.objects.get(user_tchr=user.id)
            except:
                return Response("Please Loged in as a Teacher", status=400)

            if str(user) == str(teacher_user_id):
                teacher_user_id.classrooms_set.create(course_name=self.request.data.get('course_name'),
                                                          course_img=self.request.data.get('course_img'),
                                                          description=self.request.data.get('description'))

                return Response("Class Added Successfully", status=200)

            else:
                return Response("Loged in user is a Student so Please Logged in as Teacher and Add Courses",
                                status=400)
        else:
            return Response(serializer.errors, status=400)



class Add_Course_by_Teacher_Retrive_Update_Delete(RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = Add_Course_by_Teacher_Serializer
    lookup_url_kwarg = 'pk'
    queryset = classrooms.objects.all()


class Enroll_Class_by_Student(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        student = Student.objects.get(id=self.request.user.id)
        serializer = Enroll_Class_by_Student_Serializer(data=self.request.data)

        if serializer.is_valid():
            course_id = self.request.data.get('enter_course_id')

            try:
                cls_room = classrooms.objects.get(id=course_id)
            except:
                return Response("Classroom Not Found", status=404)
            teacher = Teacher.objects.get(id=cls_room.teacher.id)
            if cls_room:

                enrl_class = Enroll_Courses.objects.filter(Q(student_name=self.request.user.id) & Q(enrolled_class=course_id) & Q(is_enrolled=True))

                if enrl_class:
                    return Response("Class Already Enrolled to Logged in User", status=400)
                else:
                    Enroll_Courses.objects.create(enrolled_class=cls_room, teacher_name=teacher, student_name=student, is_enrolled=True)
                    """Any One save method can use Here"""
                    # cls_room.enroll_courses_set.create(teacher_name=teacher, student_name=student, is_enrolled=True)
                    return Response("Addedd Successfully", status=201)
            else:
                return Response("Class not exists to add", status=400)

        else:
            return Response("Not Valid Data", status=400)
