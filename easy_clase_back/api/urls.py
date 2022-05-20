from django.urls import path
from api.views import RegisterView, TeachersAPIView, TeacherAPIView, PerfilAPIView, ModuleAPIView, ModulesAPIView, SubjectAPIView, SubjectsAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('teachers_list/', TeachersAPIView.as_view(), name='teachers_view'),
    path('teacher/<int:pk>/', TeacherAPIView.as_view(), name='get_teacher'),
    path('me/', PerfilAPIView.as_view(), name='get_profile'),
    path('module/', ModuleAPIView.as_view(), name='module'),
    path('modules/', ModulesAPIView.as_view(), name='modules'),
    path('subject/', SubjectAPIView.as_view(), name='subject'),
    path('subjects/', SubjectsAPIView.as_view(), name='subjects')
]
