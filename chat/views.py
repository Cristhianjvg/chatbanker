# Importa las clases necesarias
from django.shortcuts import render
import sys, os
import re
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
    
    
def descargar_archivos(request):
    # 1 args = SharePoint folder name. May include subfolders YouTube/2022
    FOLDER_NAME = sys.argv[1]
    # 2 args = locate or remote folder_dest
    FOLDER_DEST = sys.argv[2]
    # 3 args = SharePoint file name. This is used when only one file is being downloaded
    # If all files will be downloaded, then set this value as "None"
    FILE_NAME = sys.argv[3]
    # 4 args = SharePoint file name pattern
    # If no pattern match files are required to be downloaded, then set this value as "None"
    FILE_NAME_PATTERN = sys.argv[4]

    if FILE_NAME != 'None':
        file_obj = SharePoint().download_file(FILE_NAME, FOLDER_NAME)
        file_dir_path = PurePath(FOLDER_DEST, FILE_NAME)
        with open(file_dir_path, 'wb') as f:
            f.write(file_obj)
    elif FILE_NAME_PATTERN != 'None':
        files_list = SharePoint()._get_files_list(FOLDER_NAME)
        for file in files_list:
            if re.search(FILE_NAME_PATTERN, file.name):  # Cambiado de "keyword" a "FILE_NAME_PATTERN"
                file_obj = SharePoint().download_file(file.name, FOLDER_NAME)  # Usar el nombre del archivo actual
                file_dir_path = PurePath(FOLDER_DEST, file.name)  # Usar el nombre del archivo actual
                with open(file_dir_path, 'wb') as f:
                    f.write(file_obj)
    return HttpResponse("Descarga completada")

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
    
