from django.shortcuts import render, redirect, get_object_or_404
from .models import Rutina, Serie, Usuario, Ejercicio
from .forms import RutinaForm, SerieForm
from collections import defaultdict
from django.http import JsonResponse
from django.db.models import Max

def inicio(request):
    rutinas = Rutina.objects.all().order_by('-fecha')
    return render(request, 'inicio.html', {'rutinas': rutinas})

def nueva_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save()
            return redirect('agregar_series', rutina_id=rutina.id)
    else:
        form = RutinaForm()
    return render(request, 'nueva_rutina.html', {'form': form})

from collections import defaultdict

def agregar_series(request, rutina_id):
    rutina = get_object_or_404(Rutina, id=rutina_id)

    if request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.rutina = rutina
            serie.save()
            return redirect('agregar_series', rutina_id=rutina.id)  # Recargar la página para actualizar los datos
    else:
        form = SerieForm()

    # Optimiza la consulta
    series = rutina.series.select_related('usuario', 'ejercicio').all()

    # Agrupar series por usuario y, dentro de cada usuario, por ejercicio
    series_por_usuario_ejercicio = defaultdict(lambda: defaultdict(list))
    for serie in series:
        series_por_usuario_ejercicio[serie.usuario][serie.ejercicio].append(serie)

    # Convertir a un diccionario normal anidado
    agrupado = {usuario: dict(ejercicios) for usuario, ejercicios in series_por_usuario_ejercicio.items()}

    return render(request, 'agregar_series.html', {
        'form': form,
        'rutina': rutina,
        'series_por_usuario': agrupado  # Ahora es un diccionario anidado: usuario -> ejercicio -> lista de series
    })

def detalle_rutina(request, rutina_id):
    rutina = get_object_or_404(Rutina, id=rutina_id)

    # 💡 Agrupar series por usuario
    series_por_usuario = defaultdict(list)
    series = rutina.series.select_related('usuario', 'ejercicio').all()
    for serie in series:
        series_por_usuario[serie.usuario].append(serie)

    return render(request, 'detalle_rutina.html', {
        'rutina': rutina,
        'series_por_usuario': dict(series_por_usuario)  # Convertir a diccionario normal
    })
def progreso(request):
    usuarios = Usuario.objects.all()
    ejercicios = Ejercicio.objects.all()
    return render(request, 'progreso.html', {'usuarios': usuarios, 'ejercicios': ejercicios})

def obtener_datos_progreso(request):
    usuario_id = request.GET.get('usuario_id')
    ejercicio_id = request.GET.get('ejercicio_id')

    series = Serie.objects.filter(usuario_id=usuario_id, ejercicio_id=ejercicio_id).order_by('rutina__fecha')

    datos = {
        "fechas": [serie.rutina.fecha.strftime("%d-%m-%Y") for serie in series],
        "pesos": [serie.peso for serie in series],
        "repeticiones": [serie.repeticiones for serie in series]
    }

    return JsonResponse(datos)
def editar_serie(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    
    if request.method == "POST":
        form = SerieForm(request.POST, instance=serie)
        if form.is_valid():
            form.save()
            return redirect('detalle_rutina', rutina_id=serie.rutina.id)
    else:
        form = SerieForm(instance=serie)
    
    return render(request, 'editar_serie.html', {'form': form, 'serie': serie})

def editar_serie_vivo(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    
    if request.method == "POST":
        form = SerieForm(request.POST, instance=serie)
        if form.is_valid():
            form.save()
            return redirect('agregar_series', rutina_id=serie.rutina.id)
    else:
        form = SerieForm(instance=serie)
    
    return render(request, 'agregar_series.html', {'form': form, 'serie': serie})


def historial_ejercicio(request, usuario_id, ejercicio_id):
    # Obtén el id de la rutina actual (para excluirla del historial)
    rutina_actual_id = request.GET.get('rutina_id')
    
    # Filtra las series del usuario y ejercicio
    qs = Serie.objects.filter(usuario_id=usuario_id, ejercicio_id=ejercicio_id)
    if rutina_actual_id:
        qs = qs.exclude(rutina_id=rutina_actual_id)
    
    # Usa select_related para optimizar la consulta y ordena por la fecha de la rutina (descendente)
    qs = qs.select_related('rutina').order_by('-rutina__fecha')
    
    # Agrupa las series por rutina (usando el id de la rutina)
    rutinas_dict = {}
    for serie in qs:
        rut_id = serie.rutina.id
        if rut_id not in rutinas_dict:
            rutinas_dict[rut_id] = {
                'fecha': serie.rutina.fecha,  # Se guarda como objeto datetime para ordenar
                'series': []
            }
        rutinas_dict[rut_id]['series'].append({
            'peso': serie.peso,
            'repeticiones': serie.repeticiones,
            'numero_serie': serie.numero_serie,  # Se incluye aquí
            'nota': serie.nota if serie.nota else "Sin nota"
})

    
    # Convertir el diccionario en una lista y ordenarla por fecha descendente
    rutinas_list = list(rutinas_dict.values())
    rutinas_list.sort(key=lambda x: x['fecha'], reverse=True)
    
    # Limitar a las últimas 3 rutinas
    rutinas_list = rutinas_list[:3]
    
    # Convertir la fecha a formato de cadena para el JSON
    for rut in rutinas_list:
        rut['fecha'] = rut['fecha'].strftime("%d-%m-%Y")
    
    return JsonResponse(rutinas_list, safe=False)