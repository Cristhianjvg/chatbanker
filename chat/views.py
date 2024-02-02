# Importa las clases necesarias
from django.shortcuts import render
import sys, os
import re
from chatbanker import settings
from office365_api import SharePoint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .Agent import Agent  # Asegúrate de importar correctamente tu clase Agent
from pathlib import PurePath

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
            filename = uploaded_file.name
            if fs.exists(filename):
                return HttpResponse(f'Error: Ya existe un archivo con el nombre {filename}.')
            
            filename = fs.save(filename, uploaded_file)
            file_name_without_extension, _ = os.path.splitext(filename)
            file_url = fs.url(filename)
            file_urls.append(file_url)

            # Usa la instancia de agent ya inicializada
            agent.ingest(fs.path(filename), file_name_without_extension)  # Proporciona la ruta del archivo en el sistema de archivos

        # Puedes hacer más cosas aquí, como procesar los archivos o devolver alguna respuesta
        return HttpResponse(f'Archivos subidos exitosamente. URLs: {", ".join(file_urls)}')

    return render(request, 'pdf-correcto.html')


@csrf_exempt
def principal(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        agent.load()
        # Usa la instancia de agent ya inicializada
        bot_response = agent.ask(user_message)
        return HttpResponse(bot_response)
    else:
        return render(request, "principal.html")
    
@csrf_exempt
def chatprincipal(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        agent.load()
        # Usa la instancia de agent ya inicializada
        bot_response = agent.ask(user_message)
        return HttpResponse(bot_response)
    else:
        return render(request, "chatprincipal.html")
    
    
import re
from pathlib import PurePath
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def descargar_archivos(request):
    if request.method == 'POST':
        FOLDER_NAME = request.POST.get('folder_name')
        FOLDER_DEST = request.POST.get('folder_dest')
        FILE_NAME = request.POST.get('file_name')
        FILE_NAME_PATTERN = request.POST.get('file_name_pattern')

        if FILE_NAME != 'None':
            file_obj = SharePoint().download_file(FILE_NAME, FOLDER_NAME)
            file_dir_path = PurePath(FOLDER_DEST, FILE_NAME)
            with open(file_dir_path, 'wb') as f:
                f.write(file_obj)
        elif FILE_NAME_PATTERN != 'None':
            files_list = SharePoint()._get_files_list(FOLDER_NAME)
            for file in files_list:
                if re.search(FILE_NAME_PATTERN, file.name):
                    file_obj = SharePoint().download_file(file.name, FOLDER_NAME)
                    file_dir_path = PurePath(FOLDER_DEST, file.name)
                    with open(file_dir_path, 'wb') as f:
                        f.write(file_obj)
        return HttpResponse("Descarga completada")
    else:
        return HttpResponse("Método no permitido")


def lista_pdf(request):
    # Directorio donde se almacenan los archivos PDF
    directorio_pdf = settings.MEDIA_ROOT

    # Obtener la lista de archivos PDF en el directorio
    archivos_pdf = [archivo for archivo in os.listdir(directorio_pdf) if archivo.endswith('.pdf')]

    # Imprimir los nombres de los archivos PDF
    print("Archivos PDF encontrados:", archivos_pdf)

    return render(request, 'listarpdf.html', {'archivos_pdf': archivos_pdf})

# def save_file(file_n, file_obj):
#     file_dir_path = PurePath(FOLDER_DEST, file_n)
#     with open(file_dir_path, 'wb') as f:
#         f.write(file_obj)

# def get_file(file_n, folder):
#     file_obj = SharePoint().download_file(file_n, folder)
#     save_file(file_n, file_obj)

# def get_files(folder):
#     files_list = SharePoint()._get_files_list(folder)
#     for file in files_list:
#         get_file(file.name, folder)

# def get_files_by_pattern(keyword, folder):
#     files_list = SharePoint()._get_files_list(folder)
#     for file in files_list:
#         if re.search(keyword, file.name):
#             get_file(file.name, folder)
    
