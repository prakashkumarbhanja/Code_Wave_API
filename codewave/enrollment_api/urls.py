from django.urls import path
from rest_framework.authtoken import views
from .views import (Register_Api, Registered_user_update_delete, Add_Course_by_Teacher, Add_Course_by_Teacher_Retrive_Update_Delete,
                    Enroll_Class_by_Student)


urlpatterns = [

    path('api_register/', Register_Api.as_view(), name='api_register'),
    path('registered_update_delete/<int:pk>/', Registered_user_update_delete.as_view(), name='registered_update_delete'),
    path('add_course_by_teacher/', Add_Course_by_Teacher.as_view(), name='add_course_by_teacher'),
    path('Add_Course_by_Teacher_Retrive_Update_Delete/<int:pk>/', Add_Course_by_Teacher_Retrive_Update_Delete.as_view(), name='Add_Course_by_Teacher_Retrive_Update_Delete'),
    path('Enroll_Class_by_Student/', Enroll_Class_by_Student.as_view(), name='Enroll_Class_by_Student'),
    # path('login/', views.obtain_auth_token, name='login'),

]
