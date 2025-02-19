. Crear proyecto
django-admin startproject nombre_del_proyecto

activar entorno virtual -> env\Scripts\activate
ejecutar servidor django -> python manage.py runserver
ejecutar migraciones -> python manage.py migrate

superusuario
ignacio
ifebles@gmail.com
pass: qwer1234

. Ejecutar servidor
python manage.py runserver

. hacer migraciones
python manage.py makemigrations

.construir c├│digo sql
python manage.py sqlmigrate gestionpedidos 0001

. hacer la migraci├│n que crea las tablas
python manage.py migrate

. abrir el shell
python manage.py shell
from gestionpedidos.models import Articulos

. Agregar articulos
art=Articulos(nombre='mesa', seccion='decoracion', precio=90)
art.save()
art2=Articulos(nombre='camisa', seccion='confecci├│n', precio=75)
art2.save()

. Agregar articulos de una sola vez
art3=Articulos.objects.create(nombre='taladro', seccion='ferreteria', precio=65)

. Modificar precio
art.precio=95
art.save()

. Eliminar registro
art4=Articulos.objects.get(id=3)
art4.delete()
(1, {'gestionpedidos.Articulos': 1})

. Select
lista=Articulos.objects.all()
lista
<QuerySet [<Articulos: Articulos object (1)>, <Articulos: Articulos object (2)>]>
>>> lista.query.__str__()
'SELECT "gestionpedidos_articulos"."id", "gestionpedidos_articulos"."nombre", "gestionpedidos_articulos"."seccion", "gestionpedidos_articulos"."precio" FROM
"gestionpedidos_articulos"'

. bbdd postgres
('localhost', 'wt_data', 'postgres', 'postgres1*', '5432')
. instalamos libreria
pip install psycopg2
. revisamos migraciones
python manage.py makemigrations
. hacemos las migraciones
python manage.py migrate
. llamamos shell
python manage.py shell
. agregamos un registro
from gestionpedidos.models import Clientes
c=Clientes(nombre='Juan',direccion='Camarena', telefono='6639537')
c.save()

consultas
. from gestionpedidos.models import Articulos
. Articulos.objects.filter(seccion='deportes')
<QuerySet [<Articulos: Articulos object (5)>, <Articulos: Articulos object (6)>]> <- devuelve una tupla
. Cambiamos el modelo
    def __str__(self):
        return 'El nombre es: %s, la secci├│n es: %s y el precio es: %s' %(self.nombre, self.seccion, self.precio)
. Articulos.objects.filter(seccion='deportes')
. Articulos.objects.filter(nombre='mesa', seccion='decoracion')
. Articulos.objects.filter(seccion='deportes', precio__gte=100)
. Articulos.objects.filter(seccion='deportes', precio__lte=100)
. Articulos.objects.filter(precio__gte=100).order_by('precio')
. Articulos.objects.filter(precio__gte=100).order_by('-precio') -> ordena DESC

superusuario
. user: ignacio
. pass: 123456
. email: ifebles@gmail.com

. Ejecutar servidor
python manage.py runserver

. hacer migraciones
python manage.py makemigrations

.construir c├│digo sql
python manage.py sqlmigrate gestionpedidos 0001

. hacer la migraci├│n que crea las tablas
python manage.py migrate

. abrir el shell
python manage.py shell
from gestionpedidos.models import Articulos

. Agregar articulos
art=Articulos(nombre='mesa', seccion='decoracion', precio=90)
art.save()
art2=Articulos(nombre='camisa', seccion='confecci├│n', precio=75)
art2.save()

. Agregar articulos de una sola vez
art3=Articulos.objects.create(nombre='taladro', seccion='ferreteria', precio=65)

. Modificar precio
art.precio=95
art.save()

. Eliminar registro
art4=Articulos.objects.get(id=3)
art4.delete()
(1, {'gestionpedidos.Articulos': 1})

. Select
lista=Articulos.objects.all()
lista
<QuerySet [<Articulos: Articulos object (1)>, <Articulos: Articulos object (2)>]>
>>> lista.query.__str__()
'SELECT "gestionpedidos_articulos"."id", "gestionpedidos_articulos"."nombre", "gestionpedidos_articulos"."seccion", "gestionpedidos_articulos"."precio" FROM
"gestionpedidos_articulos"'

. bbdd postgres
('localhost', 'wt_data', 'postgres', 'postgres1*', '5432')
. instalamos libreria
pip install psycopg2
. revisamos migraciones
python manage.py makemigrations
. hacemos las migraciones
python manage.py migrate
. llamamos shell
python manage.py shell
. agregamos un registro
from gestionpedidos.models import Clientes
c=Clientes(nombre='Juan',direccion='Camarena', telefono='6639537')
c.save()

consultas
. from gestionpedidos.models import Articulos
. Articulos.objects.filter(seccion='deportes')
<QuerySet [<Articulos: Articulos object (5)>, <Articulos: Articulos object (6)>]> <- devuelve una tupla
. Cambiamos el modelo
    def __str__(self):
        return 'El nombre es: %s, la secci├│n es: %s y el precio es: %s' %(self.nombre, self.seccion, self.precio)
. Articulos.objects.filter(seccion='deportes')
. Articulos.objects.filter(nombre='mesa', seccion='decoracion')
. Articulos.objects.filter(seccion='deportes', precio__gte=100)
. Articulos.objects.filter(seccion='deportes', precio__lte=100)
. Articulos.objects.filter(precio__gte=100).order_by('precio')
. Articulos.objects.filter(precio__gte=100).order_by('-precio') -> ordena DESC

superusuario
. user: ignacio
. pass: 123456
. email: ifebles@gmail.com

. Crear proyecto
django-admin startproject appfp

. Ejecutar migraciones
python manage.py migrate

. Crear primer usuario desde consola
python manage.py createsuperuser

. Par├ímetros de la bbdd en settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'appfp_data',
        'USER': 'postgres',
        'PASSWORD': 'postgres1*',
        'HOST': 'localhost',
        'DATABASE_PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',  # Aseg├║rate de usar UTF-8
        }
    }
}

. Crear nueva app, nueva aplicacion
python manage.py startapp home
python manage.py startapp moves

. Migraciones
python manage.py makemigrations
python manage.py migrate

. Mostrar migraciones
python manage.py showmigrations

. Llevar migracion moves al estado 0002
python manage.py migrate moves 0002

https://chatgpt.com/share/67851548-58a4-8001-aa49-a45aa1a20a0d-----


Caso práctico curso Analista de Datos Google
https://iffp.onrender.com/thing/pdf/

Kaggle
https://www.kaggle.com/code/ignaciofebles/casopractico

Obtener requirements.txt antes de subir a producción
pip freeze > requirements.txt