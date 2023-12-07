# Importa las clases necesarias
from django.shortcuts import render
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .Agent import Agent  # Asegúrate de importar correctamente tu clase Agent

# Inicializa la instancia de Agent fuera de los métodos
OPENAI_API_KEY = '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'
agent = Agent(OPENAI_API_KEY)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        agent.load()
        # Usa la instancia de agent ya inicializada
        bot_response = agent.ask(user_message)
        return HttpResponse(bot_response)
    else:
        return render(request, "home.html")

@csrf_exempt
def pdf(request):
    
    # Si no es una solicitud POST, renderizamos la plantilla "pdf.html" con el formulario
    # print(request.method )
    return render(request, 'pdf.html')

@csrf_exempt
def pdf_correcto(request):
    if request.method == 'POST':
        # Obtenemos el archivo del formulario con el nombre 'archivo'
        uploaded_file = request.FILES['archivo']
        # Guardamos el archivo en el directorio 'media' (asegúrate de tener esta configuración en tu settings.py)
        fs = FileSystemStorage()
        
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_name_without_extension, extension = os.path.splitext(filename)
        file_url = fs.url(filename)
        # Usa la instancia de agent ya inicializada
        agent.ingest(fs.path(filename), file_name_without_extension)  # Proporciona la ruta del archivo en el sistema de archivos
        # Puedes hacer más cosas aquí, como procesar el archivo o devolver alguna respuesta
        return HttpResponse(f'Archivo subido exitosamente. URL: {file_url}')
    return render(request, 'pdf-correcto.html-')

