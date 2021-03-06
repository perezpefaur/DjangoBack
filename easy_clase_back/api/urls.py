from django.urls import path
from api.views import ReservationCheckAPIView, RegisterView, TeachersAPIView, TeacherAPIView, PerfilAPIView, ModuleAPIView, ModulesAPIView, SubjectAPIView, SubjectsAPIView, InstitutionAPIView, InstitutionsAPIView, ReservationAPIView, CommentAPIView, CommentsAPIView, TransactionAPIView, TransactionsAPIView
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
    path('subjects/', SubjectsAPIView.as_view(), name='subjects'),
    path('institution/', InstitutionAPIView.as_view(), name='institution'),
    path('institutions/', InstitutionsAPIView.as_view(), name='institutions'),
    path('reservation/', ReservationAPIView.as_view(), name='reservation'),
    path('comment/', CommentAPIView.as_view(), name='comment'),
    path('comments/', CommentsAPIView.as_view(), name='comments'),
    path('transaction/', TransactionAPIView.as_view(), name='transaction'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    path('reservation_check/', ReservationCheckAPIView.as_view(),
         name='reservation_check')
]
