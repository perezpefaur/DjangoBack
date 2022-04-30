from django_filters import rest_framework as filters
from .models import UserProfile, Module


# We create filters for each field we want to be able to filter on
class TeachersFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    mail = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
    comunas = filters.CharFilter(lookup_expr='icontains')
    assignature = filters.CharFilter(lookup_expr='icontains')
    subjects = filters.CharFilter(lookup_expr='icontains')
    institutions = filters.CharFilter(lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'mail', 'phone', 'comunas',
                  'assignature', 'subjects', 'institutions', 'price_min', 'price_max']


class ModulesFilter(filters.FilterSet):
    teacher = filters.NumberFilter(field_name='teacher')
    start_time = filters.TimeFilter(lookup_expr='icontains')
    end_time = filters.TimeFilter(lookup_expr='icontains')
    reservation_bool = filters.BooleanFilter(lookup_expr='icontains')
    date = filters.DateFilter(lookup_expr='icontains')
    prace = filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Module
        fields = ['id', 'teacher', 'start_time', 'end_time',
                  'reservation_bool', 'date']
