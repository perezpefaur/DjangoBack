from django_filters import rest_framework as filters
from .models import UserProfile, Module


# We create filters for each field we want to be able to filter on
class TeachersFilter(filters.FilterSet):
    nombre = filters.CharFilter(lookup_expr='icontains')
    apellido = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    celular = filters.CharFilter(lookup_expr='icontains')
    comunas = filters.CharFilter(lookup_expr='icontains')
    ramos = filters.CharFilter(lookup_expr='icontains')
    materias = filters.CharFilter(lookup_expr='icontains')
    instituciones = filters.CharFilter(lookup_expr='icontains')
    precio_min = filters.NumberFilter(field_name='precio', lookup_expr='gt')
    precio_max = filters.NumberFilter(field_name='precio', lookup_expr='lt')

    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido', 'email', 'celular', 'comunas',
                  'ramos', 'materias', 'instituciones', 'precio_min', 'precio_max']


class ModulesFilter(filters.FilterSet):
    teacher = filters.NumberFilter(lookup_expr='icontains')
    start_time = filters.TimeFilter(lookup_expr='icontains')
    end_time = filters.TimeFilter(lookup_expr='icontains')
    reservationBool = filters.BooleanFilter(lookup_expr='icontains')
    date = filters.DateFilter(lookup_expr='icontains')

    class Meta:
        model = Module
        fields = ['id', 'teacher', 'start_time', 'end_time',
                  'reservationBool', 'date']
