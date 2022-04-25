from django.urls import path
from api.views import RegisterView, ProfesorsAPIView, ProfesorAPIView, PerfilAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profesors_list/', ProfesorsAPIView.as_view(), name='ProfesorsView'),
    path('profesor/<int:pk>/', ProfesorAPIView.as_view(), name='get_profesor'),
    path('me/', PerfilAPIView.as_view(), name='get_profile'),
]