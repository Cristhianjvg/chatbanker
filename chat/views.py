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
def chat_general(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        agent.load()
        # Usa la instancia de agent ya inicializada
        bot_response = agent.ask(user_message)
        return HttpResponse(bot_response)
    else:
        return render(request, 'chatgeneral.html')
    

@csrf_exempt
def pdf_correcto(request):
    if request.method == 'POST':
        # Obtenemos los archivos del formulario con el nombre 'archivos[]'
        uploaded_files = request.FILES.getlist('archivos[]')
        file_urls = []

        # Guardamos cada archivo en el directorio 'media'
        fs = FileSystemStorage()

        for uploaded_file in uploaded_files:
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_name_without_extension, _ = os.path.splitext(filename)
            file_url = fs.url(filename)
            file_urls.append(file_url)

            # Usa la instancia de agent ya inicializada
            agent.ingest(fs.path(filename), file_name_without_extension)  # Proporciona la ruta del archivo en el sistema de archivos

        # Puedes hacer más cosas aquí, como procesar los archivos o devolver alguna respuesta
        return HttpResponse(f'Archivos subidos exitosamente. URLs: {", ".join(file_urls)}')

    return render(request, 'pdf-correcto.html')

