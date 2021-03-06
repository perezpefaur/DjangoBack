from django_filters import rest_framework as filters
from .models import UserProfile, Module, Subject, Institution, Reservation, Comment


# We create filters for each field we want to be able to filter on
class TeachersFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    mail = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
    comunas = filters.CharFilter(lookup_expr='icontains')
    subjects = filters.CharFilter(lookup_expr='icontains')
    institutions = filters.CharFilter(lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'mail', 'phone', 'comunas',
                  'subjects', 'institutions', 'price_min', 'price_max']


class ModulesFilter(filters.FilterSet):
    teacher = filters.NumberFilter(field_name='teacher')
    start_time = filters.TimeFilter(lookup_expr='icontains')
    end_time = filters.TimeFilter(lookup_expr='icontains')
    reservation_bool = filters.BooleanFilter(lookup_expr='icontains')
    date = filters.DateFilter(lookup_expr='icontains')
    student_id = filters.NumberFilter(field_name='student_id', method='student', label='student_id')

    def student(self, qs, name, value):
        reservation_query = Module.objects.filter(
            reservation__student=value
        )

        return reservation_query
    class Meta:
        model = Module
        fields = ['id', 'teacher', 'start_time', 'end_time',
                  'reservation_bool', 'date', 'student_id']

class SubjectsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = Subject
        fields = ['name']

class InstitutionsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = Institution
        fields = ['name']


class CommentsFilter(filters.FilterSet):
    body = filters.CharFilter(field_name='body', method='filter_body')
    rating = filters.CharFilter(field_name='rating', method='filter_rating')

    class Meta:
        model = Comment
        fields = ['body', 'rating', 'teacher']
        
    def filter_body(self, queryset, body, value):
        return queryset.filter(body__regex=r'(?i)%s[\s\w]+'%value) | queryset.filter(body__regex=r'(?i)%s'%value)

    def filter_rating(self, queryset, rating, value):
        value = value.split(",")
        value = [float(i) for i in value]
        return queryset.filter(rating__gte = value[0], rating__lte = value[1]).order_by('-rating')
