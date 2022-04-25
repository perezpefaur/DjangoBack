from django_filters import rest_framework as filters
from .models import UserProfile


# We create filters for each field we want to be able to filter on
class ProfesoresFilter(filters.FilterSet):
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
        fields = ['nombre', 'apellido', 'email', 'celular', 'comunas', 'ramos', 'materias', 'instituciones', 'precio_min', 'precio_max']