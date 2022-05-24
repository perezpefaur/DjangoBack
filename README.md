# DjangoBack

## Instalaciones

Mac:

```console
user@MacBook-Air easy_clase_back % pip3 install -r requirements.txt
```

windows:

```console
user@MacBook-Air easy_clase_back % pip install -r requirements.txt
```

Correr migraciones:

```console
user@MacBook-Air easy_clase_back % python3 manage.py migrate
```

Correr el servidor:

```console
user@MacBook-Air easy_clase_back % python3 manage.py runserver
```

## Uso de la API

## Creacion de Usuarios y Tokens


Para crear super user

user@MacBook-Air easy_clase_back python3 manage.py createsuperuser

Ingresar con esa cuenta en http://127.0.0.1:8000/admin permite administrar la base de datos

Primero creamos un usuario para poder hacer login.

Input:
```
http POST http://127.0.0.1:8000/api/register/
```

```
{
    "first_name": "foo",
    "last_name": "bar",
    "mail": "foo@bar.cl",
    "phone": "47454345",
    "password": "pass..",
    "password2": "pass..",
    "is_teacher": "True"
}
```

Output:
```
{
    "id": 14,
    "first_name": "Matias",
    "last_name": "Perez",
    "mail": "peredfar@cd.cl",
    "phone": "47454345",
    "comunas": "",
    "subjects": "",
    "institutions": "",
    "price": 0,
    "description": "",
    "is_teacher": true
}
```

Despues que creamos una cuenta podemos utilizar las credenciales anteriores para obtener una token:

Input:
```
http POST http://127.0.0.1:8000/api/token/
```

```
{
    "mail": "foo@bar.cl",
    "password": "pass..",
}
```

Output:
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MTAwMDM0NywianRpIjoiYzA5ZDA2MmNlNTI0NDc2ZmE1ZWVhMjg1ZmMxMDFkYjAiLCJ1c2VyX2lkIjoxM30.VPTPdjg0HhqgedokZki4hmroRCAk07OQk8LtdggekME",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUwOTE0MjQ3LCJqdGkiOiJlN2RmNjFkZDkwMTU0MDEwODdkMWZjOGJjYjZkMGFlMSIsInVzZXJfaWQiOjEzfQ.3uJJRoaNl5rFVQe770Ul76gFgps3HlXc0OI4tjwkQaM"
}
```

Tenemos dos tokens, el access token es para la autentificación para casi todas las request, este token expira, por lo que podemos utilizar el refresh token para obtener una nueva access token.  

```
http http://127.0.0.1:8000/api/token/refresh/ refresh="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
```
y vamos a tener una nueva token
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```

## Documentación de Endpoints
- Account: https://documenter.getpostman.com/view/15365986/UyrGAtaU 
- Auth: https://documenter.getpostman.com/view/15365986/UyrGBZqr
- Modules: https://documenter.getpostman.com/view/15365986/UyrGBZvH
- Teachers: https://documenter.getpostman.com/view/15365986/UyrGBZvK
- Institutions: https://documenter.getpostman.com/view/16366665/Uz59MeYQ
- Subjects: https://documenter.getpostman.com/view/16366665/Uz59MeYR