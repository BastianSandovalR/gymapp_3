from django.urls import path
from . import views
from .views import historial_ejercicio

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nueva_rutina/', views.nueva_rutina, name='nueva_rutina'),
    path('rutina/<int:rutina_id>/agregar_series/', views.agregar_series, name='agregar_series'),
    path('rutina/<int:rutina_id>/', views.detalle_rutina, name='detalle_rutina'),
    path('progreso/', views.progreso, name='progreso'),
    path('progreso/datos/', views.obtener_datos_progreso, name='obtener_datos_progreso'),
    path('serie/<int:serie_id>/editar/', views.editar_serie, name='editar_serie'),
    path('serie/<int:serie_id>/editar_vivo/', views.editar_serie_vivo, name='editar_serie_vivo'),
    path("api/historial/<int:usuario_id>/<int:ejercicio_id>/", historial_ejercicio, name="historial_ejercicio"),
    

]
